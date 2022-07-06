from ddoitranslatormodule.BaseFunction import TranslatorModuleFunction
from ddoitranslatormodule.ddoiexceptions.DDOIExceptions import DDOIConfigFileException, DDOIConfigException, DDOIInvalidArguments, DDOIKTLTimeOut
from ddoitranslatormodule.ddoiexceptions.DDOIExceptions import DDOINotSelectedInstrument, DDOINoInstrumentDefined
import configparser

import os
import ktl
# import ddoi_telescope_translator.tel_utils as utils


class TelescopeBase(TranslatorModuleFunction):

    @staticmethod
    def _load_config(cfg, args=None):
        """
        Load the configuration file for reading

        @param cfg: <str> file path or None
        @param args: <dict> the class arguments

        @return: <class 'configparser.ConfigParser'> the config file parser.
        """
        config_files = [f"default_tel_config.ini"]
        if not cfg and args:
            cfg_path_base = os.path.dirname(os.path.abspath(__file__))
            inst = args.get('instrument', None)
            if inst:
                file_name = f"{inst.lower()}_tel_config.ini"
                cfg = f"{cfg_path_base}/ddoi_configurations/{file_name}"
                config_files.append(cfg)

        # return if config object passed
        param_type = type(cfg)
        if param_type == configparser.ConfigParser:
            return cfg
        elif param_type != str:
            raise DDOIConfigFileException(param_type, configparser.ConfigParser)

        config = configparser.ConfigParser()
        config.read(config_files)

        return config

    @staticmethod
    def _config_param(config, section, param_name):
        """
        Function used to read the config file,  and exit if key or value
        does not exist.

        @param config: <class 'configparser.ConfigParser'> the config file parser.
        @param section: <str> the section name in the config file.
        @param param_name: <str> the 'key' of the parameter within the section.
        @return: <str> the config file value for the parameter.
        """
        try:
            param_val = config[section][param_name]
        except KeyError:
            raise DDOIConfigException(section, param_name)

        if not param_val:
            raise DDOIConfigException(section, param_name)

        return param_val

    @staticmethod
    def _add_args(parser, args_to_add, print_only=False):
        """
        Add the argparse arguments.

        @param parser: <configparser> The parser object
        @param args_to_add: OrderedDict the arguments to add.
            keywords:
                'help' - <str> the help string to add, required
                'type' - <python type>, the argument type,  required
                'req' - <bool> True if the argument is required,  optional
                'kw_arg' - <bool> True for keyword arguments, optional
        @param print_only: <bool> True if add the print_only option

        @return: <configparser> The parser object
        """
        # check to see if print_only is true,  then do not add other arguments.
        if print_only:
            parser.add_argument('--print_only', action='store_true', default=False)
            args = parser.parse_known_args()
            if args[0].print_only:
                return parser

        for arg_name, arg_info in args_to_add.items():
            # add keyword arguments
            if 'kw_arg' in arg_info and arg_info['kw_arg']:
                parser.add_argument(f'{--arg_name}', type=arg_info['type'],
                                    required=arg_info['req'], help=arg_info['help'])
                continue

            # add positional arguments
            parser.add_argument(arg_name, type=arg_info['type'], help=arg_info['help'])

        return parser

    def _add_inst_arg(cls, parser, cfg, is_req=True):
        """
        Add Instrument as a command line argument.

        @param parser: <configparser> The parser object.
        @param cfg: <class 'configparser.ConfigParser'> the config file parser.
        @param is_req: <bool> if the parameter is required or not

        @return: <configparser> The parser object.
        """
        insts = cls._config_param(cfg, 'inst_list', 'insts')
        insts = f'{insts}, {insts.lower()}'
        inst_set = set(insts.split(', '))

        help_str = "Name of instrument for the translator module."
        parser.add_argument("--instrument", type=str, choices=inst_set,
                            required=is_req, help=help_str)

        return parser

    @staticmethod
    def _add_bool_arg(parser, name, msg):
        """

        @param parser: <configparser> The parser object.
        @param name: <str> the parameter name
        @param msg: <str> the help message

        @return: <configparser> The parser object.
        """
        parser.add_argument(f'--{name}', action='store_true', default=False,
                            help=msg)
        return parser

    @staticmethod
    def _get_arg_value(args, key):
        """
        Check the class arguments for the 'key' values.

        @param args: <dict> the command arguments
        @param key: <str> the dictionary key

        @return: The value of the parameter
        """
        val = args.get(key, None)

        if val is None:
            msg = f'{key} argument not defined'
            raise DDOIInvalidArguments(msg)

        return val

    def _write_to_kw(cls, cfg, ktl_service, key_val, logger, cls_name):
        """

        @param cfg:
        @param ktl_service: The KTL service name
        @param key_val: <dict> {cfg_key_name: new value}
            cfg_key_name = the ktl_keyword_name in the config
        @param logger: <DDOILoggerClient>, optional
                The DDOILoggerClient that should be used. If none is provided, defaults to
                a generic name specified in the config, by default None
        @param cls_name: The name of the calling class

        :return: None
        """
        cfg_service = f'ktl_kw_{ktl_service}'

        for cfg_key, new_val in key_val.items():
            ktl_name = cls._config_param(cfg, cfg_service, cfg_key)
            try:
                # ktl.write(ktl_service, ktl_name, new_val, wait=True, timeout=2)
                ktl.read(ktl_service, ktl_name)
            except ktl.TimeoutException:
                msg = f"{cls_name} timeout sending offsets."
                if logger:
                    logger.error(msg)
                raise DDOIKTLTimeOut(msg)

    def get_inst_name(cls, args, cfg, allow_current=True):
        """
        Get the instrument name from the arguments,  if not defined get from
        DCS current instrument.  If allow_current=False,  raise
        DDOINoInstrumentDefined if not defined in arguments.  allow_current=True
        allows the command to be run without a need to define the instrument,
        and using the instrument selected by the TCS.

        @param args: <dict> the arguments passed to calling function
        @param class_name: the name of the calling class for exception

        @return: <str> the instrument name
        """
        inst = args.get('instrument', None)
        if inst:
            # confirm INST = the selected instrument
            current_inst = cls.read_current_inst(cls, cfg)
            if current_inst != inst:
                raise DDOINotSelectedInstrument(current_inst, inst.upper())
            return inst.lower()

        if allow_current:
            inst = cls.read_current_inst(cls, cfg)
        else:
            msg = f'{cls.__name__} requires instrument name to be defined'
            raise DDOINoInstrumentDefined(msg)

        return inst.lower()

    def read_current_inst(cls, cfg):
        ktl_instrument = cls._config_param(cfg, 'ktl_kw_dcs', 'instrument')
        serv_name = cls._config_param(cfg, 'ktl_serv', 'dcs')
        try:
            inst = ktl.read(serv_name, ktl_instrument, timeout=2)
        except ktl.TimeoutException:
            msg = f'timeout reading,  service {serv_name}, ' \
                  f'keyword: {ktl_instrument}'
            raise DDOIKTLTimeOut(msg)

        return inst.lower()

    @staticmethod
    def write_msg(logger, msg, print_only=False):
        if logger and not print_only:
            logger.info(msg)
        else:
            print(msg)

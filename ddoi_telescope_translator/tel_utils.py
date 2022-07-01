import sys
from time import time

from ddoitranslatormodule.ddoiexceptions.DDOIExceptions import DDOIInvalidArguments, DDOIKTLTimeOut, DDOINoInstrumentDefined, DDOIConfigException, DDOINotSelectedInstrument

from ddoi_telescope_translator.wftel import WaitForTel

import ktl


def config_param(config, section, param_name):
    """
    Function used to read the config file,  and exit if key or value does not
    exist.

    :param config: <class 'configparser.ConfigParser'> the config file parser.
    :param section: <str> the section name in the config file.
    :param param_name: <str> the 'key' of the parameter within the section.
    :return: <str> the config file value for the parameter.
    """
    try:
        param_val = config[section][param_name]
    except KeyError:
        raise DDOIConfigException(section, param_name)

    if not param_val:
        raise DDOIConfigException(section, param_name)

    return param_val


def get_arg_value(args, key, logger):
    val = args.get(key, None)

    if val is None:
        msg = f'{key} argument not defined'
        if logger:
            logger.warn(msg)
        else:
            print(msg)

        raise DDOIInvalidArguments(msg)

    return val


def add_args(parser, args_to_add, print_only=False):
    """
    Add the argparse arguments.

    @param parser: the parser object
    @param args_to_add: OrderedDict the arguments to add.
        keywords:
            'help' - <str> the help string to add, required
            'type' - <python type>, the argument type,  required
            'req' - <bool> True if the argument is required,  optional
            'kw_arg' - <bool> True for keyword arguments, optional
    @param print_only: <bool> True if add the print_only option
    @return:
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


def add_bool_arg(parser, name, msg):
    parser.add_argument(f'--{name}', action='store_true', default=False, help=msg)
    return parser


def add_inst_arg(parser, cfg, is_req=True):
    insts = config_param(cfg, 'inst_list', 'insts')
    insts = f'{insts}, {insts.lower()}'
    inst_set = set(insts.split(', '))

    parser.add_argument("--instrument", type=str, choices=inst_set, required=is_req,
                        help="Name of instrument for the translator module.")
    return parser


def check_for_zero_offsets(offset1, offset2, logger):
    if not int(offset1) == 0 and int(offset2) == 0:
        msg = f'Both offsets are zero: {offset1}, {offset2}'
        if logger:
            logger.warn(msg)
        else:
            print(msg)

        return True

    return False


def wait_for_cycle(cfg, dcs_serv, logger):
    start_time = time()

    ktl_auto_resume = config_param(cfg, 'ktl_kw_dcs', 'auto_resume')
    auto_resume = ktl.read(dcs_serv, ktl_auto_resume)

    WaitForTel.execute({"auto_resume": auto_resume})

    elapsed_time = time() - start_time

    msg = f'Move completed in {elapsed_time} seconds'
    if logger:
        logger.warn(msg)
    else:
        print(msg)


def write_to_kw(cfg, ktl_service, key_val, logger, cls_name):
    """

    :param cfg:
    :param ktl_service: The KTL service name
    :param key_val: <dict> {cfg_key_name: new value}
        cfg_key_name = the ktl_keyword_name in the config
    :param logger: <DDOILoggerClient>, optional
            The DDOILoggerClient that should be used. If none is provided, defaults to
            a generic name specified in the config, by default None
    :param cls_name: The name of the calling class

    :return: None
    """
    cfg_service = f'ktl_kw_{ktl_service}'

    for cfg_key, new_val in key_val.items():
        ktl_name = config_param(cfg, cfg_service, cfg_key)
        try:
            # ktl.write(ktl_service, ktl_name, new_val, wait=True, timeout=2)
            ktl.read(ktl_service, ktl_name)
        except ktl.TimeoutException:
            msg = f"{cls_name} timeout sending offsets."
            if logger:
                logger.error(msg)
            raise DDOIKTLTimeOut(msg)


def write_msg(logger, msg, print_only=False):
    if logger and not print_only:
        logger.info(msg)
    else:
        print(msg)


def get_inst_name(args, cfg, class_name, allow_current=True):
    """
    Get the instrument name from the arguments,  if not defined get from
    DCS current instrument.  If allow_current=False,  raise
    DDOINoInstrumentDefined if not defined in arguments.

    @param args: <dict> the arguments passed to calling function
    @param class_name: the name of the calling class for exception

    @return: <str> the instrument name
    """
    inst = args.get('instrument', None)
    if inst:
        # confirm INST = the selected instrument
        current_inst = read_current_inst(cfg)
        if current_inst != inst:
            raise DDOINotSelectedInstrument(current_inst, cls.inst.upper())

    if not inst:
        if allow_current:
            inst = read_current_inst(cfg)
        else:
            msg = f'{class_name} requires instrument name to be defined'
            raise DDOINoInstrumentDefined(msg)

    return inst.lower()


def read_current_inst(cfg):
    ktl_instrument = config_param(cfg, 'ktl_kw_dcs', 'instrument')
    serv_name = config_param(cfg, 'ktl_serv', 'dcs')
    try:
        inst = ktl.read(serv_name, ktl_instrument, timeout=2)
    except ktl.TimeoutException:
        msg = f'timeout reading,  service {serv_name}, keyword: {ktl_instrument}'
        raise DDOIKTLTimeOut(msg)

    return inst.lower()


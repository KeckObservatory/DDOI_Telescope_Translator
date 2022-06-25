import sys
from time import time
from argparse import ArgumentParser

from DDOITranslatorModule.ddoitranslatormodule.ddoiexceptions.DDOIExceptions import DDOIInvalidArguments, \
    DDOIKTLTimeOut, DDOINoInstrumentDefined

from DDOI_Telescope_Translator.wftel import WaitForTel

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
        err_msg = f"Check Config file, there is no parameter name - " \
                  f"section: {section} parameter name: {param_name}"
        sys.exit(err_msg)

    if not param_val:
        err_msg = f"Check Config file, there is no value for " \
                  f"section: {section} parameter name: {param_name}"
        sys.exit(err_msg)

    return param_val


def get_arg_value(args, key, logger):
    val = args.get(key, None)

    if not val:
        msg = f'{key} argument not defined'
        if logger:
            logger.warn(msg)
        else:
            print(msg)

        raise DDOIInvalidArguments(msg)

    return val


def add_args(parser, args_to_add, print_only=False):
    if print_only:
        parser.add_argument('--print_only', action='store_true', default=False)
        args = parser.parse_known_args()
        if args[0].print_only:
            return parser

    for arg_name, arg_info in args_to_add.items():
        parser.add_argument(f'--{arg_name}', type=arg_info['type'],
                            required=arg_info['req'], help=arg_info['help'])

    return parser


def add_bool_arg(parser, name, msg):
    parser.add_argument(f'--{name}', action='store_true', default=False, help=msg)
    return parser


def add_inst_arg(parser, cfg):
    insts = config_param(cfg, 'inst_list', 'insts')
    insts = f'{insts}, {insts.lower()}'
    inst_set = set(insts.split(', '))

    parser.add_argument("--instrument", type=str, choices=inst_set, required=True,
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


def read_auto_resume_val(cfg, dcs_serv):
    kw_auto_resume = config_param(cfg, 'ktl_kw_dcs', 'auto_resume')
    auto_resume = ktl.read(dcs_serv, kw_auto_resume)

    return auto_resume


def wait_for_cycle(cfg, dcs_serv, logger):
    start_time = time()

    auto_resume = read_auto_resume_val(cfg, dcs_serv)
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
    :param logger: <DDOILoggerClient>, optional
            The DDOILoggerClient that should be used. If none is provided, defaults to
            a generic name specified in the config, by default None
    :param cls_name: The name of the calling class

    :return: None
    """
    cfg_service = f'ktl_kw_{ktl_service}'

    for cfg_key, new_val in key_val.items():
        kw_name = config_param(cfg, cfg_service, cfg_key)
        try:
            ktl.write(ktl_service, kw_name, new_val, wait=True, timeout=2)
        except ktl.TimeoutException:
            msg = f"{cls_name} timeout sending offsets."
            if logger:
                logger.error(msg)
            raise DDOIKTLTimeOut(msg)


def write_msg(logger, msg):
    if logger:
        logger.info(msg)
    else:
        print(msg)


def get_inst_name(args, class_name):
    inst = args.get('instrument', None)
    if not inst:
        msg = f'{class_name} requires instrument named to be defined'
        raise DDOINoInstrumentDefined(msg)

    return inst.lower()


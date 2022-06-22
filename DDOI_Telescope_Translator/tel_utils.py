import sys
from time import time

import ktl
from ddoitranslatormodule.DDOIExceptions import DDOIInvalidArguments, \
    DDOIKTLTimeOut, DDOINoInstrumentDefined
from wftel import WaitForTel


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


def check_float(args, key, logger):
    msg = None
    try:
        val = float(args[key])
    except KeyError:
        msg = f'{key} dictionary keys are required.'
    except ValueError:
        msg = f'{key} must be valid float.'

    if msg:
        if logger:
            logger.warn(msg)
        else:
            print(msg)

        raise DDOIInvalidArguments(msg)

    return val


def print_only(args, cfg, cfg_section, key_list):
    """
    Used to check if no args are provided,  meaning print only.

    :param args:
    :param cfg:
    :param cfg_section:
    :param key_list:
    :return:
    """
    for key_name in key_list:
        if args.get(config_param(cfg, cfg_section, key_name), None):
            return False

    return True


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
    inst = args.get('inst', None)
    if not inst:
        msg = f'{class_name} requires instrument named to be defined'
        raise DDOINoInstrumentDefined(msg)

    return inst.lower()


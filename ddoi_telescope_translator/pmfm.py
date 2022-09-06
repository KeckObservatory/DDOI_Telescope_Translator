from ddoitranslatormodule.ddoiexceptions.DDOIExceptions import DDOIKTLTimeOut
from ddoitranslatormodule.BaseTelescope import TelescopeBase

import ktl
from collections import OrderedDict


class PMFM(TelescopeBase):
    """
    pmfm -- set the amount of focus mode in the telescope primary

    Purpose: set primary mirror focus mode

    SYNOPSIS
        PMFM.execute({'pmfm_nm': float})

    DESCRIPTION
        With no argument, show the currently amount of primary mirror
        focus mode.  With a argument, set the amount of primary mirror
        focus mode to the specified number of nanometers.
        script_name - brief description of script function

    OPTIONS

    EXAMPLES
    Example:
        1) show the current amount of pmfm:
            PMFM.execute({'print_only': True})

        2) apply 500 nm of primary mirror focus mode:
            pmfm 500

        3) make pmfm change in background:
            pmfm 500 </dev/null &

    ENVIRONMENT VARIABLES
        list of environment variables used

    FILES
        list of files used

    SERVERS & KEYWORDS
        service = acs
             pmfm: primary mirror focus mode

    SCRIPTS CALLED
        help, syncheck

    KTL SERVICE & KEYWORDS

    adapted from sh script: kss/mosfire/scripts/procs/tel/
    """

    @classmethod
    def add_cmdline_args(cls, parser, cfg=None):
        """
        The arguments to add to the command line interface.

        :param parser: <ArgumentParser>
            the instance of the parser to add the arguments to .
        :param cfg: <class 'configparser.ConfigParser'> the config file parser.

        :return: <ArgumentParser>
        """
        # read the config file
        cfg = cls._load_config(cls, cfg)

        args_to_add = OrderedDict([
            ('pmfm_nm', {'type': float,
                         'help': 'The Primary Mirror Focus Mode (PMFM) to apply.'})
        ])
        parser = cls._add_args(parser, args_to_add, print_only=True)

        return super().add_cmdline_args(parser, cfg)

    @classmethod
    def pre_condition(cls, args, logger, cfg):
        """
        :param args:  <dict> The OB (or subset) in dictionary form
        :param logger: <DDOILoggerClient>, optional
            The DDOILoggerClient that should be used. If none is provided,
            defaults to a generic name specified in the config, by default None
        :param cfg: <class 'configparser.ConfigParser'> the config file parser.

        :return: bool
        """
        return True

    @classmethod
    def perform(cls, args, logger, cfg):
        """
        :param args:  <dict> The OB (or subset) in dictionary form
        :param logger: <DDOILoggerClient>, optional
            The DDOILoggerClient that should be used. If none is provided,
            defaults to a generic name specified in the config, by default None
        :param cfg: <class 'configparser.ConfigParser'> the config file parser.

        :return: None
        """
        serv_name = cls._cfg_val(cfg, 'ktl_serv', 'acs')
        ktl_pmfm = cls._cfg_val(cfg, 'ktl_kw_acs', 'pmfm_nm')
        if args.get('print_only', False):
            current_pmfm = ktl.read(serv_name, ktl_pmfm)
            cls.write_msg(logger, f"The current PMFM is {current_pmfm}",
                          print_only=True)
            return

        pmfm_new = cls._get_arg_value(args, 'pmfm_nm')

        key_val = {
            'pmfm_nm': pmfm_new
        }
        cls._write_to_kw(cls, cfg, serv_name, key_val, logger, cls.__name__)

        timeout = float(cls._cfg_val(cfg, 'ktl_timeout', 'default'))
        try:
            ktl.waitfor(f'{ktl_pmfm}={pmfm_new}', service=serv_name, timeout=timeout)
        except ktl.TimeoutException:
            msg = f'{cls.__name__} current pmfm {ktl.read(serv_name, ktl_pmfm)}' \
                  f',  timeout moving to {pmfm_new}.'
            if logger:
                logger.error(msg)
            raise DDOIKTLTimeOut(msg)

        return

    @classmethod
    def post_condition(cls, args, logger, cfg):
        """
        :param args:  <dict> The OB (or subset) in dictionary form
        :param logger: <DDOILoggerClient>, optional
            The DDOILoggerClient that should be used. If none is provided,
            defaults to a generic name specified in the config, by default None
        :param cfg: <class 'configparser.ConfigParser'> the config file parser.

        :return: None
        """
        return



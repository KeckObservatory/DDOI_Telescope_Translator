from ddoitranslatormodule.ddoiexceptions.DDOIExceptions import DDOIKTLTimeOut
from ddoi_telescope_translator.telescope_base import TelescopeBase

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
        :param cfg: <str> filepath, optional
            File path to the config that should be used, by default None

        :return: <ArgumentParser>
        """
        # read the config file
        cfg = cls._load_config(cfg)

        args_to_add = OrderedDict([
            ('pmfm', {'type': float,
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
        :param cfg: <str> filepath, optional
            File path to the config that should be used, by default None

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
        :param cfg: <str> filepath, optional
            File path to the config that should be used, by default None

        :return: None
        """
        serv_name = cls._config_param(cfg, 'ktl_serv', 'acs')
        ktl_pmfm = cls._config_param(cfg, 'ktl_kw_acs', 'pmfm')
        if args.get('print_only', False):
            current_pmfm = ktl.read(serv_name, ktl_pmfm)
            cls.write_msg(f"The current PMFM is {current_pmfm}")
            return

        pmfm_new = cls._get_arg_value(args, 'pmfm')

        key_val = {
            'pmfm': pmfm_new
        }
        cls._write_to_kw(cls, cfg, serv_name, key_val, logger, cls.__name__)

        timeout = cls._config_param(cfg, 'pmfm', 'timeout')
        try:
            ktl.waitfor(f'pmfm={pmfm_new}', service=serv_name, timeout=timeout)
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
        :param cfg: <str> filepath, optional
            File path to the config that should be used, by default None

        :return: None
        """
        return



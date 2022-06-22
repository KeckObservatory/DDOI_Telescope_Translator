from ddoitranslatormodule.BaseFunction import TranslatorModuleFunction

import tel_utils as utils


class PMFM(TranslatorModuleFunction):
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
        print_only = utils.print_only(args, cfg, 'tel_keys', ['pmfm_nm'])

        cls.serv_name = utils.config_param(cfg, 'ktl_serv', 'dcs')

        key_val = {
            '': ,
            '': ,
            '':
        }
        utils.write_to_kw(cfg, cls.serv_name, key_val, logger, cls.__name__)


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



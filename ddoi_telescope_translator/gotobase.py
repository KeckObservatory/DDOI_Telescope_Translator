from ddoi_telescope_translator.telescope_base import TelescopeBase


class GoToBase(TelescopeBase):
    """
    gotobase -- move the telescope to return to the base coordinates

    SYNOPSIS
        GoToBase.execute({})

    DESCRIPTION
        Return to the position previously marked as "base".

    RUN
        from ddoi_telescope_translator import gotobase
        gotobase.GoToBase.execute({})

    EXAMPLES
        1) return to the position marked as base:
            GoToBase.execute()

    KTL SERVICE & KEYWORDS
        servers: dcs
        keywords: raoff, decoff

    adapted from sh script: kss/mosfire/scripts/procs/tel/gotobase
    """

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
        cls.serv_name = cls._config_param(cfg, 'ktl_serv', 'dcs')

        key_val = {
            'ra_offset': 0.0,
            'dec_offset': 0.0,
            'relative_base': 't'
        }
        cls._write_to_kw(cls, cfg, cls.serv_name, key_val, logger, cls.__name__)


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





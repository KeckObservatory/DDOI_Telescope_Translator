from ddoi_telescope_translator.telescope_base import TelescopeBase

import ddoi_telescope_translator.tel_utils as utils


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
        cls.serv_name = utils.config_param(cfg, 'ktl_serv', 'dcs')

        key_val = {
            'ra_offset': 0.0,
            'dec_offset': 0.0,
            'relative_base': 't'
        }
        utils.write_to_kw(cfg, cls.serv_name, key_val, logger, cls.__name__)


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





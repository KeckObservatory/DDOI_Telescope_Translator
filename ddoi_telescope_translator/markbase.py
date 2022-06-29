from ddoitranslatormodule.BaseFunction import TranslatorModuleFunction

import ddoi_telescope_translator.tel_utils as utils


class MarkBase(TranslatorModuleFunction):
    """
    markbase -- set the base telescope coordinates to the current coordinates

    SYNOPSIS
        MarkBase.execute()

    DESCRIPTION
        Reset the telescope BASE corodinates to be the current
        coordinates of the telescope; i.e., reset the RA and Dec
        offsets to zero.  This might be useful when you are about to
        undertake and operation which will require numerous telescope moves
        and you want to be able to return to the starting position.
        In this case, use "markbase" before your first move, and then use
        "gotobase" to return to the starting position.

    ARGUMENTS

    OPTIONS

    EXAMPLES
        1) set the base coordinates to the current coordinates:
            MarkBase.execute()

    KTL SERVICE & KEYWORDS

    adapted from sh script: kss/mosfire/scripts/procs/tel/markbase
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
        serv_name = utils.config_param(cfg, 'ktl_serv', 'dcs')

        key_val = {
            'mark_base': 'true'
        }
        utils.write_to_kw(cfg, serv_name, key_val, logger, cls.__name__)

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



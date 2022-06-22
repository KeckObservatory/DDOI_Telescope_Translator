from ddoitranslatormodule.BaseFunction import TranslatorModuleFunction

import tel_utils as utils

import ktl


class SetPointingOriginName(TranslatorModuleFunction):
    """
    poname -- set or show the current pointing origin


    SYNOPSIS
        SetPointingOriginName.execute({'pointing_origin_name': ORIGIN})

    DESCRIPTION
        With no argument, prints the name of the currently selected
        pointing origin.  With one argument, reset the current
        pointing origin to the named value.

        Only functions when DEIMOS is in nighttime mode and can
        converse with the drive and control system (DCS) library.

    ARGUMENTS
        name = name of the pointing origin to select
    OPTIONS

    EXAMPLES
        1) show the current pointing origin
            SetPointingOriginName.execute()

        2) change the pointing origin to Slit:
            SetPointingOriginName.execute({'pointing_origin_name': SLIT})

    ENVIRONMENT VARIABLES

    FILES

    SERVERS & KEYWORDS
         dcs: poname
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
        serv_name = utils.config_param(cfg, 'ktl_serv', 'dcs')
        key_po_name = utils.config_param(cfg, 'ob_keys', 'pointing_origin_name')

        if utils.print_only(args, cfg, 'ob_keys', ['pointing_origin_name']):
            utils.write_msg(logger, ktl.read(serv_name, key_po_name))
            return

        key_val = {
            'pointing_origin_name': key_po_name,
            'pointing_origin_select': 1
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



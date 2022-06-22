from ddoitranslatormodule.BaseFunction import TranslatorModuleFunction

import tel_utils as utils
from en import OffsetEastNorth

import ktl


class OffsetBackFromNod(TranslatorModuleFunction):
    """
    fromsky - move the telescope from the sky position

    SYNOPSIS
        OffsetBackFromNod.execute()

    DESCRIPTION
        Move the telescope to the target position from the
            "sky" position designated by the nod parameters.
           Offset the telescope by minus the nod params.

    KTL SERVICE & KEYWORDS
        nodn, node

    adapted from sh script: kss/mosfire/scripts/procs/tel/fromsky
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
        inst = utils.get_inst_name(args, cls.__name__)
        serv_name = utils.config_param(cfg, 'ktl_serv', inst)

        key_east_offset = utils.config_param(cfg, 'ob_keys', 'tel_east_offset')
        key_north_offset = utils.config_param(cfg, 'ob_keys', 'tel_north_offset')

        kw_nodded_north = utils.config_param(cfg, f'ktl_kw_{inst}', 'noded_north')
        kw_nodded_east = utils.config_param(cfg, f'ktl_kw_{inst}', 'noded_east')

        nodded_north = ktl.read(serv_name, kw_nodded_north)
        nodded_east = ktl.read(serv_name, kw_nodded_east)

        OffsetEastNorth.execute({key_east_offset: -1.0 * nodded_east,
                                 key_north_offset: -1.0 * nodded_north})

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



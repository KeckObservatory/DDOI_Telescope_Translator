from ddoitranslatormodule.BaseFunction import TranslatorModuleFunction

import tel_utils as utils

import ktl
import math


class MarkCoords(TranslatorModuleFunction):
    """
    mark - stores current ra and dec offsets

    SYNOPSIS
        MarkCoords.execute({'inst': str of instrument name})

    DESCRIPTION
          stores the current ra and dec offsets for later use.
          Values stored in the KPF keywords: ??raoffset?? and ??decoffset??
          See also gomark

    ARGUMENTS

    OPTIONS

    EXAMPLES
    gomark

    ENVIRONMENT VARIABLES

    FILES

    SERVERS & KEYWORDS
       server: instrument, dcs
         keywords: raoffset, decoffset, raoff, decoff

    KTL SERVICE & KEYWORDS

    adapted from sh script: kss/mosfire/scripts/procs/tel/mark
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

        dcs_serv_name = utils.config_param(cfg, 'ktl_serv', 'dcs')

        # for precision read the raw (binary) versions -- in radians.
        kw_ra_offset = utils.config_param(cfg, 'ktl_kw_dcs', 'ra_offset')
        kw_dec_offset = utils.config_param(cfg, 'ktl_kw_dcs', 'dec_offset')

        current_ra_offset = ktl.read(dcs_serv_name, kw_ra_offset, binary=True)
        current_dec_offset = ktl.read(dcs_serv_name, kw_dec_offset, binary=True)

        current_ra_offset = current_ra_offset * 180.0 * 3600.0 / math.pi
        current_dec_offset = current_dec_offset * 180.0 * 3600.0 / math.pi

        # There is a bug in DCS where the value of RAOFF read back has been
        # divided by cos(Dec).  That is corrected here.

        kw_dec = utils.config_param(cfg, 'ktl_kw_dcs', 'declination')
        current_dec = ktl.read(dcs_serv_name, kw_dec, binary=True)
        current_ra_offset = current_ra_offset * math.cos(current_dec)

        inst_serv_name = utils.config_param(cfg, 'ktl_serv', inst)

        key_val = {
            'ra_mark': current_ra_offset,
            'dec_mark': current_dec_offset
        }
        utils.write_to_kw(cfg, inst_serv_name, key_val, logger, cls.__name__)


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



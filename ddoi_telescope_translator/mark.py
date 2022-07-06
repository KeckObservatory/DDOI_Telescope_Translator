from ddoi_telescope_translator.telescope_base import TelescopeBase

import ktl
import math


class MarkCoords(TelescopeBase):
    """
    mark - stores current ra and dec offsets

    SYNOPSIS
        MarkCoords.execute({'instrument': str of instrument name})

    RUN
        from ddoi_telescope_translator import mark
        mark.MarkCoords({})

    DESCRIPTION
          stores the current ra and dec offsets for later use.
          Values stored in the KPF keywords: ??raoffset?? and ??decoffset??
          See also gomark

    SERVERS & KEYWORDS
       server: instrument, dcs
         keywords: raoffset, decoffset, raoff, decoff

    KTL SERVICE & KEYWORDS

    adapted from sh script: kss/mosfire/scripts/procs/tel/mark
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

        # add inst parameter as optional
        parser = cls._add_inst_arg(cls, parser, cfg, is_req=False)

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
        inst = cls.get_inst_name(cls, args, cfg)

        dcs_serv_name = cls._config_param(cfg, 'ktl_serv', 'dcs')

        # for precision read the raw (binary) versions -- in radians.
        ktl_ra_offset = cls._config_param(cfg, 'ktl_kw_dcs', 'ra_offset')
        ktl_dec_offset = cls._config_param(cfg, 'ktl_kw_dcs', 'dec_offset')

        current_ra_offset = ktl.read(dcs_serv_name, ktl_ra_offset, binary=True)
        current_dec_offset = ktl.read(dcs_serv_name, ktl_dec_offset, binary=True)

        current_ra_offset = current_ra_offset * 180.0 * 3600.0 / math.pi
        current_dec_offset = current_dec_offset * 180.0 * 3600.0 / math.pi

        # There is a bug in DCS where the value of RAOFF read back has been
        # divided by cos(Dec).  That is corrected here.

        ktl_dec = cls._config_param(cfg, 'ktl_kw_dcs', 'declination')
        current_dec = ktl.read(dcs_serv_name, ktl_dec, binary=True)
        current_ra_offset = current_ra_offset * math.cos(current_dec)

        inst_serv_name = cls._config_param(cfg, 'ktl_serv', inst)

        key_val = {
            'ra_mark': current_ra_offset,
            'dec_mark': current_dec_offset
        }
        cls._write_to_kw(cls, cfg, inst_serv_name, key_val, logger, cls.__name__)


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

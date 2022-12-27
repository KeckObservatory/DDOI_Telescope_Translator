from ddoitranslatormodule.BaseTelescope import TelescopeBase

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
        :param cfg: <class 'configparser.ConfigParser'> the config file parser.

        :return: <ArgumentParser>
        """
        # read the config file
        cfg = cls._load_config(cls, cfg)

        parser.description = f'Stores current ra and dec offsets.  Modifies ' \
                             f'Instrument Specific keywords for RA/Dec mark.'

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
        inst = cls.get_inst_name(cls, args, cfg)

        # for precision read the raw (binary) versions -- in radians.
        current_ra_offset = ktl.read('dcs', 'raoff', binary=True)
        current_dec_offset = ktl.read('dcs', 'decoff', binary=True)

        current_ra_offset = current_ra_offset * 180.0 * 3600.0 / math.pi
        current_dec_offset = current_dec_offset * 180.0 * 3600.0 / math.pi

        # There is a bug in DCS where the value of RAOFF read back has been
        # divided by cos(Dec).  That is corrected here.
        current_dec = ktl.read('dcs', 'dec', binary=True)
        current_ra_offset = current_ra_offset * math.cos(current_dec)

        inst_serv_name = cls._cfg_val(cfg, 'ktl_serv', inst)

        # write to instrument keywords,  keys are cfg keys not ktl keys
        key_val = {
            'ra_mark': current_ra_offset,
            'dec_mark': current_dec_offset
        }
        cls._write_to_kw(cls, cfg, inst_serv_name, key_val, logger,
                         cls.__name__, cfg_key=True)


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

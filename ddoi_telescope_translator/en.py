from ddoitranslatormodule.ddoiexceptions.DDOIExceptions import DDOIPreConditionNotRun
from ddoitranslatormodule.BaseTelescope import TelescopeBase

import ddoi_telescope_translator.tel_utils as utils
from collections import OrderedDict


class OffsetEastNorth(TelescopeBase):
    """
    en -- move the telescope east and north

    SYNOPSIS
        OffsetEastNorth.execute({'tcs_offset_east': 10.0,  'tcs_offset_north': 5.0})

    RUN
        from ddoi_telescope_translator import en
        en.OffsetEastNorth.execute({'tcs_offset_east': 10.0,  'tcs_offset_north': 5.0})

    DESCRIPTION
        Move the telescope the given number of arcsec EAST & NORTH
        relative to its current position

    ARGUMENTS
        offset = number of arcseconds to move EAST/NORTH; negative
        values indicate WEST/SOUTH movement

     EXAMPLES
        1) Move the telescope east by 10 arcsec:
            OffsetEastNorth.execute({tcs_offset_east: 10.0,  tcs_offset_north: 0.0})
        2) Move the telescope west and north by 10 arcsec:
            OffsetEastNorth.execute({tcs_offset_east: 0.0,  tcs_offset_north: 10.0})

     KTL SERVICE & KEYWORDS
          servers: dcs
             keywords: raoff, decoff

    adapted from sh script: kss/mosfire/scripts/procs/tel/en
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

        # add the command line description
        parser.description = f'Moves telescope X,Y arcseconds East and North.' \
                             f' Modifies KTL DCS Keyword: RAOFF, DECOFF.'

        cls.key_east_offset = cls._cfg_val(cfg, 'ob_keys', 'tel_east_offset')
        cls.key_north_offset = cls._cfg_val(cfg, 'ob_keys', 'tel_north_offset')

        args_to_add = OrderedDict([
            (cls.key_east_offset, {'type': float,
                                   'help': 'The offset East in arcseconds.'}),
            (cls.key_north_offset, {'type': float,
                                    'help': 'The offset North in arcseconds.'})
            ])

        parser = cls._add_args(parser, args_to_add, print_only=False)

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
        if not hasattr(cls, 'key_east_offset'):
            cls.key_east_offset = cls._cfg_val(cfg, 'ob_keys',
                                                    'tel_east_offset')
        if not hasattr(cls, 'key_north_offset'):
            cls.key_north_offset = cls._cfg_val(cfg, 'ob_keys',
                                                     'tel_north_offset')

        cls.east_off = cls._get_arg_value(args, cls.key_east_offset)
        cls.north_off = cls._get_arg_value(args, cls.key_north_offset)

        if utils.check_for_zero_offsets(cls.east_off, cls.north_off):
            return False

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
        if not hasattr(cls, 'east_off'):
            raise DDOIPreConditionNotRun(cls.__name__)

        # the ktl key name to modify and the value
        key_val = {
            'raoff': cls.east_off,
            'decoff': cls.north_off,
            'rel2curr': 't'
        }
        cls._write_to_kw(cls, cfg, 'dcs', key_val, logger, cls.__name__)

        return

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
        utils.wait_for_cycle(cls, cfg, 'dcs', logger)

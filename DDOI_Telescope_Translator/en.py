from ddoitranslatormodule.BaseFunction import TranslatorModuleFunction
from ddoitranslatormodule.ddoiexceptions.DDOIExceptions import DDOIPreConditionNotRun

import tel_utils as utils


class OffsetEastNorth(TranslatorModuleFunction):
    """
    en -- move the telescope east and north

    SYNOPSIS
        OffsetEastNorth.execute({key_east_offset: 10.0,  key_north_offset: 5.0})

    DESCRIPTION
        Move the telescope the given number of arcsec EAST & NORTH
        relative to its current position

    ARGUMENTS
        offset = number of arcseconds to move EAST/NORTH; negative
        values indicate WEST/SOUTH movement

     EXAMPLES
        1) Move the telescope east by 10 arcsec:
            OffsetEastNorth.execute({key_east_offset: 10.0,  key_north_offset: 0.0})
        2) Move the telescope west and north by 10 arcsec:
            OffsetEastNorth.execute({key_east_offset: 0.0,  key_north_offset: 10.0})

     KTL SERVICE & KEYWORDS
          servers: dcs
             keywords: raoff, decoff

    adapted from sh script: kss/mosfire/scripts/procs/tel/en
    """

    @classmethod
    def add_cmdline_args(cls, parser, cfg):
        """
        The arguments to add to the command line interface.

        :param parser: <ArgumentParser>
            the instance of the parser to add the arguments to .
        :param cfg: <str> filepath, optional
            File path to the config that should be used, by default None

        :return: <ArgumentParser>
        """
        cls.key_east_offset = utils.config_param(cfg, 'ob_keys', 'tel_east_offset')
        cls.key_north_offset = utils.config_param(cfg, 'ob_keys', 'tel_north_offset')

        args_to_add = {
            cls.key_east_offset: {'type': float, 'req': True,
                                  'help': 'The offset East in arcseconds.'},
            cls.key_north_offset: {'type': float, 'req': True,
                                   'help': 'The offset North in arcseconds.'}}
        parser = utils.add_args(parser, args_to_add, print_only=False)

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
        if not hasattr(cls, 'key_east_offset'):
            cls.key_east_offset = utils.config_param(cfg, 'ob_keys',
                                                     'tel_east_offset')
        if not hasattr(cls, 'key_north_offset'):
            cls.key_north_offset = utils.config_param(cfg, 'ob_keys',
                                                      'tel_north_offset')

        cls.east_off = utils.get_arg_value(args, cls.key_east_offset, logger)
        cls.north_off = utils.get_arg_value(args, cls.key_north_offset, logger)

        if utils.check_for_zero_offsets(cls.east_off, cls.north_off, logger):
            return False

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
        if not hasattr(cls, 'east_off'):
            raise DDOIPreConditionNotRun(cls.__name__)

        cls.serv_name = utils.config_param(cfg, 'ktl_serv', 'dcs')

        key_val = {
            'ra_offset': cls.east_off,
            'dec_offset': cls.north_off,
            'relative_current': 't'
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
        utils.wait_for_cycle(cfg, cls.serv_name, logger)

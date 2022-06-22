from ddoitranslatormodule.BaseFunction import TranslatorModuleFunction
from ddoitranslatormodule.DDOIExceptions import DDOIPreConditionNotRun

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
        key_east_offset = utils.config_param(cfg, 'ob_keys', 'tel_east_offset')
        key_north_offset = utils.config_param(cfg, 'ob_keys', 'tel_north_offset')

        cls.east_off = utils.check_float(args, key_east_offset, logger)
        cls.north_off = utils.check_float(args, key_north_offset, logger)

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
        cls.auto_resume = utils.read_auto_resume_val(cfg, cls.serv_name)

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




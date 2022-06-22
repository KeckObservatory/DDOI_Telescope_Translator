from ddoitranslatormodule.BaseFunction import TranslatorModuleFunction
from ddoitranslatormodule.DDOIExceptions import DDOIPreConditionNotRun

import tel_utils as utils

from time import sleep


class OffsetAzEl(TranslatorModuleFunction):
    """
    azel -- move the telescope x arcsec in azimuth and y arcsec in elevation

    SYNOPSIS
        OffsetAzEl.execute({'inst_az_offset': 10.0,  'inst_el_offset': 5.0})

    DESCRIPTION
        Move the telescope the given number of arcseconds in the
        azimuth and elevation directions.

    DICTIONARY KEYS
        inst_az_offset = distance to move in azimuth [arcsec]
        inst_el_offset = distance to move in elevation [arcsec]

     KTL SERVICE & KEYWORDS
         service = dcs
              keywords: azoff, rel2curr, axestat, autresum

    adapted from sh script: kss/mosfire/scripts/procs/tel/azel
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
        key_az_offset = utils.config_param(cfg, 'ob_keys', 'az_offset')
        key_el_offset = utils.config_param(cfg, 'ob_keys', 'el_offset')

        cls.az_off = utils.check_float(args, key_az_offset, logger)
        cls.el_off = utils.check_float(args, key_el_offset, logger)

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
        if not hasattr(cls, 'az_off'):
            raise DDOIPreConditionNotRun(cls.__name__)

        cls.serv_name = utils.config_param(cfg, 'ktl_serv', 'dcs')

        key_val = {
            'az_offset': cls.az_off,
            'el_offset': cls.el_off,
            'relative_current': 't'
        }
        utils.write_to_kw(cfg, cls.serv_name, key_val, logger, cls.__name__)

        sleep(3)

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




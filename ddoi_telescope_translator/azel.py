from ddoitranslatormodule.BaseFunction import TranslatorModuleFunction
from ddoitranslatormodule.ddoiexceptions.DDOIExceptions import DDOIPreConditionNotRun

import ddoi_telescope_translator.tel_utils as utils

from time import sleep


class OffsetAzEl(TranslatorModuleFunction):
    """
    azel -- move the telescope x arcsec in azimuth and y arcsec in elevation

    SYNOPSIS
        OffsetAzEl.execute({'tcs_offset_az': 10.0,  'tcs_offset_el': 5.0})

    DESCRIPTION
        Move the telescope the given number of arcseconds in the
        azimuth and elevation directions.

    DICTIONARY KEYS
        tcs_offset_az = distance to move in azimuth [arcsec]
        tcs_offset_el = distance to move in elevation [arcsec]

     KTL SERVICE & KEYWORDS
         service = dcs
              keywords: azoff, rel2curr, axestat, autresum

    adapted from sh script: kss/mosfire/scripts/procs/tel/azel
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
        cls.key_az_offset = utils.config_param(cfg, 'ob_keys', 'az_offset')
        cls.key_el_offset = utils.config_param(cfg, 'ob_keys', 'el_offset')

        args_to_add = {
            cls.key_az_offset: {'type': float, 'req': True,
                                'help': 'The offset in Azimuth in degrees.'},
            cls.key_el_offset: {'type': float, 'req': True,
                                'help': 'The offset in Elevation in degrees.'}
        }
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
        if not hasattr(cls, 'key_az_offset'):
            cls.key_az_offset = utils.config_param(cfg, 'ob_keys', 'az_offset')
        if not hasattr(cls, 'key_el_offset'):
            cls.key_el_offset = utils.config_param(cfg, 'ob_keys', 'el_offset')

        print(f'args {args}')
        cls.az_off = utils.get_arg_value(args, cls.key_az_offset, logger)
        cls.el_off = utils.get_arg_value(args, cls.key_el_offset, logger)

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

from ddoitranslatormodule.ddoiexceptions.DDOIExceptions import DDOIPreConditionNotRun
from ddoitranslatormodule.BaseTelescope import TelescopeBase

import ddoi_telescope_translator.tel_utils as utils

from time import sleep
from collections import OrderedDict


class OffsetAzEl(TelescopeBase):
    """
    azel -- move the telescope x arcsec in azimuth and y arcsec in elevation

    SYNOPSIS
        OffsetAzEl.execute({'tcs_offset_az': 10.0,  'tcs_offset_el': 5.0})

    RUN
        from ddoi_telescope_translator import azel
        azel.OffsetAzEl.execute({'tcs_offset_az': 0.0, 'tcs_offset_el': 0.0})

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

        cls.key_az_offset = cls._cfg_val(cfg, 'ob_keys', 'az_offset')
        cls.key_el_offset = cls._cfg_val(cfg, 'ob_keys', 'el_offset')

        args_to_add = OrderedDict([
            (cls.key_az_offset, {'type': float,
                                 'help': 'The offset in Azimuth in arcseconds.'}),
            (cls.key_el_offset, {'type': float,
                                 'help': 'The offset in Elevation in arcseconds.'}),
            ('rel_current', {'type': bool, 'kw_arg': True,
                             'help': 'True if offset is relative to current position.'})
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
        if not hasattr(cls, 'key_az_offset'):
            cls.key_az_offset = cls._cfg_val(cfg, 'ob_keys', 'az_offset')
        if not hasattr(cls, 'key_el_offset'):
            cls.key_el_offset = cls._cfg_val(cfg, 'ob_keys', 'el_offset')

        cls.az_off = cls._get_arg_value(args, cls.key_az_offset)
        cls.el_off = cls._get_arg_value(args, cls.key_el_offset)

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
        if not hasattr(cls, 'az_off'):
            raise DDOIPreConditionNotRun(cls.__name__)

        cls.serv_name = cls._cfg_val(cfg, 'ktl_serv', 'dcs')

        key_val = {
            'az_offset': cls.az_off,
            'el_offset': cls.el_off,
            'relative_current': 't'
        }
        cls._write_to_kw(cls, cfg, cls.serv_name, key_val, logger, cls.__name__)

        sleep(3)

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
        utils.wait_for_cycle(cls, cfg, cls.serv_name, logger)

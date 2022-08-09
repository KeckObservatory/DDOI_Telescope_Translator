from ddoitranslatormodule.ddoiexceptions.DDOIExceptions import DDOIPreConditionNotRun
from ddoitranslatormodule.BaseTelescope import TelescopeBase

import ddoi_telescope_translator.tel_utils as utils
from collections import OrderedDict


class OffsetGuiderCoordXY(TelescopeBase):
    """
    gxy -- move the telescope in GUIDER coordinates

    SYNOPSIS
        OffsetGuiderCoordXY.execute({'guider_offset_x': 0.0, 'guider_offset_y': 1.0})

    RUN
        from ddoi_telescope_translator import gxy
        gxy.OffsetGuiderCoordXY.execute({'guider_offset_x': 0.0, 'guider_offset_y': 1.0})

    Purpose:
        Offset the telescope by the given number of arcseconds in the
        guider coordinate system, which is rotated 180 degrees relative
        to the DEIMOS coordinate system.

    ARGUMENTS
        guider_x_offset = offset in the direction parallel with guider rows [arcsec]
        guider_y_offset = offset in the direction parallel with guider columns [arcsec]

    OPTIONS

    KTL SERVICE & KEYWORDS
        servers: dcs
          keywords: tvxoff, tvyoff

    adapted from sh script: kss/mosfire/scripts/procs/tel/telfoc

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

        cls.key_x_offset = cls._config_param(cfg, 'ob_keys', 'guider_x_offset')
        cls.key_y_offset = cls._config_param(cfg, 'ob_keys', 'guider_y_offset')

        parser = cls._add_inst_arg(cls, parser, cfg)

        args_to_add = OrderedDict([
            (cls.key_x_offset, {
                'type': float,
                'help': 'The offset in Guider X offset in pixels.'
            }),
            (cls.key_y_offset, {
                'type': float,
                'help': 'The offset in Guider Y offset in pixels.'
            })
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
        key_x_offset = cls._config_param(cfg, 'ob_keys', 'guider_x_offset')
        key_y_offset = cls._config_param(cfg, 'ob_keys', 'guider_y_offset')

        cls.x_off = cls._get_arg_value(args, key_x_offset)
        cls.y_off = cls._get_arg_value(args, key_y_offset)

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
        if not hasattr(cls, 'x_off'):
            raise DDOIPreConditionNotRun(cls.__name__)

        cls.serv_name = cls._config_param(cfg, 'ktl_serv', 'dcs')

        key_val = {
            'guider_x_offset': cls.x_off,
            'guider_y_offset': cls.y_off,
            'relative_current': 't'
        }
        cls._write_to_kw(cls, cfg, cls.serv_name, key_val, logger, cls.__name__)


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
        utils.wait_for_cycle(cls._config_param, cfg, cls.serv_name, logger)


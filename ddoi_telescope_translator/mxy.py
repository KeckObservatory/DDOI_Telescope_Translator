from ddoitranslatormodule.ddoiexceptions.DDOIExceptions import DDOIPreConditionNotRun
from ddoitranslatormodule.BaseTelescope import TelescopeBase

import ddoi_telescope_translator.tel_utils as utils

from collections import OrderedDict


class OffsetXY(TelescopeBase):
    """
    offset telescope in instrument (detector) coordinates

    SYNOPSIS
        OffsetXY.execute({'inst_offset_x': x, 'inst_offset_y': y})

    DESCRIPTION
        Offset the telescope a given number of arcsec in the
        coordinate system of the detector.  The offset is
        relative to the current coordinates by default

    ARGUMENTS
        inst_offset_x = offset in the direction parallel with CCD rows [arcsec]
        inst_offset_y = offset in the direction parallel with CCD columns [arcsec]

    EXAMPLE
        1) Move telecope 10 arcsec along rows and -20 arcsec along columns:
            OffsetXY.execute({'inst_offset_x': 10, 'inst_offset_y': -20})

        Note that since this is a *telescope* move, the target will
        "move" in the OPPOSITE direction!

    KTL SERVICE & KEYWORDS
         service = dcs
              keywords: instxoff, instyoff

    adapted from kss/mosfire/scripts/procs/tel/mxy
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

        cls.key_x_offset = cls._config_param(cfg, 'ob_keys', 'inst_x_offset')
        cls.key_y_offset = cls._config_param(cfg, 'ob_keys', 'inst_y_offset')

        parser = cls._add_inst_arg(cls, parser, cfg)

        args_to_add = OrderedDict([
            (cls.key_x_offset, {
                'type': float,
                'help': 'The offset in the direction parallel to CCD rows [arcsec]'
            }),
            (cls.key_y_offset, {
                'type': float,
                'help': 'The offset in the direction perpendicular to CCD columns [arcsec]'
            })
        ])
        parser = cls._add_args(parser, args_to_add, print_only=False)

        return super().add_cmdline_args(parser, cfg)

    @classmethod
    def pre_condition(cls, args, logger, cfg):
        """
        :param args:  <dict> The OB (or subset) in dictionary form.
            required: inst_x_offset, inst_y_offset
        :param logger: <DDOILoggerClient>, optional
            The DDOILoggerClient that should be used. If none is provided,
            defaults to a generic name specified in the config, by default None
        :param cfg: <class 'configparser.ConfigParser'> the config file parser.

        :return: bool
        """
        cls.inst = cls.get_inst_name(cls, args, cfg)

        if not hasattr(cls, 'key_x_offset'):
            cls.key_x_offset = cls._config_param(cfg, 'ob_keys', 'inst_x_offset')
        if not hasattr(cls, 'key_y_offset'):
            cls.key_y_offset = cls._config_param(cfg, 'ob_keys', 'inst_y_offset')

        cls.x_offset = cls._get_arg_value(args, cls.key_x_offset)
        cls.y_offset = cls._get_arg_value(args, cls.key_y_offset)

        if utils.check_for_zero_offsets(cls.x_offset, cls.y_offset):
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
        if not hasattr(cls, 'x_offset'):
            raise DDOIPreConditionNotRun(cls.__name__)

        cls.serv_name = cls._config_param(cfg, 'ktl_serv', 'dcs')

        det_u, det_v = utils.transform_detector(cls._config_param, cfg,
                                                cls.write_msg, cls.x_offset,
                                                cls.y_offset, cls.inst)

        key_val = {
            'inst_x_offset': det_u,
            'inst_y_offset': det_v,
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

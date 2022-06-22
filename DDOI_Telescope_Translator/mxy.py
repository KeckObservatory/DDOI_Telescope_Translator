from ddoitranslatormodule.BaseFunction import TranslatorModuleFunction
from ddoitranslatormodule.DDOIExceptions import DDOIPreConditionNotRun

import tel_utils as utils

import ktl
import math


class OffsetXY(TranslatorModuleFunction):
    """
    offset telescope in instrument (detector) coordinates

    SYNOPSIS
        OffsetXY.execute({'inst_x_offset': x, 'inst_y_offset': y,
                          'inst': str of instrument name})

    DESCRIPTION
        Offset the telescope a given number of arcsec in the
        coordinate system of the detector.  The offset is
        relative to the current coordinates by default

    ARGUMENTS
        x_offset = offset in the direction parallel with CCD rows [arcsec]
        y_offset = offset in the direction parallel with CCD columns [arcsec]

    EXAMPLE
        1) Move telecope 10 arcsec along rows and -20 arcsec along columns:
            OffsetXY.execute({'inst_x_offset': 10, 'inst_y_offset': -20,
            'inst': 'KPF'})

        Note that since this is a *telescope* move, the target will
        "move" in the OPPOSITE direction!

    KTL SERVICE & KEYWORDS
         service = dcs
              keywords: instxoff, instyoff

    adapted from kss/mosfire/scripts/procs/tel/mxy
    """

    @classmethod
    def pre_condition(cls, args, logger, cfg):
        """
        :param args:  <dict> The OB (or subset) in dictionary form.
            required: inst_x_offset, inst_y_offset
        :param logger: <DDOILoggerClient>, optional
            The DDOILoggerClient that should be used. If none is provided,
            defaults to a generic name specified in the config, by default None
        :param cfg: <str> filepath, optional
            File path to the config that should be used, by default None

        :return: bool
        """
        cls.inst = utils.get_inst_name(args, cls.__name__)

        key_x_offset = utils.config_param(cfg, 'ob_keys', 'inst_x_offset')
        key_y_offset = utils.config_param(cfg, 'ob_keys', 'inst_y_offset')

        cls.x_offset = utils.check_float(args, key_x_offset, logger)
        cls.y_offset = utils.check_float(args, key_y_offset, logger)

        if utils.check_for_zero_offsets(cls.x_offset, cls.y_offset, logger):
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
        if not hasattr(cls, 'x_offset'):
            raise DDOIPreConditionNotRun(cls.__name__)

        cls.serv_name = utils.config_param(cfg, 'ktl_serv', 'dcs')

        det_u, det_v = cls.transform_detector(cfg, cls.x_offset,
                                              cls.y_offset, cls.inst)

        key_val = {
            'inst_x_offset': det_u,
            'inst_y_offset': det_v,
            'relative_current': 't'}
        utils.write_to_kw(cfg, cls.serv_name, key_val, logger, cls.__name__)

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

    @staticmethod
    def transform_detector(cfg, x, y, inst):
        det_ang = utils.config_param(cfg, f'{inst}_parameters', 'det_angle')

        det_u = x * math.cos(det_ang) + y * math.sin(det_ang)
        det_v = y * math.cos(det_ang) - x * math.sin(det_ang)

        return det_u, det_v


from ddoitranslatormodule.BaseFunction import TranslatorModuleFunction
from ddoitranslatormodule.ddoiexceptions.DDOIExceptions import DDOIPreConditionNotRun

import ddoi_telescope_translator.tel_utils as utils
from ddoi_telescope_translator.mxy import OffsetXY

import ktl
import argparse
from collections import OrderedDict


class MovePixelXY(TranslatorModuleFunction):
    """
    pxy -- move telescope in pixel coordinates of the DEIMOS detector

    SYNOPSIS
        MovePixelXY.execute({'inst_offset_xpix': float,
                             'inst_offset_ypix': float,
                             'instrument': str of instrument name})

    DESCRIPTION
        Move the telescope a given number of pixels in the "x" and "y"
        directions as defined by the DEIMOS detector.

    Arguments:
        inst_offset_xpix = offset in the direction parallel with CCD rows [pixels]
        inst_offset_ypix = offset in the direction parallel with CCD columns [pixels]

    EXAMPLES:
        1) Move the telescope 100 pixels in "x" and -200 in "y":
            MovePixelXY.execute({'inst_offset_xpix': 100.0,
                                 'inst_offset_ypix': -200.0,
                                 'instrument': INST})

        Note that since this is a *telescope* move, the target will
        "move" in the OPPOSITE direction!

    KTL SERVICE & KEYWORDS
        service = instrument
             keywords: sfilter/ifilter, sscale

    adapted from sh script: kss/mosfire/scripts/procs/tel/pxy
    """

    @classmethod
    def add_cmdline_args(cls, parser, cfg=None):
        """
        The arguments to add to the command line interface.

        :param parser: <ArgumentParser>
            the instance of the parser to add the arguments to .
        :param cfg: <str> filepath, optional
            File path to the config that should be used, by default None

        :return: <ArgumentParser>
        """
        # read the config file
        cfg = cls._load_config(cfg)

        cls.key_x_offset = utils.config_param(cfg, 'tel_keys', 'inst_offset_xpix')
        cls.key_y_offset = utils.config_param(cfg, 'tel_keys', 'inst_offset_ypix')

        args_to_add = OrderedDict([
            (cls.key_x_offset, {'type': float,
                                'help': 'The Instrument X offset in pixels.'}),
            (cls.key_y_offset, {'type': float,
                                'help': 'The Instrument Y offset in pixels.'})
        ])
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
        cls.inst = utils.get_inst_name(args, cls.__name__)

        if not hasattr(cls, 'key_x_offset'):
            cls.key_x_offset = utils.config_param(cfg, 'tel_keys', 'inst_offset_xpix')
        if not hasattr(cls, 'key_y_offset'):
            cls.key_y_offset = utils.config_param(cfg, 'tel_keys', 'inst_offset_ypix')

        cls.x_offset = utils.get_arg_value(args, cls.key_x_offset, logger)
        cls.y_offset = utils.get_arg_value(args, cls.key_y_offset, logger)

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

        serv_name = utils.config_param(cfg, 'ktl_serv', cls.inst)
        ktl_pixel_scale = utils.config_param(cfg, f'ktl_kw_{cls.inst}',
                                            'pixel_scale')
        pixel_scale = ktl.read(serv_name, ktl_pixel_scale)

        dx = pixel_scale * cls.x_offset
        dy = pixel_scale * cls.y_offset

        key_x_offset = utils.config_param(cfg, 'ob_keys', 'inst_x_offset')
        key_y_offset = utils.config_param(cfg, 'ob_keys', 'inst_y_offset')

        OffsetXY.execute({key_x_offset: dx, key_y_offset: dy}, cfg=cfg)


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
        return



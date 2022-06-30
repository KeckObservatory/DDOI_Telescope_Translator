from ddoitranslatormodule.BaseFunction import TranslatorModuleFunction
from ddoitranslatormodule.ddoiexceptions.DDOIExceptions import DDOIDetectorAngleUndefined

from ddoi_telescope_translator import tel_utils as utils
from ddoi_telescope_translator.mxy import OffsetXY

import math
from collections import OrderedDict


class MoveAlongSlit(TranslatorModuleFunction):
    """
    sltmov -- move object along the slit direction in arcsec

    SYNOPSIS
        MoveAlongSlit.execute({'inst_offset_det': float, 'instrument': INST})

    DESCRIPTION
        Move the telescope the given number of arcseconds along the
        slit.  A positive value will "move" the object "down" (i.e., to
        a smaller y pixel value).

    ARGUMENTS
          inst_offset_y - number of arcsec to offset object.

    EXAMPLES
        MoveAlongSlit.execute({'inst_offset_det': 10.0, 'instrument': 'KPF'})
             moves object 10 arcsec in y to more positive y values

    adapted from sh script: kss/mosfire/scripts/procs/tel/slitmov
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

        cls.key_slit_offset = utils.config_param(cfg, 'ob_keys', 'inst_slit_offset')

        parser = utils.add_inst_arg(parser, cfg)

        args_to_add = OrderedDict([
            (cls.key_slit_offset, {'type': float,
                                  'help': 'The number of arcseconds to offset '
                                          'object along the slit.'})
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
        if not hasattr(cls, 'key_slit_offset'):
            cls.key_slit_offset = utils.config_param(cfg, 'ob_keys', 'inst_slit_offset')

        slit_offset = utils.get_arg_value(args, cls.key_slit_offset, logger)

        inst = utils.get_inst_name(args, cls.__name__)
        det_angle = utils.config_param(cfg, f'{inst}_parameters', 'det_angle')

        try:
            det_angle = float()
        except (ValueError, TypeError):
            msg = 'ERROR, could not determine detector angle'
            raise DDOIDetectorAngleUndefined(msg)

        dx = slit_offset * math.sin(math.radians(det_angle))
        dy = slit_offset * math.cos(math.radians(det_angle))

        cls.serv_name = utils.config_param(cfg, 'ktl_serv', 'dcs')

        # run mxy with the calculated offsets
        key_x_offset = utils.config_param(cfg, 'ob_keys', 'inst_x_offset')
        key_y_offset = utils.config_param(cfg, 'ob_keys', 'inst_y_offset')
        OffsetXY.execute({key_x_offset: dx, key_y_offset: dy,
                          'instrument': inst}, cfg=cfg)

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
        return

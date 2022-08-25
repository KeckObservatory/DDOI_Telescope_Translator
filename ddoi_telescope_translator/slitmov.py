from ddoitranslatormodule.ddoiexceptions.DDOIExceptions import DDOIDetectorAngleUndefined
from ddoitranslatormodule.BaseTelescope import TelescopeBase

from ddoi_telescope_translator.mxy import OffsetXY

import math
from collections import OrderedDict


class MoveAlongSlit(TelescopeBase):
    """
    sltmov -- move object along the slit direction in arcsec

    SYNOPSIS
        MoveAlongSlit.execute({'inst_offset_det': float, 'instrument': INST})

    RUN
        from ddoi_telescope_translator import slitmov
        slitmov.MoveAlongSlit.execute({'inst_offset_det': 10.0, 'instrument': 'KPF'})

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
        :param cfg: <class 'configparser.ConfigParser'> the config file parser.

        :return: <ArgumentParser>
        """
        # read the config file
        cfg = cls._load_config(cls, cfg)

        cls.key_slit_offset = cls._cfg_val(cfg, 'ob_keys',
                                                'inst_slit_offset')

        parser = cls._add_inst_arg(cls, parser, cfg)

        args_to_add = OrderedDict([
            (cls.key_slit_offset, {
                'type': float,
                'help': 'The number of arcseconds to offset object along the slit.'
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
        if not hasattr(cls, 'key_slit_offset'):
            cls.key_slit_offset = cls._cfg_val(cfg, 'ob_keys',
                                                    'inst_slit_offset')

        slit_offset = cls._get_arg_value(args, cls.key_slit_offset)

        inst = cls.get_inst_name(cls, args, cfg)

        # TODO
        det_angle = cls._cfg_val(cfg, f'{inst}_parameters', 'det_angle')

        try:
            det_angle = float()
        except (ValueError, TypeError):
            msg = 'ERROR, could not determine detector angle'
            raise DDOIDetectorAngleUndefined(msg)

        dx = slit_offset * math.sin(math.radians(det_angle))
        dy = slit_offset * math.cos(math.radians(det_angle))

        cls.serv_name = cls._cfg_val(cfg, 'ktl_serv', 'dcs')

        # run mxy with the calculated offsets
        key_x_offset = cls._cfg_val(cfg, 'ob_keys', 'inst_x_offset')
        key_y_offset = cls._cfg_val(cfg, 'ob_keys', 'inst_y_offset')
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
        :param cfg: <class 'configparser.ConfigParser'> the config file parser.

        :return: None
        """
        return

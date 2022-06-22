from ddoitranslatormodule.BaseFunction import TranslatorModuleFunction
from ddoitranslatormodule.DDOIExceptions import DDOIPreConditionNotRun

import tel_utils as utils
from mxy import OffsetXY


class MoveP1ToP2(TranslatorModuleFunction):
    """
      mov -- move an object to a given position on the detector

    SYNOPSIS:
        MoveP1ToP2.execute({'inst_x1': float, 'inst_y1: float,
                            'inst_x2': float, 'inst_y2: float,
                            'inst': inst name string})

    DESCRIPTION
        Given the starting pixel coordinates of an object on a
        DEIMOS image, and destination coordinates, compute and apply the
        required telescope move the object as desired.

    ARGUMENTS:
        inst_x1 = starting column location of object [pixels]
        inst_y1 = starting row location of object [pixels]
        inst_x2 = ending column location of object [pixels]
        inst_y2 = ending row location of object [pixels]
        inst = the instrument name (str)

    OPTIONS
         none

    EXAMPLE:
        1) Move a target at pixel (100,200) to pixel (300,400):

            MoveP1ToP2.execute({'inst_x1': 100, 'inst_y1: 200,
                                'inst_x2': 300, 'inst_y2: 400, 'inst': KPF})

        2) Display the telescope move required to shift a target at
        pixel (100,200) to the pixel (300,400) without moving the telecope:

            MoveP1ToP2.execute('inst': KPF)

    SCRIPTS CALLED
        mxy

    adapted from sh script: kss/mosfire/scripts/procs/tel/mov
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
        cls.inst = utils.get_inst_name(args, cls.__name__)

        tel_key_list = ['inst_x1', 'inst_y1', 'inst_x2', 'inst_y2']
        cls.print_only = utils.print_only(args, cfg, 'tel_keys', tel_key_list)
        if cls.print_only:
            return True

        cls.coords = {}
        for tel_key in tel_key_list:
            key_inst = utils.config_param(cfg, 'tel_keys', tel_key)
            cls.coords[tel_key] = utils.check_float(args, key_inst, logger)

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
        if not hasattr(cls, 'print_only'):
            raise DDOIPreConditionNotRun(cls.__name__)

        cls.inst_serv_name = utils.config_param(cfg, 'ktl_serv', cls.inst)
        pixel_scale = utils.config_param(cfg, f'ktl_kw_{cls.inst}', 'pixel_scale')

        dx = pixel_scale * (cls.coords['inst_x1'] - cls.coords['inst_x2'])
        dy = pixel_scale * (cls.coords['inst_y1'] - cls.coords['inst_y2'])

        if cls.print_only:
            print(f"Required shift is X: {dx} Y: {dy}")
            return

        key_x_offset = utils.config_param(cfg, 'tel_keys', 'inst_x_offset')
        key_y_offset = utils.config_param(cfg, 'tel_keys', 'inst_y_offset')
        OffsetXY.execute({key_x_offset: dx, key_y_offset: dy})

        msg = f"Moving target from pixel: ({cls.coords['inst_x1']}," \
              f"{cls.coords['inst_y1']}) to ({cls.coords['inst_x1']}," \
              f"{cls.coords['inst_y1']}),  magnitude X: {dx} Y: {dy}"

        utils.write_msg(logger, msg)

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



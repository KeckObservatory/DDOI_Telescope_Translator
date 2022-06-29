from ddoitranslatormodule.BaseFunction import TranslatorModuleFunction
from ddoitranslatormodule.ddoiexceptions.DDOIExceptions import DDOIPreConditionNotRun

import tel_utils as utils
from gxy import OffsetGuiderCoordXY

import ktl


class MoveToGuiderCenter(TranslatorModuleFunction):
    """
    gcent -- move an object to the center of the guider pick off mirror

    SYNOPSIS
        MoveGuiderCenter.execute({'inst_x1': float, 'inst_y1': float,
                                 'instrument': INST})

    DESCRIPTION
        Given the pixel coordinates of an object on a DEIMOS guider image,
        compute and apply the required telescope move to bring the
        object to the center of the field of view for the DEIMOS TV
        guider pickoff mirror (pixel coordinates x=512, y=800).

    ARGUMENTS
        print_only = no move, only print the required shift
        inst_x1 = column location of object [pixels]
        inst_y1 = row location of object [pixels]

    OPTIONS

    EXAMPLES
        1) Move a target at pixel (100,200) to the pickoff mirror center:
            MoveGuiderCenter.execute({'det_x_pix': 100.0, 'det_y_pix': 200.0,
                                      'instrument': INST})

        2) Display the telescope move required to shift a target at
        pixel (100,200) to the pickoff mirror center, without
        actually performing the move:
            MoveGuiderCenter.execute({'det_x_pix': 100.0, 'det_y_pix': 200.0,
                                      'instrument': INST, 'print_only': 1}

    KTL SERVICE & KEYWORDS

    adapted from sh script: kss/mosfire/scripts/procs/tel/gcent
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
        cls.key_inst_x = utils.config_param(cfg, 'tel_keys', 'inst_x1')
        cls.key_inst_y = utils.config_param(cfg, 'tel_keys', 'inst_y1')

        parser = utils.add_inst_arg(parser, cfg)

        args_to_add = {
            cls.key_inst_x: {'type': float, 'req': True,
                             'help': 'The X pixel position to move to guider center.'},
            cls.key_inst_y: {'type': float, 'req': True,
                             'help': 'The Y pixel position to move to guider center.'}}
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
        if not hasattr(cls, 'key_inst_x'):
            cls.key_inst_x = utils.config_param(cfg, 'tel_keys', 'inst_x1')
        if not hasattr(cls, 'key_inst_y'):
            cls.key_inst_y = utils.config_param(cfg, 'tel_keys', 'inst_y1')

        cls.current_x = utils.get_arg_value(args, cls.key_inst_x, logger)
        cls.current_y = utils.get_arg_value(args, cls.key_inst_y, logger)

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
        if not hasattr(cls, 'current_x'):
            raise DDOIPreConditionNotRun(cls.__name__)

        serv_name = utils.config_param(cfg, 'ktl_serv', 'dcs')

        inst = utils.get_inst_name(args, cls.__name__)

        guider_cent_x = utils.config_param(cfg, f'{inst}_parameters', 'guider_cent_x')
        guider_cent_y = utils.config_param(cfg, f'{inst}_parameters', 'guider_cent_y')

        ktl_pixel_scale = utils.config_param(cfg, f'ktl_kw_{cls.inst}', 'guider_pix_scale')
        guider_pix_scale = ktl.read(serv_name, ktl_pixel_scale)

        dx = guider_pix_scale * (cls.current_x - guider_cent_x)
        dy = guider_pix_scale * (guider_cent_y - cls.current_y)

        OffsetGuiderCoordXY.execute({'guider_x_offset': dx, 'guider_y_offset': dy})

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



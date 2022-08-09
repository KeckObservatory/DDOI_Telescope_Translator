from ddoitranslatormodule.ddoiexceptions.DDOIExceptions import DDOIPreConditionNotRun
from ddoitranslatormodule.BaseTelescope import TelescopeBase

from ddoi_telescope_translator.gxy import OffsetGuiderCoordXY

import ktl
from collections import OrderedDict


class MoveToGuiderCenter(TelescopeBase):
    """
    gcent -- move an object to the center of the guider pick off mirror

    SYNOPSIS
        MoveToGuiderCenter.execute({'inst_x1': float, 'inst_y1': float,
                                 'instrument': INST})

    RUN
        from ddoi_telescope_translator import gcent
        gcent.MoveToGuiderCenter.execute({'inst_x1': 1.0, 'inst_y1': 2.0,
                                          'instrument': 'kpf'})

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
            MoveToGuiderCenter.execute({'det_x_pix': 100.0, 'det_y_pix': 200.0,
                                      'instrument': INST})

        2) Display the telescope move required to shift a target at
        pixel (100,200) to the pickoff mirror center, without
        actually performing the move:
            MoveToGuiderCenter.execute({'det_x_pix': 100.0, 'det_y_pix': 200.0,
                                      'instrument': INST, 'print_only': 1}

    KTL SERVICE & KEYWORDS

    adapted from sh script: kss/mosfire/scripts/procs/tel/gcent
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

        cls.key_inst_x = cls._config_param(cfg, 'tel_keys', 'inst_x1')
        cls.key_inst_y = cls._config_param(cfg, 'tel_keys', 'inst_y1')

        parser = cls._add_inst_arg(cls, parser, cfg)

        args_to_add = OrderedDict([
            (cls.key_inst_x, {
                'type': float,
                'help': 'The X pixel position to move to guider center.'
            }),
            (cls.key_inst_y, {
                'type': float,
                'help': 'The Y pixel position to move to guider center.'
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
        if not hasattr(cls, 'key_inst_x'):
            cls.key_inst_x = cls._config_param(cfg, 'tel_keys', 'inst_x1')
        if not hasattr(cls, 'key_inst_y'):
            cls.key_inst_y = cls._config_param(cfg, 'tel_keys', 'inst_y1')

        cls.current_x = cls._get_arg_value(args, cls.key_inst_x)
        cls.current_y = cls._get_arg_value(args, cls.key_inst_y)

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
        if not hasattr(cls, 'current_x'):
            raise DDOIPreConditionNotRun(cls.__name__)

        inst = cls.get_inst_name(cls, args, cfg)
        serv_name = cls._config_param(cfg, 'ktl_serv', inst)

        guider_cent_x = cls._config_param(cfg, f'{inst}_parameters',
                                          'guider_cent_x')
        guider_cent_y = cls._config_param(cfg, f'{inst}_parameters',
                                          'guider_cent_y')

        ktl_pixel_scale = cls._config_param(cfg, f"ktl_kw_{inst}",
                                            'guider_pix_scale')
        guider_pix_scale = ktl.read(serv_name, ktl_pixel_scale)

        dx = guider_pix_scale * (cls.current_x - guider_cent_x)
        dy = guider_pix_scale * (guider_cent_y - cls.current_y)

        OffsetGuiderCoordXY.execute({'guider_x_offset': dx,
                                     'guider_y_offset': dy})

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



from ddoitranslatormodule.BaseFunction import TranslatorModuleFunction
from ddoitranslatormodule.ddoiexceptions.DDOIExceptions import DDOIPreConditionNotRun

import tel_utils as utils


class OffsetGuiderCoordXY(TranslatorModuleFunction):
    """
    gxy -- move the telescope in GUIDER coordinates

    SYNOPSIS
        OffsetGuiderCoordXY.execute({'guider_offset_x': 0.0, 'guider_offset_y': 1.0})

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
    def add_cmdline_args(cls, parser, cfg):
        """
        The arguments to add to the command line interface.

        :param parser: <ArgumentParser>
            the instance of the parser to add the arguments to .
        :param cfg: <str> filepath, optional
            File path to the config that should be used, by default None

        :return: <ArgumentParser>
        """
        cls.key_x_offset = utils.config_param(cfg, 'ob_keys', 'guider_x_offset')
        cls.key_y_offset = utils.config_param(cfg, 'ob_keys', 'guider_y_offset')

        parser = utils.add_inst_arg(parser, cfg)

        args_to_add = {
            cls.key_x_offset: {'type': float, 'req': True,
                               'help': 'The offset in Guider X offset in pixels.'},
            cls.key_y_offset: {'type': float, 'req': True,
                               'help': 'The offset in Guider Y offset in pixels.'}}
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
        key_x_offset = utils.config_param(cfg, 'ob_keys', 'guider_x_offset')
        key_y_offset = utils.config_param(cfg, 'ob_keys', 'guider_y_offset')

        cls.x_off = utils.get_arg_value(args, key_x_offset, logger)
        cls.y_off = utils.get_arg_value(args, key_y_offset, logger)

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
        if not hasattr(cls, 'x_off'):
            raise DDOIPreConditionNotRun(cls.__name__)

        cls.serv_name = utils.config_param(cfg, 'ktl_serv', 'dcs')

        key_val = {
            'guider_x_offset': cls.x_off,
            'guider_y_offset': cls.y_off,
            'relative_current': 't'
        }
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


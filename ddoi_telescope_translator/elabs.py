from ddoitranslatormodule.BaseFunction import TranslatorModuleFunction
from ddoitranslatormodule.ddoiexceptions.DDOIExceptions import DDOIPreConditionNotRun

import ddoi_telescope_translator.tel_utils as utils

import ktl


class MoveToElevation(TranslatorModuleFunction):
    """
    elabs -- set/show telescope elevation

    SYNOPSIS
        MoveToElevation.execute({'tcs_coord_el': 10.0})

    DESCRIPTION
        With no argument, return the current telescope absolute elevation.
        With one argument, set the telescope elevation to the specified value.

    ARGUMENTS
        el = desired elevation angle [deg]

    EXAMPLES
        1) show the current elevation:
            MoveToElevation.execute({'print_only': True})

        2) move the telescope to an elevation of 45 deg:
            MoveToElevation.execute({'tcs_coord_el': 45.0})

    adapted from sh script: kss/mosfire/scripts/procs/tel/elabs
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
        cls.key_el_offset = utils.config_param(cfg, 'ob_keys', 'tel_elevation')

        args_to_add = {
            cls.key_el_offset: {'type': float, 'req': True,
                                'help': 'The offset in Elevation in degrees.'}
        }
        parser = utils.add_args(parser, args_to_add, print_only=True)

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
        # check if it is only set to print the current values
        cls.print_only = args.get('print_only', False)
        if cls.print_only:
            return True

        if not hasattr(cls, 'key_el_offset'):
            cls.key_el_offset = utils.config_param(cfg, 'ob_keys', 'tel_elevation')

        cls.el_offset = utils.get_arg_value(args, cls.key_el_offset, logger)

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

        serv_name = utils.config_param(cfg, 'ktl_serv', 'dcs')

        # only print the elevation
        if cls.print_only:
            ktl_elevation = utils.config_param(cfg, 'ktl_kw_dcs', 'elevation')
            el_value = ktl.read(serv_name, ktl_elevation)

            msg = f"Current Elevation = {el_value}"
            utils.write_msg(logger, msg, print_only=True)

            return

        key_val = {
            'target_el': cls.el_offset,
            'target_frame': 'mount',
            'move_tel': 1
        }
        utils.write_to_kw(cfg, serv_name, key_val, logger, cls.__name__)


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


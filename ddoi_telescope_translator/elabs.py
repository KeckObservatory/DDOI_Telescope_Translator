from ddoitranslatormodule.ddoiexceptions.DDOIExceptions import DDOIPreConditionNotRun
from ddoitranslatormodule.BaseTelescope import TelescopeBase

import ktl
from collections import OrderedDict


class MoveToElevation(TelescopeBase):
    """
    elabs -- set/show telescope elevation

    SYNOPSIS
        MoveToElevation.execute({'tcs_coord_el': 10.0})

    RUN
        from ddoi_telescope_translator import elabs
        elabs.MoveToElevation.execute({'print_only': True})

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
        :param cfg: <class 'configparser.ConfigParser'> the config file parser.

        :return: <ArgumentParser>
        """
        # read the config file
        cfg = cls._load_config(cls, cfg)

        cls.key_el_offset = cls._config_param(cfg, 'ob_keys', 'tel_elevation')

        args_to_add = OrderedDict([
            (cls.key_el_offset, {'type': float,
                                'help': 'The offset in Elevation in degrees.'})
        ])
        parser = cls._add_args(parser, args_to_add, print_only=True)

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
        # check if it is only set to print the current values
        cls.print_only = args.get('print_only', False)
        if cls.print_only:
            return True

        if not hasattr(cls, 'key_el_offset'):
            cls.key_el_offset = cls._config_param(cfg, 'ob_keys', 'tel_elevation')

        cls.el_offset = cls._get_arg_value(args, cls.key_el_offset)

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
        if not hasattr(cls, 'print_only'):
            raise DDOIPreConditionNotRun(cls.__name__)

        serv_name = cls._config_param(cfg, 'ktl_serv', 'dcs')

        # only print the elevation
        if cls.print_only:
            ktl_elevation = cls._config_param(cfg, 'ktl_kw_dcs', 'elevation')
            el_value = ktl.read(serv_name, ktl_elevation)

            msg = f"Current Elevation = {el_value}"
            cls.write_msg(logger, msg, print_only=True)

            return

        key_val = {
            'target_el': cls.el_offset,
            'target_frame': 'mount',
            'move_tel': 1
        }
        cls._write_to_kw(cls, cfg, serv_name, key_val, logger, cls.__name__)


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


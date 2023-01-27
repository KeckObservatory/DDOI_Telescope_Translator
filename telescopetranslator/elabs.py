from ddoitranslatormodule.ddoiexceptions.DDOIExceptions import DDOIPreConditionNotRun
from telescopetranslator.BaseTelescope import TelescopeBase

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

        # add the command line description
        parser.description = f'Moves telescope to Elevation in degrees.  ' \
                             f'Modifies KTL DCS keyword: TARGEL, TARGFRAM,' \
                             f' MOVETEL.'

        cls.key_el_offset = cls._cfg_val(cfg, 'ob_keys', 'tel_elevation')

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
            cls.key_el_offset = cls._cfg_val(cfg, 'ob_keys', 'tel_elevation')

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

        # only print the elevation
        if cls.print_only:
            el_value = ktl.read('dcs', 'el')
            msg = f"Current Elevation = {el_value}"
            cls.write_msg(logger, msg, val=el_value, print_only=True)

            return

        # the ktl key name to modify and the value
        key_val = {
            'targel': cls.el_offset,
            'targfram': 'mount',
            'movetel': 1
        }
        cls._write_to_kw(cls, cfg, 'dcs', key_val, logger, cls.__name__)


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


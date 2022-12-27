from ddoitranslatormodule.ddoiexceptions.DDOIExceptions import DDOIPreConditionNotRun
from ddoitranslatormodule.BaseTelescope import TelescopeBase

import ktl
from time import sleep
from collections import OrderedDict


class RotatePhysicalPosAngle(TelescopeBase):
    """
    rotpposn -- set or show the instrument Rotator Physical Position angle

    SYNOPSIS
        RotatePhysicalPosAngle.execute({'rot_cfg_pa_physical': float})

    DESCRIPTION
        With no arguments, show the current physical position angle of
        the Instrument rotator.  With one numeric argument, put the
        instrument rotator into physical position angle mode at the
        given position angle

    ARGUMENTS
        rot_cfg_pa_physical = physical rotator position angle to set [deg]

    OPTIONS

    EXAMPLES
        1) Show the current rotator physical position angle:
            RotatePhysicalPosAngle.execute({'print_only': True})
        2) Set the rotator to physical position of 1.2345 deg:
            RotatePhysicalPosAngle.execute({'rot_cfg_pa_physical': 1.2345})

    KTL SERVICE & KEYWORDS
         dcs: rotmode, rotdest, rotstat

    adapted from sh script: kss/mosfire/scripts/procs/tel/rotpposn
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
        parser.description = f'Set or show the instrument Rotator Physical ' \
                             f'Position angle.  Modifies DCS KTL keywords: ' \
                             f'ROTDEST, ROTMODE.'


        cls.key_rot_angle = cls._cfg_val(cfg, 'ob_keys',
                                              'rot_physical_angle')

        args_to_add = OrderedDict([
            (cls.key_rot_angle, {
                'type': float,
                'help': 'Set the physical rotator position angle [deg].'
            })
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

        if not hasattr(cls, 'key_rot_angle'):
            cls.key_rot_angle = cls._cfg_val(cfg, 'ob_keys',
                                                  'rot_physical_angle')

        cls.rotator_angle = cls._get_arg_value(args, cls.key_rot_angle)

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

        if cls.print_only:
            cls.write_msg(logger, ktl.read('dcs', 'rotpposn'),
                            print_only=True)
            return

        # the ktl key name to modify and the value
        key_val = {
            'rotdest': cls.rotator_angle,
            'rotmode': 'stationary'
        }
        cls._write_to_kw(cls, cfg, 'dcs', key_val, logger, cls.__name__)

        sleep(1)

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
        timeout = cls._cfg_val(cfg, 'ktl_timeout', 'rotpposn')

        if not cls.print_only:
            ktl.waitfor(f'rotstat=tracking', service='dcs',
                        timeout=float(timeout))

        return

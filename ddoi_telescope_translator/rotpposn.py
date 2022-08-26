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

        cls.serv_name = cls._cfg_val(cfg, 'ktl_serv', 'dcs')

        if cls.print_only:
            ktl_rotator_pos = cls._cfg_val(cfg, 'ktl_kw_dcs',
                                                'rotator_position')
            cls.write_msg(logger, ktl.read(cls.serv_name, ktl_rotator_pos),
                            print_only=True)
            return

        key_val = {
            'rotator_destination': cls.rotator_angle,
            'rotator_mode': 'stationary'
        }
        cls._write_to_kw(cls, cfg, cls.serv_name, key_val, logger, cls.__name__)

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
        ktl_rotator_status = cls._cfg_val(cfg, 'ktl_kw_dcs',
                                               'rotator_position')
        ktl.waitfor(f'{ktl_rotator_status}=tracking', cls.serv_name,
                    timeout=timeout)

        return

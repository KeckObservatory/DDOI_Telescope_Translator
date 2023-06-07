from ddoitranslatormodule.ddoiexceptions.DDOIExceptions import DDOIPreConditionNotRun
from telescopetranslator.BaseTelescope import TelescopeBase

from time import sleep
import ktl
from collections import OrderedDict


class SetRotSkyPA(TelescopeBase):
    """
    skypa -- set rotator celestial position angle in position angle mode

    SYNOPSIS
        SetRotSkyPA.execute({'rot_cfg_pa_sky': float, 'instrument': str inst,
                             'relative': bool})

    DESCRIPTION
        With no arguments, show the current rotator position angle as
        it would appear on FACSUM.  With one numeric argument, set the
        rotator to the specified sky position angle.

    ARGUMENTS
        rot_cfg_pa_sky = rotator position angle [degrees]

    RESTRICTIONS
        - INST must be the selected instrument

    KTL SERVICE & KEYWORDS
        dcs: rotdest, rotmode, rotstat

    EXAMPLES
        1) Show the current PA:
            SetRotSkyPA.execute({'print_only': True, 'instrument': INST, 'relative': True})

        2) Set the current PA to 123.45 deg:
            SetRotSkyPA.execute({'rot_cfg_pa_sky': 123.45, 'instrument': INST})

        2) Change the sky PA by -10 deg:
            SetRotSkyPA.execute({'rot_cfg_pa_sky': -10.0, 'instrument': INST,
                                 'relative': True})

    adapted from sh script: kss/mosfire/scripts/procs/tel/skypa
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
        parser.description = f'Set rotator celestial position angle in ' \
                             f'position angle mode.  Modifies DCS KTL ' \
                             f'keywords: ROTDEST, ROTMODE.'

        cls.key_rot_angle = cls._cfg_val(cfg, 'ob_keys', 'rot_sky_angle')

        parser = cls._add_inst_arg(cls, parser, cfg)

        parser = cls._add_bool_arg(parser, 'relative',
                                   'Rotate relative to the current position.')

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
        """
        cls.inst = cls.get_inst_name(cls, args, cfg)

        cls.relative = args.get('relative', False)

        # check if it is only set to print the current values
        cls.print_only = args.get('print_only', False)

        if cls.print_only:
            return

        if not hasattr(cls, 'key_rot_angle'):
            cls.key_rot_angle = cls._cfg_val(cfg, 'ob_keys',
                                                  'rot_sky_angle')

        cls.rotator_angle = cls._get_arg_value(args, cls.key_rot_angle)

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

        if cls.print_only or cls.relative:
            rot_angle = ktl.read('dcs', 'rotpposn')

        if cls.print_only:
            msg = f"Current Rotator Angle = {rot_angle}"
            cls.write_msg(logger, msg, print_only=True)
            return

        rot_dest = args['rot_sky_angle']
        if cls.relative:
            rot_dest += rot_angle

        # the ktl key name to modify and the value
        key_val = {
            'rotdest': rot_dest,
            'rotmode': 1
        }
        cls._write_to_kw(cls, cfg, 'dcs', key_val, logger, cls.__name__)
        sleep(3)

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
        timeout = cls._cfg_val(cfg, 'ktl_timeout', 'skypa')

        if not cls.print_only:
            ktl.waitfor(f'rotstat=8', service='dcs',
                        timeout=timeout)


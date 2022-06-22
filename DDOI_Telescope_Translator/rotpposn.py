from ddoitranslatormodule.BaseFunction import TranslatorModuleFunction
from ddoitranslatormodule.DDOIExceptions import DDOIPreConditionNotRun

import tel_utils as utils

import ktl
from time import sleep

class RotatePhysicalPosAngle(TranslatorModuleFunction):
    """
    rotpposn -- set or show the instrument Rotator Physical Position angle

    SYNOPSIS
        RotatePhysicalPosAngle.execute({'rot_cfg_pa': float})

    DESCRIPTION
        With no arguments, show the current physical position angle of
        the Instrument rotator.  With one numeric argument, put the
        instrument rotator into physical position angle mode at the
        given position angle

    ARGUMENTS
        rot_cfg_pa = physical rotator position angle to set [deg]

    OPTIONS

    EXAMPLES
        1) Show the current rotator physical position angle:
            RotatePhysicalPosAngle.execute()
        2) Set the rotator to physical position of 1.2345 deg:
            RotatePhysicalPosAngle.execute({'rot_cfg_pa': 1.2345})

    KTL SERVICE & KEYWORDS
         dcs: rotmode, rotdest, rotstat

    adapted from sh script: kss/mosfire/scripts/procs/tel/rotpposn
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
        # check for no arguments meaning print value
        cls.print_only = utils.print_only(args, cfg, 'ob_keys', ['rot_physical_angle'])
        if cls.print_only:
            return True

        key_rot_angle = utils.config_param(cfg, 'ob_keys', 'rot_physical_angle')
        cls.rotator_angle = utils.check_float(args, key_rot_angle, logger)

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

        cls.serv_name = utils.config_param(cfg, 'ktl_serv', 'dcs')

        if cls.print_only:
            kw_rotator_pos = utils.config_param(cfg, 'ktl_kw_dcs', 'rotator_position')
            utils.write_msg(logger, ktl.read(cls.serv_name, kw_rotator_pos))
            return

        key_val = {
            'rotator_destination': cls.rotator_angle,
            'rotator_mode': 'stationary'
        }
        utils.write_to_kw(cfg, cls.serv_name, key_val, logger, cls.__name__)

        sleep(1)

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
        timeout = utils.config_param(cfg, 'rotpposn', 'timeout')
        kw_rotator_status = utils.config_param(cfg, 'ktl_kw_dcs', 'rotator_position')
        ktl.waitfor(f'{kw_rotator_status}=tracking', cls.serv_name, timeout=timeout)

        return



from ddoitranslatormodule.BaseFunction import TranslatorModuleFunction
from ddoitranslatormodule.DDOIExceptions import DDOIPreConditionNotRun, DDOINotSelectedInstrument

import tel_utils as utils

import ktl
from time import sleep


class SetRotSkyPA(TranslatorModuleFunction):
    """
    skypa -- set rotator celestial position angle in position angle mode

    SYNOPSIS
        SetRotSkyPA.execute({'rot_cfg_pa_sky': float, 'inst': str inst,
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
            SetRotSkyPA.execute({'inst': INST, 'relative': True})

        2) Set the current PA to 123.45 deg:
            SetRotSkyPA.execute({'rot_cfg_pa_sky': 123.45, 'inst': INST})

        2) Change the sky PA by -10 deg:
            SetRotSkyPA.execute({'rot_cfg_pa_sky': -10.0, 'inst': INST,
                                 'relative': True})

    adapted from sh script: kss/mosfire/scripts/procs/tel/skypa
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
        cls.inst = utils.get_inst_name(args, cls.__name__)
        cls.relative = args.get('relative', False)
        cls.serv_name = utils.config_param(cfg, 'ktl_serv', 'dcs')

        # check for no arguments meaning print value
        cls.print_only = utils.print_only(args, cfg, 'ob_keys', ['rot_sky_angle'])
        if cls.print_only:
            return True

        key_rot_angle = utils.config_param(cfg, 'ob_keys', 'rot_sky_angle')
        cls.rotator_angle = utils.check_float(args, key_rot_angle, logger)

        # confirm INST = the selected instrument
        kw_instrument = utils.config_param(cfg, 'ktl_kw_dcs', 'instrument')
        current_inst = ktl.read(cls.serv_name, kw_instrument)
        if current_inst != cls.inst:
            raise DDOINotSelectedInstrument(current_inst, cls.inst)

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

        rot_dest = args['rot_sky_angle']
        if cls.relative:
            kw_rot_dest = utils.config_param(cfg, 'ktl_kw_dcs',
                                             'rotator_destination')
            rot_dest += ktl.read(cls.serv_name, kw_rot_dest)

        key_val = {
            'rotator_destination': rot_dest,
            'rotator_mode': 1
        }
        utils.write_to_kw(cfg, cls.serv_name, key_val, logger, cls.__name__)
        sleep(3)

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
        timeout = utils.config_param(cfg, 'skypa', 'timeout')
        kw_rot_stat = utils.config_param(cfg, 'ktl_kw_dcs', 'rotator_status')
        ktl.waitfor(f'{kw_rot_stat}=8', cls.serv_name, timeout=timeout)




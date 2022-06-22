from ddoitranslatormodule.BaseFunction import TranslatorModuleFunction
from ddoitranslatormodule.DDOIExceptions import DDOIPreConditionNotRun

import tel_utils as utils

import ktl


class MoveToElevation(TranslatorModuleFunction):
    """
    elabs -- set/show telescope elevation

    SYNOPSIS
        MoveToElevation.execute({'tel_elevation': 10.0})

    DESCRIPTION
        With no argument, return the current telescope absolute elevation.
        With one argument, set the telescope elevation to the specified value.

    ARGUMENTS
        el = desired elevation angle [deg]

    EXAMPLES
        1) show the current elevation:
            python3 elabs.py

        2) move the telescope to an elevation of 45 deg:
            python3 elabs.py {'tel_elevation': 45.0}

    adapted from sh script: kss/mosfire/scripts/procs/tel/elabs
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
        key_el_offset = utils.config_param(cfg, 'ob_keys', 'tel_elevation')

        if key_el_offset in args:
            cls.el_offset = utils.check_float(args, key_el_offset, logger)
        else:
            cls.el_offset = None

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
        if not hasattr(cls, 'el_offset'):
            raise DDOIPreConditionNotRun(cls.__name__)

        serv_name = utils.config_param(cfg, 'ktl_serv', 'dcs')

        # only print the elevation
        if cls.el_offset:
            key_elevation = utils.config_param(cfg, 'ob_keys', 'elevation')
            el_value = ktl.read(serv_name, key_elevation)

            msg = f"Current Elevation = {el_value}"
            utils.write_msg(logger, msg)

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



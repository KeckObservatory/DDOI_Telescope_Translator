from ddoitranslatormodule.BaseFunction import TranslatorModuleFunction
from ddoitranslatormodule.DDOIExceptions import DDOIPreConditionNotRun

import tel_utils as utils

import ktl


class MoveAlongSlit(TranslatorModuleFunction):
    """
    sltmov -- move object along the slit direction in arcsec

    SYNOPSIS
        MoveAlongSlit.execute({'inst_offset_y': float, 'instrument': INST}

    DESCRIPTION
        Move the telescope the given number of arcseconds along the
        slit.  A positive value will "move" the object "down" (i.e., to
        a smaller y pixel value).

    ARGUMENTS
          inst_offset_y - number of arcsec to offset object.

    EXAMPLES
        MoveAlongSlit.execute({'inst_offset_y': 10.0, 'instrument': 'KPF'}
             moves object 10 arcsec in y to more positive y values

    adapted from sh script: kss/mosfire/scripts/procs/tel/slitmov
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

        key_val = {
            '': ,
            '': ,
            '':
        }
        utils.write_to_kw(cfg, cls.serv_name, key_val, logger, cls.__name__)


        return

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



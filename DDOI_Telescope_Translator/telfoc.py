from ddoitranslatormodule.BaseFunction import TranslatorModuleFunction
from ddoitranslatormodule.DDOIExceptions import DDOIKTLTimeOut

import tel_utils as utils

import ktl


class MoveTelescopeFocus(TranslatorModuleFunction):
    """
    telfoc -- set/show the telescope secondary position

     SYNOPSIS
        MoveTelescopeFocus.execute({tel_foc_x: 1.0})

     DESCRIPTION
        With no arguments, show the current position of the telescope
        secondary.  With one argument, reset the telescope secondary
        to the given position.

     DICTIONARY KEY
        tel_foc_x = new value for telescope secondary position

     KTL SERVICE & KEYWORDS
         dcs: telfocus, secmove

    adapted from sh script: kss/mosfire/scripts/procs/tel/telfoc

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
        serv_name = utils.config_param(cfg, 'ktl_serv', 'dcs')
        kw_tel_foc = utils.config_param(cfg, 'ktl_kw_dcs', 'telescope_focus')
        key_tel_focus = utils.config_param(cfg, 'ob_keys', 'tel_foc')

        # only show the focus if no input argument
        try:
            focus_move_val = args[key_tel_focus]
        except KeyError:
            current_focus = ktl.read(serv_name, kw_tel_foc)
            return current_focus

        timeout = utils.config_param(cfg, 'telfoc', 'timeout')

        key_val = {
            'telescope_focus': focus_move_val,
            'secondary_move': 1,
        }
        utils.write_to_kw(cfg, serv_name, key_val, logger, cls.__name__)

        try:
            ktl.waitfor('secmove=0', service=serv_name, timeout=timeout)
        except ktl.TimeoutException:
            msg = f'{cls.__name__} timeout for secondary move.'
            if logger:
                logger.error(msg)
            raise DDOIKTLTimeOut(msg)


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



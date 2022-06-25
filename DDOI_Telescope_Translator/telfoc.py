from ddoitranslatormodule.BaseFunction import TranslatorModuleFunction
from DDOITranslatorModule.ddoitranslatormodule.ddoiexceptions.DDOIExceptions import DDOIKTLTimeOut

import DDOI_Telescope_Translator.tel_utils as utils

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
    def add_cmdline_args(cls, parser, cfg):
        """
        The arguments to add to the command line interface.

        :param parser: <ArgumentParser>
            the instance of the parser to add the arguments to .
        :param cfg: <str> filepath, optional
            File path to the config that should be used, by default None

        :return: <ArgumentParser>
        """
        cls.key_tel_focus = utils.config_param(cfg, 'ob_keys', 'tel_foc')

        parser = utils.add_inst_arg(parser, cfg)

        args_to_add = {
            cls.key_tel_focus: {'type': float, 'req': True,
                                'help': 'The new value for telescope secondary position.'}
        }
        parser = utils.add_args(parser, args_to_add, print_only=True)

        return super().add_cmdline_args(parser, cfg)

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

        # check if it is only set to print the current values
        cls.print_only = args.get('print_only', False)

        if cls.print_only:
            current_focus = ktl.read(serv_name, kw_tel_foc)
            return current_focus

        if not hasattr(cls, 'key_tel_focus'):
            cls.key_tel_focus = utils.config_param(cfg, 'ob_keys', 'tel_foc')

        focus_move_val = utils.get_arg_value(args, cls.key_tel_focus, logger)

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

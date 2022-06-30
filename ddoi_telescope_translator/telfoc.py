from ddoitranslatormodule.BaseFunction import TranslatorModuleFunction
from ddoitranslatormodule.ddoiexceptions.DDOIExceptions import DDOIKTLTimeOut

import ddoi_telescope_translator.tel_utils as utils

import ktl
from collections import OrderedDict


class MoveTelescopeFocus(TranslatorModuleFunction):
    """
    telfoc -- set/show the telescope secondary position

     SYNOPSIS
        MoveTelescopeFocus.execute({'tcs_cfg_focus': 1.0})

     DESCRIPTION
        With the 'print_only' argument, show the current position of the
        telescope secondary.  With 'tel_foc_x' argument, reset the
        telescope secondary to the given value.

     DICTIONARY KEY
        tel_foc_x = new value for telescope secondary position
        print_only = True
            to print the current telescope focus value
     KTL SERVICE & KEYWORDS
         dcs: telfocus, secmove

    adapted from sh script: kss/mosfire/scripts/procs/tel/telfoc

    """

    @classmethod
    def add_cmdline_args(cls, parser, cfg=None):
        """
        The arguments to add to the command line interface.

        :param parser: <ArgumentParser>
            the instance of the parser to add the arguments to .
        :param cfg: <str> filepath, optional
            File path to the config that should be used, by default None

        :return: <ArgumentParser>
        """
        # read the config file
        cfg = cls._load_config(cfg)

        cls.key_tel_focus = utils.config_param(cfg, 'ob_keys', 'tel_foc')

        parser = utils.add_inst_arg(parser, cfg)

        args_to_add = OrderedDict([
            (cls.key_tel_focus, {'type': float,
                                 'help': 'The new value for telescope '
                                         'secondary position.'})
        ])
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
        ktl_tel_foc = utils.config_param(cfg, 'ktl_kw_dcs', 'telescope_focus')

        # check if it is only set to print the current values
        cls.print_only = args.get('print_only', False)

        if cls.print_only:
            current_focus = ktl.read(serv_name, ktl_tel_foc)
            msg = f"Current Focus = {current_focus}"
            utils.write_msg(logger, msg, print_only=True)

            return

        if not hasattr(cls, 'key_tel_focus'):
            cls.key_tel_focus = utils.config_param(cfg, 'ob_keys', 'tel_foc')

        focus_move_val = utils.get_arg_value(args, cls.key_tel_focus, logger)

        timeout = int(utils.config_param(cfg, 'telfoc', 'timeout'))

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

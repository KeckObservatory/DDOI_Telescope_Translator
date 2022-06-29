from ddoitranslatormodule.BaseFunction import TranslatorModuleFunction
from ddoitranslatormodule.DDOIExceptions import DDOIPreConditionNotRun

import tel_utils as utils

import ktl


class SetNodEastValue(TranslatorModuleFunction):
    """
    node - set nod parameters for north motions

    SYNOPSIS
        SetNodEastValue.execute({
            'tel_north_offset': float,
            'instrument': str of instrument name
            })

    DESCRIPTION
        sets the telescope nod parameters to dE arcsec East
             and dN arcsec North

    ARGUMENTS

    OPTIONS

    EXAMPLES
        1) Set north nod to 5 :
            SetNodValues.execute({'tel_north_offset': 5.0, 'instrument': INST})

        2) Show current nod params:
            SetNodValues.execute('instrument': INST)

    ENVIRONMENT VARIABLES

    FILES

    SERVERS & KEYWORDS
       servers: instrument
        keywords: node nodn

    KTL SERVICE & KEYWORDS

    adapted from sh script: kss/mosfire/scripts/procs/tel/
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
        cls.key_nod_north = utils.config_param(cfg, 'ob_keys', 'tel_north_offset')

        parser = utils.add_inst_arg(parser, cfg)

        args_to_add = {
            cls.key_nod_north: {'type': float, 'req': True,
                                'help': 'Set the North Nod value [arcseconds]'}
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
        cls.inst = utils.get_inst_name(args, cls.__name__)

        # check if it is only set to print the current values
        cls.print_only = args.get('print_only', False)

        if cls.print_only:
            return True

        if not hasattr(cls, 'key_nod_north'):
            cls.key_nod_north = utils.config_param(cfg, 'ob_keys', 'tel_north_offset')

        cls.nod_north = utils.get_arg_value(args, cls.key_nod_north, logger)
        
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

        serv_name = utils.config_param(cfg, 'ktl_serv', cls.inst)

        if cls.print_only:
            key_nod_north = utils.config_param(cfg, f'ktl_kw_{cls.inst}',
                                               'nod_north')
            msg = f"Current Nod Values E: {ktl.read(serv_name, key_nod_north)}"
            utils.write_msg(logger, msg)
            return

        key_val = {'nod_north': cls.nod_north}
        utils.write_to_kw(cfg, serv_name, key_val, logger, cls.__name__)

        msg = f"New Nod East Value: {cls.nod_north}"
        utils.write_msg(logger, msg)

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



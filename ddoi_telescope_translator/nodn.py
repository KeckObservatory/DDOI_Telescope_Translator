from ddoitranslatormodule.ddoiexceptions.DDOIExceptions import DDOIPreConditionNotRun
from ddoitranslatormodule.BaseTelescope import TelescopeBase

import ktl
from collections import OrderedDict


class SetNodNorthValue(TelescopeBase):
    """
    node - set nod parameters for north motions

    SYNOPSIS
        SetNodNorthValue.execute({
            'tcs_offset_north': float,
            'instrument': str of instrument name
            })

    RUN
        from ddoi_telescope_translator import nod
        nodn.SetNodNorthValue.execute({'tcs_offset_north': 10.0, 'instrument': 'KPF'})

    DESCRIPTION
        sets the telescope nod parameters to dE arcsec East
             and dN arcsec North

    EXAMPLES
        1) Set north nod to 5 :
            SetNodNorthValue.execute({'tcs_offset_north': 5.0, 'instrument': INST})

        2) Show current nod params:
            SetNodNorthValue.execute('instrument': INST)

    ENVIRONMENT VARIABLES

    FILES

    SERVERS & KEYWORDS
       servers: instrument
        keywords: node nodn

    KTL SERVICE & KEYWORDS

    adapted from sh script: kss/mosfire/scripts/procs/tel/
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

        cls.key_nod_north = cls._config_param(cfg, 'ob_keys', 'tel_north_offset')

        parser = cls._add_inst_arg(cls, parser, cfg)

        args_to_add = OrderedDict([
            (cls.key_nod_north, {'type': float,
                                 'help': 'Set the North Nod value [arcseconds]'})
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
        cls.inst = cls.get_inst_name(cls, args, cfg)

        # check if it is only set to print the current values
        cls.print_only = args.get('print_only', False)

        if cls.print_only:
            return True

        if not hasattr(cls, 'key_nod_north'):
            cls.key_nod_north = cls._config_param(cfg, 'ob_keys',
                                                  'tel_north_offset')

        cls.nod_north = cls._get_arg_value(args, cls.key_nod_north)
        
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

        serv_name = cls._config_param(cfg, 'ktl_serv', cls.inst)

        if cls.print_only:
            key_nod_north = cls._config_param(cfg, f'ktl_kw_{cls.inst}',
                                               'nod_north')
            msg = f"Current Nod Values E: {ktl.read(serv_name, key_nod_north)}"
            cls.write_msg(logger, msg)
            return

        key_val = {'nod_north': cls.nod_north}
        cls._write_to_kw(cls, cfg, serv_name, key_val, logger, cls.__name__)

        msg = f"New Nod East Value: {cls.nod_north}"
        cls.write_msg(logger, msg)

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
        return



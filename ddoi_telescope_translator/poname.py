from ddoitranslatormodule.BaseTelescope import TelescopeBase

import ktl
from collections import OrderedDict


class SetPointingOriginName(TelescopeBase):
    """
    poname -- set or show the current pointing origin


    SYNOPSIS
        SetPointingOriginName.execute({'tcs_cfg_po_name': ORIGIN})

    DESCRIPTION
        With no argument, prints the name of the currently selected
        pointing origin.  With one argument, reset the current
        pointing origin to the named value.

        Only functions when DEIMOS is in nighttime mode and can
        converse with the drive and control system (DCS) library.

    ARGUMENTS
        name = name of the pointing origin to select
    OPTIONS

    EXAMPLES
        1) show the current pointing origin
            SetPointingOriginName.execute({'print_only': True})

        2) change the pointing origin to Slit:
            SetPointingOriginName.execute({'tcs_cfg_po_name': SLIT})

    ENVIRONMENT VARIABLES

    FILES

    SERVERS & KEYWORDS
         dcs: poname
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

        # add the command line description
        key_ktl_po = cls._cfg_val(cfg, 'ktl_kw_dcs', 'pointing_origin_name').upper()
        key_ktl_pos = cls._cfg_val(cfg, 'ktl_kw_dcs', 'pointing_origin_select').upper()

        parser.description = f'Set or show the current pointing origin. ' \
                             f'Modifies DCS KTL Keyword: {key_ktl_po},  {key_ktl_pos}.'

        cls.key_po_name = cls._cfg_val(cfg, 'ob_keys', 'pointing_origin_name')

        args_to_add = OrderedDict([
            (cls.key_po_name, {'type': str,
                               'help': 'The name of the pointing origin to select'})
        ])
        parser = cls._add_args(parser, args_to_add, print_only=True)

        # add the required instrument
        parser = cls._add_inst_arg(cls, parser, cfg)

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
        serv_name = cls._cfg_val(cfg, 'ktl_serv', 'dcs')
        if not hasattr(cls, 'key_po_name'):
            cls.key_po_name = cls._cfg_val(cfg, 'ob_keys',
                                                'pointing_origin_name')

        # check if it is only set to print the current values
        if args.get('print_only', False):
            ktl_po_name = cls._cfg_val(cfg, 'ktl_kw_dcs',
                                            'pointing_origin_name')
            cls.write_msg(logger, ktl.read(serv_name, ktl_po_name),
                            print_only=True)
            return

        po_name = cls._get_arg_value(args, cls.key_po_name)

        key_val = {
            'pointing_origin_name': po_name,
            'pointing_origin_select': 1
        }
        cls._write_to_kw(cls, cfg, serv_name, key_val, logger, cls.__name__)

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



from ddoitranslatormodule.ddoiexceptions.DDOIExceptions import DDOIPreConditionNotRun
from telescopetranslator.BaseTelescope import TelescopeBase

import tel_utils as utils

import ktl
from collections import OrderedDict


class Boiler(TelescopeBase):
    """

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

        cls.xxx = cls._cfg_val(cfg, 'ob_keys', '...')

        args_to_add = {
            cls.xxx: {'type': float, 'req': True,
                      'help': 'The offset in Azimuth in degrees.'},
            cls.xxx: {'type': float, 'req': True,
                      'help': 'The offset in Elevation in degrees.'}}
        parser = cls._add_args(parser, args_to_add, print_only=False)

        parser = cls._add_inst_arg(cls, parser)

        return super().add_cmdline_args(parser, cfg)

    @classmethod
    def pre_condition(cls, args, logger, cfg):
        """
        :param args:  <dict> The OB (or subset) in dictionary form
        :param logger: <DDOILoggerClient>, optional
            The DDOILoggerClient that should be used. If none is provided,
            defaults to a generic name specified in the config, by default None
        :param cfg: <class 'configparser.ConfigParser'> the config file parser.
        """
        if not hasattr(cls, '...'):
            cls.xxx = cls._cfg_val(cfg, 'ob_keys', '...')

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

        # the ktl key name to modify and the value
        key_val = {
            '': ,
            '': ,
            '':
        }
        cls._write_to_kw(cls, cfg, 'dcs', key_val, logger, cls.__name__)


        return

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

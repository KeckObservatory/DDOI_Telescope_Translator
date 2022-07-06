from ddoitranslatormodule.ddoiexceptions.DDOIExceptions import DDOIPreConditionNotRun
from ddoi_telescope_translator.telescope_base import TelescopeBase

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
        :param cfg: <str> filepath, optional
            File path to the config that should be used, by default None

        :return: <ArgumentParser>
        """
        # read the config file
        cfg = cls._load_config(cfg)

        cls.xxx = cls._config_param(cfg, 'ob_keys', '...')

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
        :param cfg: <str> filepath, optional
            File path to the config that should be used, by default None

        :return: bool
        """
        if not hasattr(cls, '...'):
            cls.xxx = cls._config_param(cfg, 'ob_keys', '...')

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

        cls.serv_name = cls._config_param(cfg, 'ktl_serv', 'dcs')

        key_val = {
            '': ,
            '': ,
            '':
        }
        cls._write_to_kw(cls, cfg, cls.serv_name, key_val, logger, cls.__name__)


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

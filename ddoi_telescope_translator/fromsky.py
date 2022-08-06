from ddoi_telescope_translator.telescope_base import TelescopeBase

from ddoi_telescope_translator.en import OffsetEastNorth

import ktl


class OffsetBackFromNod(TelescopeBase):
    """
    fromsky - move the telescope from the sky position

    SYNOPSIS
        OffsetBackFromNod.execute({'instrument': 'KPF'})

    RUN
        from ddoi_telescope_translator import fromsky
        fromsky.OffsetBackFromNod.execute({'instrument': 'kpf'})

    DESCRIPTION
        Move the telescope to the target position from the
            "sky" position designated by the nod parameters.
           Offset the telescope by minus the nod params.

    KTL SERVICE & KEYWORDS
        nodn, node

    adapted from sh script: kss/mosfire/scripts/procs/tel/fromsky
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

        # add inst parameter as optional
        parser = cls._add_inst_arg(cls, parser, cfg, is_req=False)

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
        inst = cls.get_inst_name(cls, args, cfg)

        serv_name = cls._config_param(cfg, 'ktl_serv', inst)

        if not hasattr(cls, 'key_east_offset'):
            cls.key_east_offset = cls._config_param(cfg, 'ob_keys',
                                                     'tel_east_offset')
        if not hasattr(cls, 'key_north_offset'):
            cls.key_north_offset = cls._config_param(cfg, 'ob_keys',
                                                      'tel_north_offset')

        ktl_nodded_north = cls._config_param(cfg, f'ktl_kw_{inst}', 'nod_north')
        ktl_nodded_east = cls._config_param(cfg, f'ktl_kw_{inst}', 'nod_east')

        nodded_north = ktl.read(serv_name, ktl_nodded_north)
        nodded_east = ktl.read(serv_name, ktl_nodded_east)

        OffsetEastNorth.execute({cls.key_east_offset: -1.0 * nodded_east,
                                 cls.key_north_offset: -1.0 * nodded_north})

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

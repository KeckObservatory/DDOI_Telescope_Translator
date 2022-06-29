from ddoitranslatormodule.BaseFunction import TranslatorModuleFunction

import tel_utils as utils
from en import OffsetEastNorth

import ktl


class OffsetBackFromNod(TranslatorModuleFunction):
    """
    fromsky - move the telescope from the sky position

    SYNOPSIS
        OffsetBackFromNod.execute()

    DESCRIPTION
        Move the telescope to the target position from the
            "sky" position designated by the nod parameters.
           Offset the telescope by minus the nod params.

    KTL SERVICE & KEYWORDS
        nodn, node

    adapted from sh script: kss/mosfire/scripts/procs/tel/fromsky
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
        cls.key_east_offset = utils.config_param(cfg, 'ob_keys', 'tel_east_offset')
        cls.key_north_offset = utils.config_param(cfg, 'ob_keys', 'tel_north_offset')

        args_to_add = {
            cls.key_east_offset: {'type': float, 'req': True,
                                  'help': 'The offset East in arcseconds.'},
            cls.key_north_offset: {'type': float, 'req': True,
                                   'help': 'The offset North in arcseconds.'}}
        parser = utils.add_args(parser, args_to_add, print_only=False)

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
        inst = utils.get_inst_name(args, cls.__name__)
        serv_name = utils.config_param(cfg, 'ktl_serv', inst)

        if not hasattr(cls, 'key_east_offset'):
            cls.key_east_offset = utils.config_param(cfg, 'ob_keys',
                                                     'tel_east_offset')
        if not hasattr(cls, 'key_north_offset'):
            cls.key_north_offset = utils.config_param(cfg, 'ob_keys',
                                                      'tel_north_offset')

        ktl_nodded_north = utils.config_param(cfg, f'ktl_kw_{inst}', 'nod_north')
        ktl_nodded_east = utils.config_param(cfg, f'ktl_kw_{inst}', 'nod_east')

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
        :param cfg: <str> filepath, optional
            File path to the config that should be used, by default None

        :return: None
        """
        return

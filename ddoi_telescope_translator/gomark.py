from ddoitranslatormodule.BaseFunction import TranslatorModuleFunction

import ddoi_telescope_translator.tel_utils as utils

import ktl


class GoToMark(TranslatorModuleFunction):
    """
      gomark - restore telescope position to saved offsets

    SYNOPSIS
        GoToMark.execute({'inst': str of instrument name})

    DESCRIPTION
          moves to the position defined by the keywords "raoffset" and
          "decoffset", which are normally loaded by the command "mark".

    KTL SERVICE & KEYWORDS
        server: instrument, dcs
            keywords: raoffset, decoffset, raoff, decoff

    adapted from sh script: kss/mosfire/scripts/procs/tel/gmomark
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
        parser = utils.add_inst_arg(parser, cfg)

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

        inst_serv_name = utils.config_param(cfg, 'ktl_serv', inst)
        ktl_ra_mark = utils.config_param(cfg, f'ktl_kw_{inst}', 'ra_mark')
        ktl_dec_mark = utils.config_param(cfg, f'ktl_kw_{inst}', 'dec_mark')

        ra_mark = ktl.read(inst_serv_name, ktl_ra_mark)
        dec_mark = ktl.read(inst_serv_name, ktl_dec_mark)

        cls.dcs_serv_name = utils.config_param(cfg, 'ktl_serv', 'dcs')

        key_val = {
            'ra_offset': ra_mark,
            'dec_offset': dec_mark,
            'relative_base': 't'
        }
        utils.write_to_kw(cfg, cls.dcs_serv_name, key_val, logger, cls.__name__)


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
        utils.wait_for_cycle(cfg, cls.dcs_serv_name, logger)



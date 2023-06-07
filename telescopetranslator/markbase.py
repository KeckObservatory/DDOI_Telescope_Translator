from telescopetranslator.BaseTelescope import TelescopeBase


class MarkBase(TelescopeBase):
    """
    markbase -- set the base telescope coordinates to the current coordinates

    SYNOPSIS
        MarkBase.execute()

    DESCRIPTION
        Reset the telescope BASE corodinates to be the current
        coordinates of the telescope; i.e., reset the RA and Dec
        offsets to zero.  This might be useful when you are about to
        undertake and operation which will require numerous telescope moves
        and you want to be able to return to the starting position.
        In this case, use "markbase" before your first move, and then use
        "gotobase" to return to the starting position.

    ARGUMENTS

    OPTIONS

    EXAMPLES
        1) set the base coordinates to the current coordinates:
            MarkBase.execute()

    KTL SERVICE & KEYWORDS

    adapted from sh script: kss/mosfire/scripts/procs/tel/markbase
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

        parser.description = f'Set the base telescope coordinates to the ' \
                             f'current coordinates.  Modifies KTL DCS ' \
                             f'Keyword: MARK.'

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
        # the ktl key name to modify and the value
        key_val = {
            'mark': 'true'
        }
        cls._write_to_kw(cls, cfg, 'dcs', key_val, logger, cls.__name__)

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



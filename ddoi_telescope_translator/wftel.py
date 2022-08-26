from ddoitranslatormodule.ddoiexceptions.DDOIExceptions import DDOIPreConditionNotRun
from ddoitranslatormodule.BaseTelescope import TelescopeBase

import ktl
from time import sleep
from collections import OrderedDict


class WaitForTel(TelescopeBase):
    """
    Wait for the Telescope move to complete.

    SYNOPSIS
        WaitForTel.execute({"auto_resume": auto_resume})

    RUN
        from ddoi_telescope_translator import wftel
        wftel.WaitForTel.execute({"auto_resume": auto_resume})

    After issuing the offset request, the keyword AUTPAUSE is monitored
    for an increment in sequence number. Next the keyword AUTGO is monitored
    for a change to RESUMEACK -- which is issued by the guider. The guider
    will throw away the first image and resume guiding with the next image.
    The offsetting/nodding script can terminate at this point also, without
    waiting for guiding to fully resume. TCS internally waits for AXESTAT
    to go from SLEWING to TRACKING before sending the RESUME notification,
    thus we assume that the telescope is at the correct position by the
    time the guider acknowledges the RESUME notification. This will save
    more time one more guider cycle than the first method at the risk that
    the guide star may be not at the final destination. This can happen if
    the plate scale is not correct (i.e. at the edges of the guider detector)
    and the guide box goes to a different place than the guide star image.
    The first guider image after the offset will drag the star to where the
    guide box is.

     KTL SERVICE & KEYWORDS
     service = dcs
       keywords: autresum, autactiv, autgo

    adapted from sh script: kss/mosfire/scripts/procs/tel/wftel
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
        args_to_add = OrderedDict([
            ('auto_resume', {'type': int, 'req': False, 'kw_arg': True,
                             'help': 'The Auto Resume parameter.'})
        ])
        parser = cls._add_args(parser, args_to_add, print_only=False)

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
        # max guider exposure
        cls.timeout = cls._cfg_val(cfg, 'ktl_timeout', 'default')
        cls.serv_name = cls._cfg_val(cfg, 'ktl_serv', 'dcs')
        ktl_auto_activate = cls._cfg_val(cfg, 'ktl_kw_dcs', 'auto_activate')

        cls.auto_resume = args.get('auto_resume', None)

        try:
            waited = ktl.waitfor('axestat=tracking', service=cls.serv_name,
                                 timeout=cls.timeout, )
        except:
            waited = False

        if not waited:
            msg = f'tracking was not established in {cls.timeout}'
            cls.write_msg(logger, msg)
            return False

        if ktl.read(cls.serv_name, ktl_auto_activate) == 'no':
            msg = 'guider not currently active'
            cls.write_msg(logger, msg)
            return False

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
        if not hasattr(cls, 'timeout'):
            raise DDOIPreConditionNotRun(cls.__name__)

        ktl_auto_resume = cls._cfg_val(cfg, 'ktl_kw_dcs', 'auto_resume')
        ktl_auto_go = cls._cfg_val(cfg, 'ktl_kw_dcs', 'auto_go')

        serv_auto_resume = ktl.cache(cls.serv_name, ktl_auto_resume)
        serv_auto_go = ktl.cache(cls.serv_name, ktl_auto_go)

        # set the value for the current autpause
        if not cls.auto_resume:
            cls.auto_resume = serv_auto_resume.read()

        if not cls.waited_for_val(cls.timeout, serv_auto_resume, cls.autresum):
            msg = 'timeout waiting for dcs keyword AUTRESUM to increment'
            cls.write_msg(logger, msg)

        if not cls.waited_for_val(cls.timeout, serv_auto_go, "RESUMEACK",
                                  val2="GUIDE"):
            msg = 'timeout waiting for dcs keyword AUTGO ' \
                  'to go to RESUMEACK or GUIDE'
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


    @staticmethod
    def waited_for_val(timeout, ktl_cache, val1, val2=None):
        """
        Wait for ktl keyword value to change to specified value(s)

        @param timeout: <int> the length in seconds to wait
        @param ktl_cache: <ktl cache> the ktl cached connection
        @param val1: <> the value to wait for.
        @param val2: <> optionally specify a second value to wait for.

        @return: <bool> True if the keyword became the awaited value,  False on
                        timeout.
        """
        for cnt in range(0, timeout):
            chk_val = ktl_cache.read()
            if not val2:
                if chk_val == val1:
                    return True
            else:
                if chk_val == val1 or chk_val == val2:
                    return True

            sleep(1)

        return False

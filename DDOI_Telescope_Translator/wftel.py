from ddoitranslatormodule.BaseFunction import TranslatorModuleFunction
from ddoitranslatormodule.DDOIExceptions import DDOIPreConditionNotRun

import ktl
from time import sleep

import tel_utils as utils


class WaitForTel(TranslatorModuleFunction):
    """
    Wait for the Telescope move to complete.

    SYNOPSIS
        WaitForTel.execute({"auto_resume": auto_resume})

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
    def __init__(self):
        super().__init__()

    @classmethod
    def pre_condition(cls, args, logger, cfg):
        """

        :param args:
        :param logger:
        :param cfg:
        :return:
        """
        # max guider exposure
        cls.timeout = utils.config_param(cfg, 'wftl', 'timeout')
        cls.serv_name = utils.config_param(cfg, 'ktl_serv', 'dcs')
        auto_activate = utils.config_param(cfg, 'ktl_kw_dcs', 'auto_activate')

        cls.auto_resume = args.get('auto_resume', None)

        if not ktl.waitfor('axestat=tracking', service=cls.serv_name,
                           timeout=cls.timeout):
            msg = f'tracking was not established in {cls.timeout}'
            utils.write_msg(logger, msg)
            return False

        if ktl.read(cls.serv_name, auto_activate) == 'no':
            msg = 'guider not currently active'
            utils.write_msg(logger, msg)
            return False

        return True

    @classmethod
    def perform(cls, args, logger, cfg):
        """

        :param args: (dict)
        :param logger:
        :param cfg:
        :return:
        """
        if not hasattr(cls, 'timeout'):
            raise DDOIPreConditionNotRun(cls.__name__)

        kw_auto_resume = utils.config_param(cfg, 'ktl_kw_dcs', 'auto_resume')
        kw_auto_go = utils.config_param(cfg, 'ktl_kw_dcs', 'auto_go')

        serv_auto_resume = ktl.cache(cls.serv_name, kw_auto_resume)
        serv_auto_go = ktl.cache(cls.serv_name, kw_auto_go)

        # set the value for the current autpause
        if not cls.auto_resume:
            cls.auto_resume = utils.read_auto_resume_val(cfg, cls.serv_name)

        if not cls.waited_for_val(cls.timeout, serv_auto_resume, cls.autresum):
            msg = 'timeout waiting for dcs keyword AUTRESUM to increment'
            utils.write_msg(logger, msg)

        if not cls.waited_for_val(cls.timeout, serv_auto_go, "RESUMEACK",
                                  val2="GUIDE"):
            msg = 'timeout waiting for dcs keyword AUTGO ' \
                  'to go to RESUMEACK or GUIDE'
            utils.write_msg(logger, msg)

    @classmethod
    def post_condition(cls, args, logger, cfg):
        return


    @staticmethod
    def waited_for_val(timeout, kw_cache, val1, val2=None):
        for cnt in range(0, timeout):
            chk_val = kw_cache.read()
            if not val2:
                if chk_val == val1:
                    return True
            else:
                if chk_val == val1 or chk_val == val2:
                    return True

            sleep(1)

        return False

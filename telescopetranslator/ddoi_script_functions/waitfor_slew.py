
from telescopetranslator.BaseTelescope import TelescopeBase

class waitfor_slew(TelescopeBase):

    '''
    '''
    @classmethod
    def pre_condition(cls, args, logger, cfg):
        pass 

    @classmethod
    def perform(cls, args, logger, cfg):
        logger.info("I would wait for slew, if I knew how!")


    @classmethod
    def post_condition(cls, args, logger, cfg):
        pass


from telescopetranslator.BaseTelescope import TelescopeBase

class begin_slew(TelescopeBase):

    '''
    '''
    @classmethod
    def pre_condition(cls, args, logger, cfg):
        pass 

    @classmethod
    def perform(cls, args, logger, cfg):
        logger.info("I would slew, if I knew how!")


    @classmethod
    def post_condition(cls, args, logger, cfg):
        pass 
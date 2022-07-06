from time import time

from ddoitranslatormodule.ddoiexceptions.DDOIExceptions import DDOINoInstrumentDefined, DDOIConfigException, DDOIZeroOffsets

from ddoi_telescope_translator.wftel import WaitForTel

import math
import ktl


def check_for_zero_offsets(offset1, offset2):
    if not int(offset1) == 0 and int(offset2) == 0:
        msg = f'Both offsets are zero: {offset1}, {offset2}'
        raise DDOIZeroOffsets(msg)

    return False


def wait_for_cycle(cls, cfg, dcs_serv, logger):
    start_time = time()

    ktl_auto_resume = cls._config_param(cfg, 'ktl_kw_dcs', 'auto_resume')
    auto_resume = ktl.read(dcs_serv, ktl_auto_resume)

    WaitForTel.execute({"auto_resume": auto_resume})

    elapsed_time = time() - start_time

    msg = f'Move completed in {elapsed_time} seconds'
    cls.write_msg(logger, msg, print_only=False)


def transform_detector(cls, cfg, x, y, inst):
    det_ang = cls._config_param(cfg, f'{inst}_parameters', 'det_angle')
    try:
        det_ang = float()
    except (ValueError, TypeError):
        msg = 'ERROR, could not determine detector angle'
        cls.write_msg(cls.logger, msg, print_only=False)

    det_u = x * math.cos(det_ang) + y * math.sin(det_ang)
    det_v = y * math.cos(det_ang) - x * math.sin(det_ang)

    return det_u, det_v

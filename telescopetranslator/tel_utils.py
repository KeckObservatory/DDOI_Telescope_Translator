from time import time

from ddoitranslatormodule.ddoiexceptions.DDOIExceptions import DDOINoInstrumentDefined, DDOIConfigException, DDOIZeroOffsets

from telescopetranslator.wftel import WaitForTel

import math
import ktl


def check_for_zero_offsets(offset1, offset2):
    """
    Determine if both offsets are zero.

    :param offset1: <float> first offset to check
    :param offset2: <float> second offset to check
    :return:
    """
    if math.isclose(offset1, 0.0, rel_tol=1e-5) and \
            math.isclose(offset2, 0.0, rel_tol=1e-5):
        msg = f'Both offsets are zero: {offset1}, {offset2}'
        raise DDOIZeroOffsets(msg)


def wait_for_cycle(cls, cfg, ktl_serv, logger):
    """
    Wait a cycle

    :param cfg: <class 'configparser.ConfigParser'> the config file parser.
    :param ktl_serv: <str> name of the dcs service
    :param logger: <DDOILoggerClient>, optional
            The DDOILoggerClient that should be used. If none is provided,
            defaults to a generic name specified in the config, by default None
    :return:
    """
    start_time = time()

    auto_resume = ktl.read(ktl_serv, 'autresum')

    WaitForTel.execute({"auto_resume": auto_resume})

    elapsed_time = time() - start_time

    msg = f'Move completed in {elapsed_time} seconds'
    cls.write_msg(logger, msg, print_only=False)


def transform_detector(cls, cfg, x, y, inst):
    """
    Change X,Y into detector coordinates.

    :param cfg: <class 'configparser.ConfigParser'> the config file parser.
    :param x: <float> the X coordinate to transform
    :param y: <float> the Y coordinate to transform
    :param inst: <str> the instrument string
    :return: 
    """
    det_ang = cls._cfg_val(cfg, f'{inst}_parameters', 'det_angle')
    try:
        det_ang = float()
    except (ValueError, TypeError):
        msg = 'ERROR, could not determine detector angle'
        cls.write_msg(cls.logger, msg, print_only=False)

    det_u = x * math.cos(det_ang) + y * math.sin(det_ang)
    det_v = y * math.cos(det_ang) - x * math.sin(det_ang)

    return det_u, det_v

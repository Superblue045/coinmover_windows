from enum import Enum


class IntradayIntervalSeconds(Enum):
    _1m    =         1 * 60
    _3m    =         3 * 60
    _5m    =         5 * 60
    _15m   =        15 * 60
    _30m   =        30 * 60
    _1h    =        60 * 60
    _2h    =    2 * 60 * 60
    _4h    =    4 * 60 * 60
    _6h    =    6 * 60 * 60
    _8h    =    8 * 60 * 60
    _12h   =   12 * 60 * 60
    _D     =   24 * 60 * 60
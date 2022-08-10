from enum import Enum


class Importance(Enum):
    high = 10
    normal = 5
    low = 1

importanceDict={Importance.high:'灰常重要！',
                Importance.normal:'普通事项',
                Importance.low:'不着急呢~'}

from enum import Enum


class Importance(Enum):
    high = 10
    normal = 5
    low = 1

importanceDict={Importance.high:'灰常重要！',
                Importance.normal:'普通事项',
                Importance.low:'不着急呢~'}
str2Importmance={'灰常重要！':Importance.high,
                 '普通事项':Importance.normal,
                 '不着急呢~':Importance.low}

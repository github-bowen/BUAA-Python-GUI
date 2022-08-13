from enum import Enum

class Species(Enum):
    work = 1  # 工作
    study = 2  # 学习
    sport = 3  # 运动
    fun = 4  # 娱乐
    other = 5 # 其他


speciesDict={Species.work:'工作',Species.study:'学习',
              Species.sport:'运动',Species.fun:'娱乐',
              Species.other:'其他'}
str2Species={'工作':Species.work,'学习':Species.study,
             '运动':Species.sport,'娱乐':Species.fun,
             '其他':Species.other}

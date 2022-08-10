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

from enum import Enum


class State(Enum):
    notStarted = 1  # 未开始
    inProgress = 2  # 进行中
    finished = 3  # 已完成
    expired = 4  # 过期

    daily = 5 # 日常任务

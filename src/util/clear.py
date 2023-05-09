"""
清空所有注册的账号
"""
import os

with open("../backend/.data/userList.json", "w") as userList:
    userList.write("{}")
try:
    os.remove("../frontend/.login.log")
except FileNotFoundError:
    pass
print("\033[36m" + "clear the information of account successfully!" + "\033[0m")

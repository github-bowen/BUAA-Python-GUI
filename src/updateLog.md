### 第一次更新

#### 新加文件

```
login.py
updateLog.md (本文档)
```

#### 说明

- login.py：除了登录成功后切换到日历界面，其余功能已实现，具体包括：
  - 登录时，输入不合法或密码错误的反馈信息
  - 注册时，不同阶段的反馈信息
  - 调用src/backend/method.py中的几个接口
  - 修改了method.py和，Module.py中的import(要输入路径src/backend/method，直接from method import * 会报错)

### 2022-08-05

#### login.py到calendar.py的切换

- login.py中，在成功登录后结束自身程序，直接运行calendar.py
- 为了在calendar.py得到登录用户的数据，login.py最后将登录的用户名和密码写入一个临时文件".name_password.tmp"
- 在calendar.py一开始运行就读该文件，读完后把该文件删除
- 在CalenWindow类中新增user属性，并用```self.user = loginUser(username, password)```得到登录用户的对象

#### 记住密码功能

- 如果上一次登录勾选记住密码，则会在下次登录时直接显示用户名和密码
- 如果上一次没勾选记住密码，则只会在下次登录时显示用户名
- 第一次登录啥都没有
- 信息保存在```.login.log```(可以删掉它测试第一次登录的情况)

#### 搞了三个gitignore


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

#### 搞了frontend目录的个gitignore(哦，这是本地的)
还有根目录的
本来要搞其他目录，但发现backend目录的.data文件夹不能删



### 2022-08-08

转自微信群：

- 我先把昨天写的commit后push上去

- 我把原来的AddTaskDialog类分成两个类：ddDailyTaskDialog， AddNormalTaskDialog
- 然后我发现现在可以在加代办时，起始时间大于截止时间，我再加一个警告上去
- 然后就是我感觉可以把一些类放到别的文件里
- 我这些东西弄完后再push一次？



### 2022-08-08 17：42

Author:匡莉

- 新增文件夹Icon（有更好看的图标也可以接着换，嘿嘿）

- 为日历页面增加了工具栏（以图标形式显示）
- 为AddTaskDialog的页面增加图标以及新增类别栏及内容栏
- 普通任务删去截止时间，日常任务删去开始时间
- 将上述提到的两个类进行了抽象，统一继承父类AddTaskDialog

问题：

- 消息盒子不能改变页面大小，图标有点报看（后期考虑还是改窗口？



### 2022-08-10 17:06

Author:匡莉

- 完善了taskLabel文件
  - 对于编辑按钮，弹出相应的编辑对话框，新增`editTask.py`
  - 开始按钮设为两种状态，按下或弹起
  - 完成设置为勾选框
  - 新增了删除按钮以及相应的消息盒子
- 后端
  - 修改了`class Task`的定义，删除了`deadline`，统一为了`time`
  - 为种类新增了枚举变量
- 待办：
  - 主页面右侧的滚动条区域，以及如何让taskLabel控件固定大小
  - 上述新增按钮对应函数待补充


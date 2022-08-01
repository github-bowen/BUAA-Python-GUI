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

# Calendar in Python

[中文版](./README_zh.md)

<img src="forReport/报告封面.png" style="zoom:%;" />

## 0. Run

Clone the project from the github repository (only branch `main` is needed):

```shell
git clone -b main --single-branch https://github.com/NormalLLer/BUAA-Python-GUI.git
```

Installation dependencies:

```shell
pip install -r requirement.txt
```

Switch directory:

```shell
cd ./src/frontend
```

Run:

```shell
python welcome.py
```

## 1. Experimental tasks

Selected topic: Topic 4

Contents: Task Scheduler

Requirements: Design an application to help users plan daily schedules, log tasks reasonably to plan time



## 2. The task has been completed

- **Basic Experimental Requirements**

   - Experiment requirement a: task adding system

     The user can add a new task through the button on the toolbar, and set the corresponding attributes of the task, such as: title, content, deadline, importance, category, etc.

   - Experiment Requirement b: Show daily quests

     When the user selects a specific date in the calendar control, the tasks for that day will be displayed on the right half of the main page

   - Experimental Requirement c: Task Completion Confirmation

     The task control contains a completed check box, and the task is set to complete after checking

   - Experiment Requirement d: Calendar System

     Add a calendar control on the left side of the main interface of the program

   - Experimental Requirement e: Task state difference.

     Divide task status into four categories: not started, in progress, completed, overdue

   - Experimental requirement f: task scheduling

   - Experimental requirement g: user login system

- **OPTIONAL EXPERIMENTAL REQUIREMENT**

   - Optional requirement a: The to-do list system can filter and display tasks based on time.
   - Optional Requirement b: Classification of tasks. Set task categories, including work, study, entertainment, sports, and other five categories.
   - Optional Requirement c: Support for daily tasks. Make daily tasks automatically appear in the task list every day by specifying the hours and minutes at which they appear
   - Optional requirement d: Weighted task scheduling. Through the two sorting factors of task importance and deadline, automatically plan future tasks, arrange the order of completion of tasks, and present a list of completion order for users
   - Optional task e: support data review, and display user data in the form of charts, etc.

    

## 3. Overall design plan

We divide the entire task into two parts, the front end and the back end. The back end is responsible for interacting with the database, saving data, and providing data to the front end. The front end is responsible for accepting the data provided by the back end and displaying it in a graphical interface.

### 3.1 Frontend

The front end mainly designs two modules, one is the user login system interface including the boot animation, and the other is the main interface of the task manager we designed, namely `login` module and `calendarFront` module

#### 3.1.1 User login system

The login interface is as follows:

<img src="forReport/login.png" style="zoom:40%;" />

The left side is the icon we designed for the task scheduler (printed with the word "Task manager"), and the right side is the input part, where the user can enter the user name and password. Among them, there are light gray text prompts in the user name input box and password input box, informing the relevant specifications about inputting the user name and password. Below the two input boxes, there are two check boxes of "Remember password" and "Show welcome animation". If a check box is checked, the next time you log in to the software, it will be displayed according to the selected behavior (for example: if "Remember Password" is checked, the password box will be automatically entered when you log in next time password; if the "Show welcome animation" is removed, the 3-second welcome animation will not be displayed at the next login).

In addition to the login interface itself, a series of operations of "registration" is also the focus of the user login system.

After clicking Register, three pop-up windows, "Enter new user name", "Enter new password", and "Repeat password", will be displayed in sequence. The latter two have restrictions on the new password set. If the input password does not conform to the specification (such as: the password length is not between 6-15 digits, the password protects special symbols other than numbers and letters), a corresponding error prompt box will pop up to inform the user of the non-compliance with the specification. Similarly, if the entered password is different from the previous one at the third "Repeat Password", a corresponding error prompt box will also pop up.

In addition, you can see that there is a small box on the right side of the password box on the login interface. Long press the box to display the password, and move the mouse to display the password characters as "$\bullet$".

#### 3.1.2 Task Manager main interface

As can be seen from the figure below, the main interface can be divided into three parts, namely the toolbar, the calendar module, and the task display module of the day

<img src="forReport/主页面.png" style="zoom:50%;" />

- toolbar

   In the calendar main interface, the upper left is the toolbar:

   <img src="forReport/工具栏.png" style="zoom:80%;" />
   
   The icons correspond to `Add Task`, `Filter Task`, `Refresh Task`, `Scheduling Task` from left to right, and there are five functions of data review.

   - **Add task**: Relying on the `addTask.py` file, click the corresponding button on the toolbar to trigger the display of the `SelectTaskDialog` control, asking the user whether to add a daily task or a general task

     <img src="forReport/select.png" style="zoom:60%;" />

     Clicking different buttons triggers their corresponding dialog boxes, which are the `AddDailyTaskDialog` class and `AddNormalTaskDialog` class inherited from the `AddTaskDialog` class.
     The user needs to fill in the name, details, importance and category of the created to-do in sequence on the page, as shown in the following figure

     <img src="forReport/创建新的日常待办.png" style="zoom:50%;" />

     The difference between the dialog boxes of daily tasks and general tasks is that the user fills in the deadline (including year, month, day, hour and minute) on the general task page, but only fills in the specific date when the task should start every day on the daily task page. time.
     After the user has entered the relevant attributes of the task, clicking the confirm button in the dialog box will trigger the `checkDate` function to judge the validity of the input data. After passing the validity check, the system will create a `taskLabel` according to the attributes and automatically call `taskDisplay` , display the task on the right side of the main interface, see 4.1 for detailed design

​    

   - **Filter task**: Relying on the `taskFliter.py` file, click the corresponding button on the toolbar to trigger the display of the control, ask the user the start date and end date of the filter, and then pass it to the backend to read user data to display

     Since the filter is based on date, and daily tasks occur every day, here is the general task list

     <img src="forReport/筛选.png" style="zoom:50%;" />

   - **Refresh tasks**: We divide tasks into four states: not started, in progress, completed and expired. We believe that the start and completion of a task is determined by the user, so only the state **Expired** is determined by the system. The interface that the user does not operate is static, but as time goes by, some unstarted tasks may have exceeded the deadline and become expired, so we design the `refreshAndDisplay` function, pass the current time to the backend, and call The back-end function automatically judges whether the task has expired, and the front-end re-reads the changed data and displays it on the page

   - **Scheduling tasks**: Here we only schedule the tasks of the day, and sort them according to the weighted importance and time, with the importance as the first keyword and time as the second keyword, get the sorted task list, and then in The front end calls the function for display

   - **Data Review**: Draw a pie chart based on the user's to-do categories for the day, and a line chart based on the number of tasks completed by the user in the last seven days, so as to clearly and intuitively display the user's task status

     <img src="forReport/数据回看.jpg" style="zoom:50%;" />

​    

- Calendar module

   Using the `QCalendarWidget` control of `PyQt5.QtWidgets`, you can get the date selected by the user, and add a label at the bottom to display the details of the date, making the page layout simple and elegant

- task display

   See 4.1 for detailed design

  

### 3.2 Backend

The backend adopts object-oriented method design, which is mainly divided into the following two parts

* The `Method` module is a module used for user registration and login

* `Module` module, the class that stores data, consists of the following classes

   * User class

     Each user who logs into the system corresponds to a User object. The front end can call the method of the User object to obtain task information.

   *Calender class

     The Calender class represents a monthly calendar and organizes Tasks. Calendarer stores the to-do information of a certain month, and uses a Python dictionary to match the date with the tasks of the day.

     The Calender object is invisible to the front end and is organized by the back end, which ensures the simplicity of the interface and reduces the coupling between the front end and the front end.

   * Task class

     The Task class is used to represent to-dos and is the bottom class in this project. The Task class stores the basic information of a to-do, and its attributes include the title, content, time, category, and current status of the to-do. The Task class can also convert the task object and json into each other to realize the storage and reading of the task.

   * DailyTask(Task) class

     DailyTask is a subclass of Task, which is used to represent daily tasks. In addition to the attributes of general tasks, DailyTask also saves the date when this task has been completed before. See 5.1 for the specific introduction of this part.
   
    

## 4. Innovation

### 4.1 Display of tasks

#### 4.1.1 Task label design

From left to right are icons, to-do status, to-do name, to-do time, edit button, status switch button and delete button

- Icon: Represents the category and importance of the task. When the task is more important, the color of the icon is darker, and the style of the icon is related to the to-do category
- Edit button: After the user clicks it, the task edit box will pop up, which is similar to the task add box, the difference is that the edit box starts to display various attributes before the task
- Status switching button: In order to make the layout more beautiful and give users a better sense of experience, the start and end buttons are combined. When the user starts an unfinished task, the text of the check box will change to "Complete", and the check box will be unchecked select

In order to make it easier for users to distinguish the status of the task, the color of the label text is set to gray for the task of "Completed", and a strikethrough is added

#### 4.1.2 Main interface task layout

Considering the size of the interface and the actual needs of users, a vertical scroll bar is added to the task display area on the right side of the main interface, so the number of realistic tasks is unlimited

When the selected date has no tasks, a prompt message will be displayed



### 4.2 Data storage and update

#### 4.2.1 Data storage

The backend uses the database `TinyDb` to store data. `TinyDb` is a text-based database. Parsing the data to be stored into a dictionary, list or other basic data types in python can be used as a record of the TinyDb database. The stored data is in json format, and each user corresponds to a json file.

When the user logs in, in order to save resources, only the database object is created without loading and processing the data in it. When the user needs to obtain the data of a certain month, the corresponding Calender object is created, and the Calender object is initialized from the database. The data corresponding to the current month's Task is read in, and the Task class parses it into a Task object and stores it in the Calender. This "reload when needed" processing method makes it unnecessary for our program to load all tasks every time it starts, and it is no problem for long-term use.

After reading the data, we will store the data in the Task object and organize it with Calender. This kind of processing is equivalent to a cache of data, and it is not necessary to read from the file every time.

#### 4.2.2 Data update

During the running of the program, the database and the data in the process memory are updated synchronously, that is, when the Task object is modified, its corresponding data items are synchronously modified, which can effectively prevent the program from being accidentally terminated compared to saving it in a file at the end of the program. resulting in loss of information.



### 4.3 Update of task status

The main issue involved here is when should the status of a task be set to "overdue". Our approach is that every time the front-end obtains the task list of a certain day from the back-end, we will scan today's tasks, and if the current time has passed the deadline of the task, set its status to expired.

For DailyTask, as mentioned above, the DailyTask object represents the status of the daily task of "today", and the year, month, and day corresponding to its time are all today's year, month, and day, so the judgment method is the same as that of ordinary tasks.



### 4.4 Judgment of abnormal situation

We have set the `showWarning` class. When the user interacts with the program abnormally, a warning window of the corresponding problem will pop up, allowing the user to reset the relevant settings.

For example, the to-do name cannot be empty, the set deadline cannot be earlier than the current time, tasks that have expired cannot be started, tasks that have not yet started cannot be completed, etc.



## 5. Experiment summary

Difficulties encountered in the experiment and our solutions:

### 5.1 Processing of daily tasks

#### 5.1.1 Storage of daily tasks

For daily tasks, because daily tasks are available every day and the content is the same, it is a waste of resources to save one copy every day, so we think it is not necessary to save multiple times, you only need to save a DailyTask in the User object, and its status represents the daily task status of the day (in progress, not started, completed, expired).

Generally speaking, daily tasks only need to store the start time (hour, minute, and second), and do not need to store the year, month, and day. However, in order to be consistent with general tasks, we set the year, month, and day of the DailyTask attribute time to the year, month, and day of the current day. This processing method has two functions, one is to decide whether the dailyTask should be reset to not started (dailyTask will be reset to not started every day), and the other is to decide when a task should be updated to an expired state . This unification simplifies the procedure.

#### 5.1.2 Differentiation of task status

For daily tasks that have been completed, we will store the date of completion of this task in the DailyTask object, which means "this DailyTask has been completed on a certain day". This is to get the completion status of the DailyTask before today. If you want to get the status of daily tasks for a certain day, call the `getState` method. If this date is before today, check to see if this day is in the list of completed dates for this task. If there is, the task is considered completed on that day; if not, it is considered overdue. If the date is today, directly return the status of the DailyTask object. If the date is after today, the task is considered unstarted. Object-oriented polymorphism is used here. The `getTask` method of the Task object directly returns the `State` property of the object, while the `DailyTask` object needs to be judged according to the date.

Another question is how to toggle the status of daily tasks to "not started" at the beginning of each day. Our solution is to record the date when the DailyTask was last created. If today’s date is different from the last saved date, it means that the last time the DailyTask was used is not today, and the status of the DailyTask needs to be reset to the unstarted state. On the contrary, it means that the last time DailyTask was used is today, and its status will not be changed.

The daily task is not displayed on the date before the daily task was created, which is more in line with the user's intuition. Our processing method is to record the creation date of the task, and only the to-do after the creation date will be added to this DailyTask.

#### 5.1.3 Polymorphism and inheritance of tasks

In our experiments, tasks are divided into general tasks and daily tasks, both of which have high attribute overlap, and both have attributes: name, details, importance, and category. The difference is that from the user's point of view, they prefer the manager to provide reminders of daily tasks (such as clocking in), that is, the start time of the task; and for general tasks, users hope that the manager is more like a memo (such as the schedule of group jobs). Deadline), to remind the end time of the task. And the former should only contain time (hour, minute and second), while the latter should include date and time.

Therefore, in terms of front-end page design, there are differences in the time editors of the two tasks, but the other aspects of the two are very similar. At this time, if you write separate `AddDailyTaskDialog` and `AddNormalTaskDialog` classes, the code appears redundant. When making changes to the same part, two classes need to be changed at the same time, which reduces the robustness of the code. From the perspective of object-oriented encapsulation, inheritance, and polymorphism, the `AddTaskDialog` class is abstracted based on this. In the subsequent code iteration process, it is found that the window for editing tasks needs to be added. At this time, it is only necessary to make small changes in the `AddTaskDialog` class.



## 6. Course learning summary

### 6.1 Course Harvest

During the study of this course, I became more proficient in the use of python. In my usual homework, I have initially come into contact with some algorithms (especially dynamic programming), and practice helps to master them. Since this course is taught in English, I not only improved my English proficiency, but also got to know the English expressions of some terms, which I could not learn in other courses. In the process of completing the big assignment, we learned the basic method of using PyQt5 to write a graphical interface. This part of knowledge should be very practical.

### 6.2 Difficulty analysis

The difficulty of daily homework mainly lies in programming and algorithm knowledge, but the topics are relatively classic, and I have learned a lot of methods from them. The difficulty of large assignments mainly lies in the use of PyQt5. Since we have not touched GUI before, we need to consult more information in this regard.

### 6.3 Teacher Evaluation

The teacher's lectures are clear and interesting, and there is a certain amount of expanded content.

### 6.4 Teaching assistant evaluation

The teaching assistants are serious and responsible, and will promptly answer our questions in the group.

### 6.5 Evaluation of the current course teaching content and suggestions for further improvement of the course

I feel that there is not much connection between after-school homework and the lecture content, so I can adjust the after-school homework appropriately and add more things related to the lecture content.



## 7. The main reference materials

PyQt5 Tutorial: [Hello World - PyQt Chinese Tutorial (gitbook.io)](https://maicss.gitbook.io/pyqt-chinese-tutoral/pyqt5/hello_world)

Qt5 reference: [Qt 5.15](https://doc.qt.io/qt-5/)

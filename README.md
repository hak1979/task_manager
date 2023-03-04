# A program for a small busoness to manage tasks
This program is designed in mind for a small business, with a few employees, wehre
the tasks assigned to each employee can be managed.

There are two versions of the program in the folders original ad improved. As the name
implies, I have taken the original design and improved upon it. 

## How the orginal task manager works
The main prorgram runs in python - task_mamager.py

The program works with two text files users.txt and tasks.txt, where the user and task
data is stored and read from respectively.

users.txt stores the user name and passwords seperated by a comma; one user per line. 

tasks.txt stores all the tasks that the team is working on. Each task is stored on a
seperate line which includes the folloowing data:
* item The username of the person to whom the task is assigned.
* item The title of the task.
* item A description of the task.
* item The date that the task was assigned to the user.
* item The due date for the task.
* item Either a ‘Yes’ or ‘No’ value that specifies if the task has been
completed yet.

The program requires the users to login, where the usernames and passwords are
verified from the users.txt file. 

![login screen](/Original/images/login.jpg)

The users are able to register a new user, add new tasks, view all the tasks and the task assigned to them,
and the statistics of the tasks assigned. The statistics are only viewable by the admim user.

![menu screen](/Original/images/menu.jpg)

An example of how tasks are viewed:

![tasks screen](/Original/images/view_all.jpg)

How statistics are viewed:

![statistics screen](/Original/images/statistics.jpg)

When a new user is registered the details are written on the users.txt file. As are the new tasks appended to
the tasks.txt file. The main input/output mechanism of data is driven by file read and write operations. 

## How the program was improved

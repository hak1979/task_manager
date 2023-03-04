# A program for a small business to manage tasks
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
The original program was enhanced by adding new functionality. In addition to all the options in the orignal
program, the admin now can view an enhaced version of the statistics, generate reports for the tasks and user tasks
statistics in two seperate files task_overview.txt and user_overview.txt respectively. Registering new users is also
restricted to the admin. The admin is also able to reset the database to it's original form (if too many entries
are made when trying the system out, this is a quick way to load the original database.)

The new menu screen:

![menu screen](/Improved/images/menu.jpg)

An exmaple how how the statistics are viewed now:

![statistics screen](/Improved/images/statistics.jpg)

As it can be seen from the two screenshots, not the statics are more comprehensive and gives detailed information per user. 

One of the biggest changes made was that intsead of using text files to store and read data from, now it is driven by a database;
task_db. The database runs on SQLite. 

The data is now stored on three realtional tables:

&ensp;&ensp; users table-> user_id, user_name, user_password

&ensp;&ensp; tasks table-> task_id, task_title, task_description, assign_date, due_date

&ensp;&ensp; tasks_assigned-> task_id, user_id, task_complete.

The passwords are now hashed/encryted and stored in the table for security.

# Running the program
Before the programs are run ensure that sqlite3 and passlib libraries are installed in your python environment. 

To be able to log into the programs the usernames and passwords are in the users.txt file - it is an exmaple afterall!

Run the programs from their respective directories by typing python task_manager.py or pyhon task_manager2.py

Follow the on screen instructions to log in, and try out the different menu items.








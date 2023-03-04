'''
A program that allows for users to be added to a system with their unique usernames
and passwords. Tasks can be assigned to, modified and viewed by the users.

'''

# =====importing libraries===========
import sys
import os
import re
import sqlite3
from datetime import date, datetime
from operator import itemgetter
from os import mkdir
from passlib.hash import sha256_crypt

# =====Functions===========


def load_database():
    ''' A function that loads the database task_db 
        and returns the databas connection'''

    # try to connect to the database
    try:
        database = sqlite3.connect('data/task_db')

    # if the file does not exist in selected path
    except sqlite3.OperationalError:
        # cretae a folder called data
        mkdir('data')

    finally:
        # connect/create the database in the path
        database = sqlite3.connect('data/task_db')

    return database


def reset_database():
    ''' A function to populate the task_db database with relational tables
    users, tasks and task_assisgn from users.txt and tasks.txt files.

    Only run if no database present, or if you would like to start with a 
    unmodified database.'''

    # ask admin to comfirm their choice
    print("\nThis process cannot be undone.")
    while True:
        confirm_choice = input(
            "Are you sure to reset the database y or n?").strip().lower()

        if confirm_choice == 'y':
            confirm_password = input(
                "Please enter your password to confirm: ")

            password = cursor.execute(
                '''SELECT user_password FROM users WHERE user_name = "admin"'''
            ).fetchone()[0]

            if sha256_crypt.verify(confirm_password, password) is True:

                # delete all tables if they exist
                cursor.execute(
                    '''DROP TABLE IF EXISTS users'''
                )

                cursor.execute(
                    '''DROP TABLE IF EXISTS tasks'''
                )

                cursor.execute(
                    '''DROP TABLE IF EXISTS task_assign'''
                )

                # create the tables again
                cursor.execute(
                    '''CREATE TABLE IF NOT EXISTS users(
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_name TEXT NOT NULL,
                        user_password TEST NOT NULL
                    )'''
                )

                cursor.execute(
                    '''CREATE TABLE IF NOT EXISTS tasks(
                        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        task_title TEXT NOT NULL,
                        task_description TEXT,
                        assign_date REAL,
                        due_date REAL
                    )'''
                )

                cursor.execute(
                    '''CREATE TABLE IF NOT EXISTS task_assign(
                        task_id INTEGER,
                        user_id INTEGER,
                        task_complete TEXT,
                        FOREIGN KEY (task_id) REFERENCES tasks(task_id),
                        FOREIGN KEY (user_id) REFERENCES users(user_id)
                    )'''
                )

                db.commit()

                # populate the users table from user.txt file
                users_list = access_file('user.txt', 'r+')

                for user in users_list:
                    user = user.strip().split(', ')

                    password = sha256_crypt.hash(user[1])
                    cursor.execute(
                        '''INSERT OR IGNORE INTO users (user_name, user_password) VALUES (?,?)''', (
                            user[0], password)
                    )

                db.commit()

                # populate the tasks table from the data in tasks.txt file
                tasks_list = access_file('tasks.txt', 'r+')

                for task in tasks_list:
                    task = task.strip().split(', ')

                    user_id = cursor.execute(
                        '''SELECT user_id FROM users WHERE user_name=?''', (task[0],)).fetchall()[0][0]

                    # dates are stores in the database is formatted as year-month-day. This is the best
                    # way to store the dates as sqlite is btter able to sort and compare dates in this format.
                    # dates are formatted as %Y-%m-%dd
                    assign_date = datetime.strptime(
                        task[3], '%d %b %Y').strftime('%Y-%m-%d')

                    due_date = datetime.strptime(
                        task[4], '%d %b %Y').strftime('%Y-%m-%d')

                    cursor.execute(
                        '''INSERT OR IGNORE INTO tasks (task_title, task_description,
                        assign_date, due_date) VALUES (?,?,julianday(?),julianday(?))''', (
                            task[1], task[2], assign_date, due_date,)
                    )

                    # populate the task_assign table
                    task_id = cursor.execute(
                        '''SELECT task_id FROM tasks WHERE task_title=?''', (task[1],)).fetchall()[0][0]

                    cursor.execute(
                        '''INSERT OR IGNORE INTO task_assign (task_id, user_id, task_complete) 
                        VALUES (?,?,?)''', (task_id, user_id, task[5],)
                    )
                db.commit()

                print("\nThe task_db has been reset.")
                break

            print("\nYou did not enter a valid password.")
            break
        if confirm_choice == 'n':
            break

        print("Please enter 'y' or 'n' only to indicate your choice.")


def search_for_user(username):
    '''' Function to search if user exits in users table
    returns user_id, user_name and user_password'''

    # from the users table search if the usermane exists
    searched_user = cursor.execute(
        '''SELECT * FROM users WHERE user_name=?''', (
            username,)
    ).fetchall()

    return searched_user


def user_login():
    ''' Function that will allow a user to login.
        user will repeatedly be asked to enter a valid username and password until
        they provide appropriate credentials.'''

    # while loop to validate username and password
    while True:
        # ask user to enter their username - use strip to remove any whitespaces in the inputs
        user_name = input("Please enter your username: ").strip().lower()

        # if username exists in users table ask for password
        user_exists = search_for_user(user_name)

        if user_exists != []:
            # the user will get three tries to enter correct password
            for tries in range(3):
                # user enters password
                password = input("Please enter your password: ").strip()

                # if the password corresponds to the user key the break password loop
                if sha256_crypt.verify(password, user_exists[0][2]) is True:
                    # print sucessful login message
                    print("\nCorrect login details! Loading...\n")

                    # return the user_id and username of logged in user
                    return user_exists[0][0], user_exists[0][1]

                # after the third try, the program will ask for the username again
                if tries == 2:
                    print("Too many tries, start again.")
                    break

                # otherwise display an error message

                print("Wrong password entered")

        # if there is no username in dictionary print the error
        else:
            print("No such user name exists. Please try again.")


def reg_user():
    '''function to add a new user to the users table '''

    print("\nYou will be registering a new user.\n")

    # using a while loop add the details of the new user
    while True:
        # ask to enter a new username
        new_username = input(
            "Please enter a new username: ").strip().lower()

        # seach the users table if user exists
        search_user = search_for_user(new_username)

        # if the username already exists ask if to enter another username, otherwise go to
        # main menu by breaing out of the loop
        if search_user != []:
            print(f"\nThe username {new_username} already exists.\n")
            while True:
                try_again = input(
                    "Would you like to try another username, y or n: ").lower()
                if try_again == "n":
                    return "\nGoing back to main menu\n"

                if try_again == "y":
                    break

                print("Wrong input: Enter y or n")
        else:
            break

    # once new username entered ask to enter new password
    new_password = input("Please enter a password: ").strip()
    while True:
        # re_enter the password
        check_password = input(
            "Please re-enter the password: ").strip()

        # check that the entered passwords match
        if new_password == check_password:
            # encrypt the new password
            new_password = sha256_crypt.hash(new_password)

            # insert the new user into users table
            cursor.execute(
                '''INSERT INTO users (user_name, user_password) VALUES (?,?)''', (
                    new_username, new_password)
            )

            db.commit()

            # print the sucessfully added message and break the loop
            return f"\nYou have registered {new_username} successfully.\n"

        print("The passwords do not match.")


def menu_options(user_name):
    ''' function presenting an appropriate menu depending on the user '''

    # the list for the menu options
    menu_list = ["\nPlease select one of the following Options below:",
                 "r - Registering a user", "a - Adding a task", "va - View all tasks",
                 "vm - view my task", "gr - generate reports", "ds - Statistics", "rd - reset database", "e - Exit\n:"]

    # if the user is admin the statistics and registering new user options visible in menu
    if user_name == "admin":
        # replace e - Exit\n from menu string with "s - Statistics\ne - Exit\n:" using
        # regualr expressions function re.sub
        menu_string = "\n".join(menu_list)

    else:
        # choosing the indexes for the menu options for the non admin users to see
        user_options = [0, 2, 3, 4, 8]

        # using itemgetter from the operator library to get the correct options from menu_list
        # to generate a menu_string for non admin users
        menu_string = "\n".join(itemgetter(*user_options)(menu_list))

    return menu_string


def view_tasks(menu_option, logged_in_user):
    ''' A function to view a list of the tasks stored tasks table.
        If type is va - view all tasks,
        if type is vm view tasks assigned to the user only.'''

    # task_list to store the tasks for vm and va menu options
    # to be used in the task_printer function
    if menu_option == 'vm':
        task_list = cursor.execute(
            '''SELECT tasks.task_id, users.user_name, tasks.task_title,
            tasks.task_description, date(tasks.assign_date), date(tasks.due_date), 
            task_assign.task_complete FROM task_assign 
            INNER JOIN tasks ON tasks.task_id = task_assign.task_id
            INNER JOIN users ON users.user_id = task_assign.user_id
            WHERE task_assign.user_id=?''', (logged_in_user[0],)
        ).fetchall()

    elif menu_option == 'va':
        task_list = cursor.execute(
            '''SELECT tasks.task_id, users.user_name, tasks.task_title,
            tasks.task_description, date(tasks.assign_date), date(tasks.due_date),
            task_assign.task_complete FROM task_assign
            INNER JOIN tasks ON tasks.task_id = task_assign.task_id
            INNER JOIN users ON users.user_id = task_assign.user_id'''
        ).fetchall()

    else:
        # if wrong menu item, not va or vm, then print an error message
        print("Please make sure the type is either va or vm")
        return None

    # if tasks exists call the task_printer to print the tasks on screen
    # folowed by modify_task to allow the user to edit tasks
    print(task_printer(task_list))

    # Following the listing of tasks the user gets an option to edit tasks
    # if the menu enetered is va, only admin can modify all tasks, otherwise
    # the user can only modify their own tasks.
    if menu_option == 'va' and logged_in_user[1] == "admin":
        modify_task(task_list)

    if menu_option == "vm":
        modify_task(task_list)

    # once all is done print an infomative line
    print("\nGoing back to main menu")


def modify_task(task_list):
    '''A function that allows the users the edit tasks or
        mark them as complete. The function takes the task list'''

    # bool task_found is set to false, and it wll be true if selected task
    # by user exists
    task_found = False

    # this will loop until the task is found by task ID
    while task_found is False:
        # ask user to select task by task id number
        select_task = input(
            "Please select the task ID to edit by or -1 to exit: ")

        # -1 entry will go to main menu
        if select_task == '-1':
            break

        # for reference: [0] - task id, [1] - username, [2] - title, [3] - description,
        # [4] - date assigned, [5] - due date, [6] - task complete
        for task in task_list:
            if select_task == str(task[0]):
                # set task_found bool to true
                task_found = True

                # call the edit_options function to change status or edit task
                edit_options(task)

        # if user did not enter a valid task id number show error message
        if task_found is False:
            print(f"The task with task ID {select_task} does not exist")


def edit_options(current_task):
    ''' a function that gives the use the options to edit tasks.'''

    # information for user before asking for input
    print("\nPlease select one of the options:\n\n"
          "Option 1 - Change task complete status\n\n"
          "Option 2 - Edit the task\n")

    # loop to take in user input and act on selection
    while True:
        select_option = input("For the option please enter 1 or 2: ").strip()

        # if user selected to change task completion
        if select_option == '1':
            print("\nYou have selected to change the task completion status\n")

            # this wil call the mark_complete function to edit task completion
            answer = mark_complete()

            # if the current task completion in tasks.txt is different to user answer
            # then up_date the task completion parameter and set task_changed to true
            if current_task[6] != answer:
                cursor.execute(
                    '''UPDATE task_assign SET task_complete=?
                    WHERE task_id=?''', (answer, current_task[0])
                )
                db.commit()
                print(
                    f"\nTask {current_task[0]} completion has been set to {answer}\n")
            break

        # if the user selected to edit the task
        if select_option == '2':

            # if the task is marked as complete then can't edit the file
            if current_task[6] == "Yes":
                print(
                    "\nYou cannot edit your selected task, as it has been marked as complete.\n")
            else:
                print(
                    f"\nYou have selected to edit the task number {current_task[0]}\n")

                # this calls the edit_task function which return True if any
                # changes have been made
                edit_task(current_task)
            break

        # if no valid option selected the user will see this error message
        print("You have entered an incorrect option")


def edit_task(current_task):
    ''' A function that asks the user if they would like to edit the
        username of the person to whom the task is assigned and the due
        date of the task. Function returns true if any changes have been made.'''

    # loop to ask the user to change user assigned to task
    while True:
        assign_option = input(
            "Would you like to change the assigned user "
            "for the task, y or n: ").strip().lower()

        # ask if the user wants to edit the user assigned to task,
        if assign_option == 'y':
            while True:
                # ask user for new assigned user
                edit_user = input(
                    "To assign the task to another user, ",
                    "please enter their username: ").strip().lower()

                # check that the user exists otherwise print error message
                # if the user exists update the user name in the task list current_tasks
                user_exists = search_for_user(edit_user)

                if user_exists != []:
                    cursor.execute(
                        '''UPDATE task_assign SET user_id=?
                        WHERE task_id=?''', (user_exists[0][0], current_task[0])
                    )
                    db.commit()
                    print(
                        f"Task {current_task[0]} is now assigned to {edit_user}.")
                    break
                # else:
                print(f"A user with the user name {edit_user} does not exist.")

            # break out of loop to progress to the next section of edit_task
            break

        # if n selected, do nothing, break out of loop as no changes to be made
        if assign_option == 'n':
            break

        # if wrong input then show error message
        print("You can only type y or n")

    # ask if user want to edit the due date of task
    while True:
        assign_option = input(
            "Would you like to edit the due date for the task, y or n: ").strip().lower()

        # if the user selects to edit the due date then the entry checked for
        # format be calling the date_input function, and the ensuring the due
        # date is later than the assigned date by using the compare_dates function
        if assign_option == 'y':
            edit_due_date = date_input()
            assign_date = datetime.strptime(
                current_task[4], '%Y-%m-%d').strftime('%d %b %Y')
            while compare_dates(assign_date, edit_due_date) is True:
                print("\nThe due date cannot be before assigned date.")
                edit_due_date = date_input()

            # once date is correct update the due date on the task list current_task
            # and task_changed is set to true

            # format dates to year-month-day before updating table
            due_date = datetime.strptime(
                edit_due_date, '%d %b %Y').strftime('%Y-%m-%d')
            cursor.execute(
                '''UPDATE tasks SET due_date=?
                WHERE task_id =?''', (due_date, current_task[0])
            )
            db.commit()
            print(f"\nThe task due date has been updated to {edit_due_date}")
            break

        # break out of loop if no editing required
        if assign_option == 'n':
            break

        # prints error message for not entering y or n
        print("You can only type y or n")

    # returns bool: True if task edited, False for no changes
    # return task_changed


def mark_complete():
    ''' Function that asks use if the task if complete or not and returns answer.
        A helper function for modify_task function'''

    while True:
        # ask the user for their answer,
        task_complete = input("Is the task complete y or n? ").strip().lower()

        # if it's y return Yes
        if task_complete == 'y':
            return 'Yes'

        # if it's n return No
        if task_complete == 'n':
            return 'No'

        # if the user enters anything else, then display the error message
        print("You can only type y or n")


def date_input():
    ''' A function that asks for the due date of the task whilst checking that
        the format is correct. The function returns the formatted date'''

    while True:
        # ask user to enter the date in the dd mm yyyy format
        print("\nThe due date should be entered in the format dd mm yyyy",
              "\n\nFor example 2nd October 2022 should be written as 02 10 2022\n")

        input_date = input("Please enter the due date as dd mm yyyy: ").strip()

        # check that it is the correct format, if not ask to input again otherwise break loop
        if not re.match(r'[0-3][0-9] [0-1][0-9] [0-9]{4}$', input_date):
            print("\n -> Wrong date format. Please enter it correctly.")

        else:
            try:
                # format the entered date to correct format, eg 10 Dec 2023
                correct_date = datetime.strptime(
                    input_date, '%d %m %Y').strftime('%d %b %Y')

                # leave loop now that correct date format entered
                break

            except ValueError:
                # if the format is not correct,eg if they enetered 35 15 2000, then print error
                print("\nWrong date format. Please enter it correctly.")

    return correct_date


def task_printer(task_list):
    ''' A helper function to view_tasks for printing the tasks on the screen
        in a user friendly way. The function returns the string my_tasks'''

    # if no tasks exists
    if task_list == []:
        print("_____________________________________________________________________\n\n"
              "There are no tasks to display."
              "\n_____________________________________________________________________\n")
        return None

    # the string to be printed out for each task, formatted for va or vm use.
    task_string = "Task ID:\t\t{}\nTask:\t\t\t{}\nAssigned to:\t\t{}\
                   \nDate assigned:\t\t{}\nDue date:\t\t{}\n"\
                    "Task complete?\t\t{}\nTask description:\n\t{}\n"

    # empty string to take the formatted task string to be viewed by user
    my_tasks = "_____________________________________________________________________\n\n"

    for task in task_list:

        # for reference: [0] - task id, [1] - username, [2] - title, [3] - description,
        # [4] - date assigned, [5] - due date, [6] - task complete

        # format dates to day month year when displaying on screen
        assigned_date = datetime.strptime(
            task[4], '%Y-%m-%d').strftime('%d %b %Y')

        due_date = datetime.strptime(
            task[5], '%Y-%m-%d').strftime('%d %b %Y')

        my_tasks += task_string.format(task[0], task[2], task[1],
                                       assigned_date, due_date, task[6], task[3])

        # add final seperator line to the last task list to look visually nicer
        my_tasks += "\n_____________________________________________________________________\n\n"

    return my_tasks


def compare_dates(date_1, date_2):
    '''a function that compares two dates. if the date_1 is greater or
        equal to date_2 it will return True, otherwise it will return False.'''

    # format time string to day month year as numbers
    first_date = datetime.strptime(
        date_1, '%d %b %Y').strftime('%d %m %Y')

    # day month and year casted as integers
    first_date = [int(n) for n in first_date.split()[::-1]]

    # using datetime the date is in year month day format, eg 2000 10 02
    first_date = datetime(
        first_date[0], first_date[1], first_date[2]).date()

    # format time string to day month year as numbers
    second_date = datetime.strptime(
        date_2, '%d %b %Y').strftime('%d %m %Y')

    # day month and year casted as integers
    second_date = [int(n) for n in second_date.split()[::-1]]

    # using datetime the date is in year month day format, eg 2000 10 02
    second_date = datetime(
        second_date[0], second_date[1], second_date[2]).date()

    # if the first date date_1 is later than or same date as date_2 return true
    if first_date >= second_date:
        return True

    # for all other scenarios return False
    if first_date < second_date:
        return False


def add_task():
    '''function that will allow a user to add a new task to task.txt file'''

    # use a loop to enter and check the username to assign task
    while True:
        # ask user to enter username to assign task
        assign_user = input(
            "Enter the username of who you are assigning the task to: ").strip().lower()

        # if the username does not exist the print out message and loop again
        user_exists = search_for_user(assign_user)
        if user_exists == []:
            print("\nA user with that username does not exist.\n")
        else:
            # if user exists break out of loop
            break

    # ask for a title of a task
    task_title = input("Please enter the title of the task: ").strip()

    # ask for a description of the task
    task_description = input(
        "Please enter a description of the task: ").strip()

    # today's date in the format of 10 Dec 2022
    current_date = date.today().strftime("%d %b %Y")

    # call the date_input funtion to enter  and output date in correct format
    # store date value as a sting in task_due_date
    task_due_date = date_input()

    # check that the due date is in the future, if in the past ask
    # user to re-enter date
    while compare_dates(current_date, task_due_date) is True:
        print("\nThe due date cannot be before todays date.")
        task_due_date = date_input()

    # the task is set to not complete
    task_complete = "No"

    # append new task in file tasks table

    # reformat dates to year-month-day format to be stored inthe table
    task_due_date = datetime.strptime(
        task_due_date, '%d %b %Y').strftime('%Y-%m-%d')

    current_date = datetime.strptime(
        current_date, '%d %b %Y').strftime('%Y-%m-%d')

    cursor.execute(
        '''INSERT INTO tasks (task_title, task_description, assign_date, due_date)
        VALUES(?,?,?,?)''', (task_title, task_description, current_date, task_due_date)
    )
    db.commit()

    # get the new task_id from tasks
    task_id = cursor.execute(
        '''SELECT MAX(task_id) FROM tasks '''
    ).fetchone()[0]

    # ammend the task_assign table with task_id, user_id and task_complete for the new task
    cursor.execute(
        '''INSERT INTO task_assign (task_id, user_id, task_complete)
        VALUES (?,?,?)''', (task_id, user_exists[0][0], task_complete)
    )
    db.commit()

    # return a susccess message
    return "\nThe task has been been saved succesfully."


def access_file(file_name, mode, write_string="", error_message="", encoding="utf-8"):
    '''function that checks if a file exists, if it doesn't will print an error message
        (a standard messsage + the optional error_message) and exit the program. For write
        and append modes you can enter the string to be written to file. The encoding of
        the function is set to utf-8 by default'''

    while True:
        try:
            # if read is selected, lines of file is read and retured
            if mode in ("r+", "r"):
                # check that the file exists
                if os.path.isfile("./" + file_name):
                    with open(file_name, mode, encoding=encoding) as file:
                        file.seek(0)
                        lines = file.readlines()
                        return lines
                else:
                    # if the file does not exist show error and exit program
                    print(f"{file_name} does not exist. " + error_message)
                    print("The program will now terminate")
                    sys.exit()

            # if write or appaned are selected, it will write to file
            # return None, as there is nothing to return
            if mode in ("w+", "w", "a+", "a"):
                with open(file_name, mode, encoding=encoding) as file:
                    file.write(write_string)
                    return None

        except ValueError:
            # if mode is incorredt a ValueError is rasied, print error and ask
            # user to enter correct mode
            print("Error: incorrect mode")
            mode = input("Please enter r, r+, w, w+, a or a+: ")


def generate_reports(menu_item='gr'):
    ''' function to generate reports, two text files, called
        task_overview.txt and user_overview.txt, should be generated. Both
        these text files should output data in a user-friendly, easy to read manner.'''

    # user_string to be used to write the user reports initialised befor the
    # loop.
    user_string = "Users Overview Report"

    # today's date in the format of 10 Dec 2022
    # current_date = str(date.today().strftime("%Y-%m-%d"))

    # total number of tasks
    total_tasks = cursor.execute(
        '''SELECT COUNT(*) FROM task_assign'''
    ).fetchone()[0]

    # total number of complete tasks
    complete_tasks = cursor.execute(
        '''SELECT COUNT(*) FROM task_assign
        WHERE task_complete = "Yes"'''
    ).fetchone()[0]

    # total number of incomplete tasks
    incomplete_tasks = cursor.execute(
        '''SELECT COUNT(*) FROM task_assign
        WHERE task_complete = "No"'''
    ).fetchone()[0]

    # total number of overdue tasks
    overdue_tasks = cursor.execute(
        '''SELECT COUNT(*) FROM tasks
        WHERE  date(due_date) < date('now')'''
    ).fetchone()[0]

    # all users

    users_list = cursor.execute(
        '''SELECT user_name FROM users'''
    ).fetchall()

    for user in users_list:
        user = user[0]

        user_total_tasks = cursor.execute(
            '''SELECT COUNT(task_assign.task_id) FROM task_assign
            INNER JOIN users ON task_assign.user_id = users.user_id
            WHERE users.user_name = ?
            ''', (user,)
        ).fetchone()[0]

        user_completed_tasks = cursor.execute(
            '''SELECT COUNT(task_assign.task_id) FROM task_assign
            INNER JOIN users ON task_assign.user_id = users.user_id
            WHERE task_assign.task_complete = "Yes" AND users.user_name=?
            ''', (user,)
        ).fetchone()[0]

        user_incomplete_tasks = cursor.execute(
            '''SELECT COUNT(task_assign.task_id)FROM task_assign
            INNER JOIN users ON task_assign.user_id = users.user_id
            WHERE task_assign.task_complete = "No" AND users.user_name=?
            ''', (user,)
        ).fetchone()[0]

        user_overdue_tasks = cursor.execute(
            '''SELECT COUNT(task_assign.task_id) FROM task_assign
            INNER JOIN users ON task_assign.user_id = users.user_id
            INNER JOIN tasks ON task_assign.task_id = tasks.task_id
            WHERE date(tasks.due_date) < date('now') AND users.user_name=?
            ''', (user,)
        ).fetchone()[0]

        # again accounting for divide by zero cases
        if user_total_tasks == 0:
            percentage_user_complete = 0

            percentage_user_incomplete = 0

            percentage_user_overdue = 0

            percentage_tasks_assigned = 0

        else:
            # calculating percentages
            percentage_user_complete = (
                user_completed_tasks / user_total_tasks) * 100

            percentage_tasks_assigned = (
                user_total_tasks / total_tasks) * 100

            percentage_user_incomplete = (
                user_incomplete_tasks / user_total_tasks) * 100

            percentage_user_overdue = (
                user_overdue_tasks / user_total_tasks) * 100

        # add to the user_string per user, this will be written to user_overview.txt
        user_string += f"\n_____________________________________________________________________\n\n"\
            f"{user.capitalize()}'s Overview Report\n\n"\
            f"The total number of tasks assigned:    {user_total_tasks}\n"\
            f"The percentage of tasks assigned:      {percentage_tasks_assigned :.2f}%\n"\
            f"The percentage of complete tasks:      {percentage_user_complete :.2f}%\n"\
            f"The percentage of tasks incomplete:    {percentage_user_incomplete :.2f}%\n"\
            f"The percentage of overdue tasks:       {percentage_user_overdue :.2f}%"

    # calculations for tasks statistics
    if total_tasks == 0:
        # accounting for divide by zero cases
        percentage_incomplete = 0
        percentage_overdue = 0

    else:
        percentage_incomplete = (incomplete_tasks / total_tasks) * 100

        percentage_overdue = (overdue_tasks / total_tasks) * 100

    # string to be written to task_overview.txt
    tasks_string = "Tasks Overview Report\n\n"\
        f"The total number of tasks:            {total_tasks}\n"\
        f"The number of tasks completed:        {complete_tasks}\n"\
        f"The number of incomplete tasks:       {incomplete_tasks}\n"\
        f"The number of overdue tasks:          {overdue_tasks}\n"\
        f"The percentage of tasks incomplete:   {percentage_incomplete :.2f}%\n"\
        f"The percentage of overdue tasks:      {percentage_overdue :.2f}%"\

    # ammend user_string with divider line before writing to file
    user_string += "\n_____________________________________________________________________"

    # write tasks_string to task_overview.txt
    access_file("task_overview.txt", "w", tasks_string)

    # write user_string to user_overview.txt
    access_file("user_overview.txt", "w", user_string)

    if menu_item == 'ds':
        # print on screen the statistics for tasks and users
        print("\n_____________________________________________________________________\n\n" +
              tasks_string +
              "\n\n_____________________________________________________________________\n" +
              "_____________________________________________________________________\n\n" +
              user_string + "\n")


# ======load database===========
db = load_database()

# set cursor
cursor = db.cursor()

# ====Login Section====
# Here code that will allow a user to login by calling the user_login function
# user_logged_in the user who has logged into the system

# user_logged_in[0] = user_id , user_logged_in[1] = username
user_logged_in = user_login()

# loop to be able to access the menu items until the program terminates
while True:

    # menu displyed for user input using menu_option function to generate
    # appropriate menu depending on the user
    menu = input(menu_options(user_logged_in[1]))

    if menu == 'a':
        # In this block you will put code that will allow a user to add a new
        # task to task_db

        # used the function add_task to add a task to task.txt
        print(add_task())

    elif menu == 'va':
        # In this block the function view_tasks will read the tasks from task_db
        # and print to the console all tasks

        # used the function view_tasks to generate the list of tasks
        view_tasks(menu, user_logged_in)

    elif menu == 'vm':
        # In this block the function view_tasks will read the task from task_db
        # and print to the console only the user's tasks
        view_tasks(menu, user_logged_in)

    elif menu == 'e':
        # close the database connection
        db.close()

        # an exit message for user and program terminates in this menu
        print(f"Goodbye {user_logged_in[1].capitalize()}!!!")
        exit()

    # admin only menus other users cannot enter
    elif menu == 'r' and user_logged_in[1] == "admin":
        # In this block used function reg_user to add a new user to task_db
        print(reg_user())

    elif menu == 'gr' and user_logged_in[1] == "admin":
        # When the user chooses to generate reports, two text files, called
        # task_overview.txt and user_overview.txt, should be generated by
        # generate_reports in a user-friendly easy to read manner.
        generate_reports()

    elif menu == 'ds' and user_logged_in[1] == "admin":
        # The admin user is provided with a new menu option that allows them to
        # display statistics by calling display_statistics function to read data
        # from task_db
        generate_reports('ds')

    elif menu == 'rd' and user_logged_in[1] == "admin":
        # Admin is the only user who can reset the database to the original form.
        # This is only included for the sake of this example project where it
        # may be required to reset the database to the origanal form.
        reset_database()

    else:
        # if a non menu or admin only item entered the user receives an error message
        print("\nYou have made a wrong choice, Please Try again")

'''
A program for a small business that can
help it to manage tasks assigned to each member of the team.
'''
# =====importing libraries===========
'''This is the section where you will import libraries'''

# ====Functions====




from datetime import date, datetime
import re
import os
def user_dictonary(text_file):
    '''Funtion to add the users to a dictionary from a list generated by 
    readlines froma file read'''

    # open and read user.txt file and store usernames and passwords in a dictionary users
    # since we are reading, check that it exists before proceeding
    if os.path.isfile('./'+text_file):
        with open(text_file, "r") as user_file:
            user_list = user_file.readlines()
    else:
        # if no file then print error
        print(f"{text_file} does not exist, please make sure it is in the same folder.")
        exit()

    # users stored as {username1 : password1, username2 : password2, ... } in users dictionary
    users = {k.strip().split(", ")[0]: k.strip().split(", ")[
        1] for k in user_list}

    # returns the dictionary
    return users


def view_tasks(type):
    ''' A function to view a list of the tasks stored in tasks.txt.
        If type is va - view all tasks, 
        if type is vm view tasks assigned to the user only.'''

    # check that the tasks.txt file exists. Open and read the tasks
    if os.path.exists('./tasks.txt'):
        with open("tasks.txt", "r") as task_file:
            tasks = task_file.readlines()
    else:
        # print error if no file exists and exit program
        print("tasks.txt does not exist, please make sure it is in the same folder.")
        exit()

    # the string to be printed out for each task, formatted for va or vm use.
    task_string = """
_____________________________________________________________________

Task:\t\t\t{}
Assigned to:\t\t{}
Date assigned:\t\t{}
Due date:\t\t{}
Task complete?\t\t{}
Task description:\n\t{}"""

    # empty string to take the formatted task string to be viewed by user
    my_tasks = ""

    # counter for the tasks listed, initially set to zero
    total_tasks = 0

    # useing a loop accessing each individual task
    for task in tasks:
        # strip any white spaces or escape characters and split to create list of
        # words for each line
        task = task.strip().split(', ')

        # if type is vm, we only display the tasks asigned to the user logged in
        if type == "vm":
            if task[0] == username:
                # append my_tasks string with only the tasks for user
                # 0 - username, 1 - title, 2 - description, 3 - date assigned, 4- due date, 5 - task complete
                my_tasks += task_string.format(task[1], task[0],
                                               task[3], task[4], task[5], task[2])

                # if there is a task increment the total tasks counter
                total_tasks += 1

        # otherwise, if type is va, then display all of the tasks to all users
        elif type == "va":
            my_tasks += task_string.format(task[1], task[0],
                                           task[3], task[4], task[5], task[2])

            # increment the task counter if task exists
            total_tasks += 1
        else:
            my_tasks = "Please make sure the type is either va or vm"

    # if there are no tasks listed to display, then print meesage to tell user there
    # are no tasks
    if total_tasks == 0:
        my_tasks = """_____________________________________________________________________

There are no tasks to display."""

    # add final seperator line to the last task list to look visually nicer
    my_tasks += """
_____________________________________________________________________"""

    # return the string with tasks formatted
    return my_tasks


# ====Login Section====
# use the function userDcitionary to store usernames and passwords
users = user_dictonary("user.txt")


# while loop to validate username and password
# user will repeatedly be asked to enter a valid username and password until
# they provide appropriate credentials.
while True:
    # ask user to enter their username - use strip to remove any whitespaces in the inputs
    username = input("Please enter your username: ").strip().lower()

    # if username exists as a key in users dictionary ask for password
    if username in users:
        # the user will get three tries to enter correct password
        for tries in range(3):
            # user enters password
            password = input("Please enter your password: ").strip()

            # if the password corresponds to the user key the break password loop
            if users[username] == password:
                break

            # after the third try, the program will ask for the username again
            elif tries == 2:
                print("Too many tries, start again.")
                break

            # otherwise display an error message
            else:
                print("Wrong password entered")

        # only break out of the user input loop once a correct username and
        # password has been entered to progress.
        if users[username] == password:
            break
    # if there is no username in dictionary print the error
    else:
        print("No such user name exists. Please try again.")


# display sucessful login message
print("\nCorrect login details! Loading...")


while True:
    # presenting the menu to the user and
    # making sure that the user input is coneverted to lower case.

    # the string for the menu
    menu_string = '''\nPlease select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - view my task
e - Exit\n:'''

    # if the user is admin add the statistics option to the menu
    if username == "admin":
        # replace e - Exit\n from menu string with "s - Statistics\ne - Exit\n:" using
        # regualr expressions function re.sub
        menu_string = re.sub(
            "e - Exit\n:$", "s - Statistics\ne - Exit\n:", menu_string)

    # menu displyed for user input
    menu = input(menu_string).lower()

    if menu == 'r':
        ''' code to add a new user to the user.txt file
            - Request input of a new username
            - Request input of a new password
            - Request input of password confirmation.
            - Check if the new password and confirmed password are the same.
            - If they are the same, add them to the user.txt file,
            - Otherwise you present a relevant message.'''

        # only the admin user can add new users
        if username == "admin":
            # print information
            print("\nYou will be registering a new user.\n")

            # using a while loop add the details of the new user
            while True:
                # ask to enter a new username
                new_username = input(
                    "Please enter a new username: ").strip().lower()

                # if the username already exists ask if to enter another username, otherwise go to
                # main menu by breaing out of the loop
                if new_username in users:
                    print(f"\nThe username {new_username} already exists.\n")
                    try_again = input(
                        "Would you like to try another username, y or n: ").lower()
                    if try_again == "n":
                        break
                    else:
                        continue
                else:
                    # once new username entered ask to enter new password
                    new_password = input("Please enter a password: ").strip()
                    while True:
                        # re_enter the password
                        check_password = input(
                            "Please re-enter the password: ").strip()

                        # check that the entered passwords match
                        if new_password == check_password:
                            # if passwords match append user.txt
                            with open("user.txt", "a") as user_file:
                                # write informat: username, password. it will add \n end of previous line
                                user_file.write(
                                    "\n" + new_username + ", " + new_password)

                            # update the users dictionary with new user details using user_dictonary function
                            users = user_dictonary("user.txt")

                            # print the sucessfully added message and break the loop
                            print(
                                f"\nYou have registered {new_username} successfully.")
                            break

                    # once new username and password are entered brreak out of loop to program menu
                    break
        else:
            # if the user is not admin, they will see this message
            print("\nYou are not allowed to register new users.")

    elif menu == 'a':
        ''' code that will allow a user to add a new task to task.txt file.
            - Prompt a user for the following: 
                - A username of the person whom the task is assigned to,
                - A title of a task,
                - A description of the task and 
                - the due date of the task.
            - Then get the current date.
            - Add the data to the file task.txt and
            - You must remember to include the 'No' to indicate if the task is complete.'''

        # use a loop to enter and check the username to assign task
        while True:
            # ask user to enter username to assign task
            assign_user = input(
                "Enter the username of who you are assigning the task to: ").strip().lower()

            # if the username does not exist the print out message and loop again
            if assign_user not in users:
                print("\nA user with that username does not exist.\n")
            else:
                # if user exists break out of loop
                break

        # ask for a title of a task
        task_title = input("Please enter the title of the task: ").strip()

        # ask for a description of the task
        task_description = input(
            "Please enter a description of the task: ").strip()

        # ask for the due date of the task whilst checking that the ofrmat is correct
        while True:
            # ask user to enter the date in the dd mm yyyy format
            print("\nThe due date should be entered in the format dd mm yyyy",
                  "\n\nFor example 2nd October 2022 should be written as 02 10 2022\n")

            task_due = input(
                "Please enter the due date as dd mm yyyy: ").strip()

            # check that it is the correct format, if not ask to input again otherwise break loop
            if not re.match(r'[0-3][0-9] [0-1][0-9] [0-9]{4}$', task_due):
                print("\n -> Wrong date format. Please enter it correctly.")

            else:
                try:
                    # format the entered date to correct format, eg 10 Dec 2023
                    task_due_date = datetime.strptime(
                        task_due, '%d %m %Y').strftime('%d %b %Y')

                    # leave loop now that correct date format entered
                    break

                except ValueError:
                    # if the format is not correct,eg if they enetered 35 15 2000, then print error
                    print("\nWrong date format. Please enter it correctly.")

        # today's date in the format of 10 Dec 2022
        current_date = date.today().strftime("%d %b %Y")

        # the task is set to not complete
        task_complete = "No"

        # the string in the correct format to be written in tasks.txt
        string_task = f"{assign_user}, {task_title}, {task_description}, {current_date}, {task_due_date}, {task_complete}"

        # append new task in file tasks.txt on a new line
        with open("tasks.txt", "a") as task_file:
            task_file.write("\n" + string_task)

        # print out a susccess message
        print("\nThe task has been been saved succesfully.")

    elif menu == 'va':
        ''' code that the program will read the task from task.txt file and
        print to the console in the format of Output 2 in the task PDF(i.e. include spacing and labelling)
            - Read a line from the file.
            - Split that line where there is comma and space.
            - Then print the results in the format shown in the Output 2 
            - It is much easier to read a file using a for loop.'''

        # used the function view_tasks to generate the list of tasks
        print(view_tasks(menu))

    elif menu == 'vm':
        ''' code that will read the task from task.txt file and
         print to the console in the format of Output 2 in the task PDF(i.e. include spacing and labelling)
            - Read a line from the file
            - Split the line where there is comma and space.
            - Check if the username of the person logged in is the same as the username you have
            read from the file.
            - If they are the same print it in the format of Output 2 in the task PDF'''

        # used the function view_tasks to generate the list of tasks
        print(view_tasks(menu))

    elif menu == 's':
        '''The admin user is provided with a new menu option that allows them to display statistics. 
        When this menu option is selected, the total number of tasks and the total number of users should 
        be displayed in a user-friendly manner.'''

        # setting the contion that this will only work if the user logged in is admin
        if username == "admin":

            # total number of tasks
            if os.path.isfile('./tasks.txt'):
                with open('./tasks.txt', "r") as user_file:
                    task_list = user_file.readlines()
            else:
                print(
                    "tasks.txt does not exist, please make sure it is in the same folder.")
                exit()

            # and the total number of users
            if os.path.isfile('./user.txt'):
                with open('./user.txt', "r") as user_file:
                    user_list = user_file.readlines()
            else:
                print(
                    "user.txt does not exist, please make sure it is in the same folder.")
                exit()

            # print out the statistics of total number of tasks and users
            # Using the len function to determine the total numbers in each list
            print(f"""
_____________________________________________________________________

\033[1m{"Statistics" : ^15} \033[0m

    The total number of tasks:\t{len(task_list)}
    Total number of users:\t{len(user_list)}

_____________________________________________________________________
            """)

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")

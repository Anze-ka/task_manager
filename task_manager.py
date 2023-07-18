# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password


#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    # To ensure the task will not carry any unnecessary characters.
    task_data = [t for t in task_data if t != ""] 


task_list = [] # the list that stores the tasks(dict items).

for t_str in task_data: 
    curr_t = {}  # the dict for the current/original task in the file.

    # Split strings by semicolon and manually add each component as key: value pair into a curr_t dict.
    task_components = t_str.split(";")  
    curr_t['username'] = task_components[0]  
    curr_t['title'] = task_components[1]
    curr_t['due_date'] = task_components[2]
    curr_t['assigned_date'] = task_components[3]
    curr_t['description'] = task_components[4]
    curr_t['completed'] = task_components[5]
    # Add current task into the task_list.
    task_list.append(curr_t)   


#====Login Section================
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''

# Read in user_data.
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary.
username_password = {}
for user in user_data:
    username, password = user.split(';') # Split 'admin' and 'password'
    username_password[username] = password  # Add admin: password as key:value pair in a dict

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    # If the input username not in the keys of dict - username_password = {}.
    if curr_user not in username_password.keys(): 
        print("User does not exist")
        continue
    # If the input passrowd doesn't match the value for the input username in username_password = {}. 
    elif username_password[curr_user] != curr_pass: 
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


#====Functions Section==========


def reg_user():
    # - Request input of a new username
    new_username = input("New Username: ")

    if new_username not in username_password.keys(): # If the input username not in the username_password dict keys.
        # - Request input of a new password
        new_password = input("New Password: ")
        # - Request input of password confirmation.
        confirm_password = input("Confirm Password: ")

        # - Check if the new password and confirmed password are the same.
        if new_password == confirm_password:
            # - If passwords match, add a new key: value pair into the username_password dict.
            print("New user added")
            username_password[new_username] = new_password

            # - Add new username and password to the user.txt file.        
            with open("user.txt", "w") as out_file:
                user_data = []
                for k in username_password:     # For every key in the dict username_password.
                    user_data.append(f"{k};{username_password[k]}") # Add username; passowrd from the dict into user_data list.
                out_file.write("\n".join(user_data)) # Join method concatenates the list and forms a string which is added into the user.txt file.
        else: 
            print("Passwords do no match")     

    # - Otherwise presenting a relevant message.
    else:
        print("This username already exists in the database.")

 
def add_task():
    # - Request an input of a username of the person whom the task is assigned to.
    task_username = input("Name of person assigned to task: ")

    # - Check if a username exists in the list of users
    if task_username in username_password.keys():
         
    
        # - Request an input of a title of the task.
        task_title = input("Title of Task: ") 
            
        while True:
            try:
                # - Request an input of a task due date.
                task_due_date = input("Due date of task (YYYY-MM-DD): ")  
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)  # convert the date into a string
                break
            # If the format of the input of the due date isn't correct, exception is raised.
            except ValueError:  
                print("Invalid datetime format. Please use the format specified")
                
        # - Get the current date.
        curr_date = date.today()
        # - Request an input of a task description.
        task_description = input("Description of Task: ")
        # - Create a dictionary for a new task.
        new_task = {
                "username": task_username,
                "title": task_title,
                "due_date": due_date_time.strftime(DATETIME_STRING_FORMAT), # converted to a string object
                "assigned_date": curr_date.strftime(DATETIME_STRING_FORMAT), # today's date converted to a string object
                "description": task_description,
                "completed": "No" 
            }
        # - Add the new task into the list of tasks - task_list.
        task_list.append(new_task)  

        # - Write the task into the file.
        with open("tasks.txt", "a") as task_file:  
            task_list_to_write = []   
            for t in task_list:  
                # - Define attributes for a task.
                str_attrs = [
                        t['username'],
                        t['title'],
                        t['due_date'],
                        t['assigned_date'],
                        t['description'],
                        t['completed']
                    ]
                task_list_to_write.append(";".join(str_attrs)) 
            # - Write in the tasks file.
            task_file.write("\n".join(task_list_to_write))
            
        print("Task successfully added.")
    elif task_username not in username_password.values():
        print("\nSorry. The user does not exist. Please register a new user first.")

        while True:
            reg = input("\nWould you like to register a new user? Yes/No").capitalize()
            if reg == "Yes":
                reg_user()
                break
            elif reg == "No":
                add_task()
                break
            else:
                print("\nInvalid input. PLease try again.")


# Function displays all tasks.
def view_all():
    for i, t in enumerate(task_list,1):
        disp_str = f"Task {i}: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t\t {t['username']}\n"
        disp_str += f"Due Date: \t\t {t['due_date']}\n"
        disp_str += f"Date Assigned: \t\t {t['assigned_date']}\n" 
        disp_str += f"Task Description: \t {t['description']}\n"
        disp_str += f"Completed: \t\t {t['completed']}\n"
        
        print(disp_str) # display details for all tasks

# Function allows to display the tasks for the current user and mark as complete or edit username and/or due date.
def view_mine(curr_user,task_list):
    curr_user_t_list = []
    curr_t_index = 0

    for t in task_list: 
        # - If the task username is the current user or the person logged in.
        if t['username'] == curr_user: 
            # - Append all current user tasks into a separate list.          
            curr_user_t_list.append(t)
            curr_t_index += 1
            # Iterate through the list of current user tasks. 
            #for index,t in enumerate(curr_user_t_list,1):

            disp_str = f"\nTask {curr_t_index}: \t\t {t['title']} \n"               
            disp_str += f"Assigned to: \t\t {t['username']}\n"
            disp_str += f"Due Date: \t\t {t['due_date']}\n"
            disp_str += f"Date Assigned: \t\t {t['assigned_date']}\n"
            disp_str += f"Task Description: \t {t['description']}\n"
            disp_str += f"Completed: \t\t {t['completed']}\n"
            print(disp_str) # display the details for each task for the current user

    while True:
        # - Request an input of a task number or -1.
        user_index = int(input("Please enter a task number to edit or -1 to return to the main menu: ")) -1

        # - If the input is not '-1' and in the range of the length of the current user task list .
        if user_index <= len(curr_user_t_list) and user_index >= 0:
            # - Select a task to edit from the curr_user_t_list.
            task_to_edit = curr_user_t_list[user_index] 

            # - Request an input of 1 or 2.
            option_choice = int(input('''
Enter:
1 - to mark as complete or
2 - to edit the task
: '''))
            
            while True:
                # - If the user input is 1 - request to mark the task as complete.
                if option_choice == 1:
                    # - If the task is incomplete. 
                    if task_to_edit['completed'] == "No":
                        # - Mark the task as complete.  
                        task_to_edit['completed'] = "Yes"
                        print("Success! Marked as complete.")
                        break
                    # - Else display a message that the task is already complete.
                    else:
                        print("The task is already complete!")
                        break
                        

                # - If the user input is 2 - request to edit the task.
                elif option_choice == 2:
                    # - If the task is incomplete.
                    if task_to_edit['completed'] == "No":
                        # - Request an input of Yes/No to to edit the username.
                        edit_username = input("Would you like to edit username?(Yes/No)\t").capitalize() 
                        if edit_username == "Yes":
                            # - Request an input of a new username.
                            update_username = input("Please add a new username: ")  
                            # - Update the username value.             
                            task_to_edit['username'] = update_username   
                            print("Success! Username updated.")
                        # - If the input is No, then pass.
                        else:
                            pass
                        # - Request an input of Yes/No to edit the due date.
                        edit_due_date = input("Would you like to edit due date?(Yes/No)\t").capitalize() 
                        if edit_due_date == "Yes":
                            # - Request an input of YYYY-MM-DD.
                            update_due_date = input("Please add a due date (YYYY-MM-DD): ") 
                            # - Update the due_date value.
                            task_to_edit['due_date'] = update_due_date  
                            print("Success! Due date is updated.")
                            break
                        # - If the input is No, then pass.
                        else:
                            break
                    # - If the input is 2, but the task is complete.
                    else:
                        # - Dislay a message that changes are not permitted.
                        print("\nChanges are not allowed. The task has already been completed.")
                        break

                # - If user input is out of range, neither 1 nor 2.
                else:
                    print("\nInvalid option. Enter '1' to mark as complete or '2' to edit.") 
                
        # - If the input is '-1' - request to return to the main menu, then pass.         
        elif user_index == -2:
            break
        # - If user input number is out of range or invalid data type.
        else:
            print("\nOops. Invalid entry.")
        
            # - If the user input was a task number to edit. 
            if user_index <= len(curr_user_t_list) and user_index >= 0:
                # - Update the task in the task list.
                for i in task_list[user_index]:
                    task_list[user_index][i] = task_to_edit[i]
                    break

        # - Write the tasks into the tasks file.
    with open("tasks.txt", "w") as task_file:
                
        for t in task_list:
            task_file.write(f"{t['username']};{t['title']};{t['due_date']};{t['assigned_date']};{t['description']};{t['completed']}\n")


def task_overview():
    
    total_tasks = len(task_list) # the total number of tasks that have been generated and tracked
    completed_tasks = 0
    uncompleted_tasks = 0
    uncompleted_overdue_tasks = 0
    overdue_tasks = 0
    curr_date = datetime.today() # to get today's date
    
    for t in task_list:

        # - Calculate the total number of completed tasks.
        if t['completed'] == "Yes":
            completed_tasks += 1    
        # - Calculate the total number of uncompleted tasks.
        if t['completed'] == "No":
            uncompleted_tasks += 1      

        deadline = datetime.strptime(t['due_date'],'%Y-%m-%d') # to convert due date to a datetime object
        # - Calculate the total number of uncompleted and overdue tasks.
        if t['completed'] == "No" and deadline < curr_date:
            uncompleted_overdue_tasks += 1

        # - Calculate the total number of overdue tasks.
        if deadline < curr_date:
            # - Add the task to the overdue_tasks list.
            overdue_tasks += 1  

    # - Calculate the percentage of the uncompleted tasks.            
    percent_uncompleted = (uncompleted_tasks * 100) / total_tasks 
    # - Calculate the percentage of tasks that are overdue.
    percent_overdue = (overdue_tasks * 100) / total_tasks

    # - Write the results into the task_overview file.    
    with open("task_overview.txt", 'w') as tasks_report:
          tasks_report.write(f'''Tasks Overview:\n
The total number of tasks:\t{total_tasks}\n
The total number of completed tasks:\t{completed_tasks}\n
The total number of incomplete tasks:\t{uncompleted_tasks}\n
The total number of incomplete and overdue tasks:\t{uncompleted_overdue_tasks}\n
The percentage of tasks that are incomplete:\t{round(percent_uncompleted,1)}%\n
The percentage of tasks that are overdue:\t{round(percent_overdue,1)}%\n       
''')

        
def user_overview():    

    user_count = len(username_password) # the total number of users registered, length of username_password dict
    total_tasks = len(task_list) # the total number of tasks that have been generated

    curr_date = datetime.today() # to get today's date
    
    user_completed = {}
    user_incomplete = {}
    user_incompl_overdue = {}
    count_per_user = {}
    counter = 0

    # - Loop through all usernames.
    for user in username_password.keys():
        # Initiliase dictionaries with an initial count of tasks per user as zero in each dict.
        count_per_user[user] = counter
        user_completed[user] = counter
        user_incomplete[user] = counter
        user_incompl_overdue[user] = counter
        # - Loop through a list of all tasks.
        for t in task_list:
            if user == t['username']:
                # - Count a number of tasks assigned to the specific user
                count_per_user[user] = counter + 1

            # - Calculate a number of completed tasks for each user.
            if user == t['username'] and t['completed'] == "Yes":
                user_completed[user] = counter + 1
    
            # - Calculate a number of in complete tasks for each user.
            if user == t['username'] and t['completed'] == "No":
                user_incomplete[user] = counter + 1
    
            deadline = datetime.strptime(t['due_date'],'%Y-%m-%d') # convert due date to datetime object
            # - Calculate a number of incomplete and overdue tasks for each user.
            if user == t['username'] and t['completed'] == "No" and deadline < curr_date:
                user_incompl_overdue[user] = counter + 1
    # - Open the user_overview file.
    with open("user_overview.txt", 'w') as user_report:
    
        for user in username_password.keys():
            
            # - The percentage of the total number of tasks that have been assigned for the user.
            task_count_percent = (count_per_user[user] / total_tasks) * 100
        
            # - The percentage of the tasks assigned to that user that have been completed.
            completed_percent = (user_completed[user] / count_per_user[user]) * 100
    
            # - The percentage of the tasks assigned to that user that must still be completed.
            incomplete_percent = (user_incomplete[user] / count_per_user[user]) * 100

            # - The percentage of the tasks assigned to that user that have not yet been completed and are overdue.
            incompl_overdue_percent = (user_incompl_overdue[user] / count_per_user[user]) * 100
    
            # - Write the above results for each user in the user_overview file.
            user_report.write(f'''User Overview: {user}\n
The total number of users:\t{user_count}\n
The total number of tasks assigned to the user:\t{count_per_user[user]}\n
The percentage of tasks assigned to the user:\t{round(task_count_percent,1)}%\n
The percentage of the completed tasks:\t{round(completed_percent,1)}%\n
The percentage of the incomplete tasks:\t{round(incomplete_percent,1)}%\n
The percentage of tasks that are incomplete and overdue:\t{round(incompl_overdue_percent,1)}%\n\n       
''')
        
#############################################################################
while logged_in:
     
    # - Display the menu for the admin user only.
    if curr_user == "admin":

        print()
        menu = input('''Select one of the following Options below:
r  - Register a user
a  - Add a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e -  Exit
: ''').lower()
    else:
        # - Display the menu for other users.
        print()
        menu = input('''Select one of the following Options below:
r  - Register a user
a  - Add a task
va - View all tasks
vm - View my task
e  - Exit
: ''').lower()


    if menu == 'r':
        reg_user()
    elif menu == 'a':
        add_task()
    elif menu == 'va': 
        view_all()      
    elif menu == 'vm':
        view_mine(curr_user, task_list)
    elif menu == 'gr':  
        task_overview()
        user_overview()
    elif menu == 'ds':
        print("\nStatistics\n")
        print("-"*65) # to print the dashed line
        while True:
            try:       
                # - Read in and display the task_overview file.
                with open("task_overview.txt", 'r') as task_report:
                    t_overview = task_report.read()
                    print(t_overview)
                    break
            # - If task_overview does not exist, call the function to generate it.
            except FileNotFoundError:   
                task_overview()
        print("-"*65) # to print the dashed line
        while True:      
            try:
                # - Read in and display the user_overview file.
                with open("user_overview.txt", 'r') as u_report:
                    u_overview = u_report.read()
                    print(u_overview)
                    break
            # - If user_overview does not exist, call the function to generate it.
            except FileNotFoundError:   
                user_overview()
    elif menu == 'e':
        print("Goodbye!")
        break   



 


        
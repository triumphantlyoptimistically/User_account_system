import os


def Print_Header(title):
    print("\n" + "=" * 30)
    print(title)
    print("=" * 30)


def Print_Separator():
    print("-" * 30)


def Print_Error(message):
    print(f"\nERROR: {message}\n")


def Display_Menu():
    Print_Header("User Account System")
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    Print_Separator()


def Display_Task_Menu(current_user):
    Print_Header(f"Task Manager ({current_user})")
    print("1. Add task")
    print("2. View my tasks")
    print("3. Mark task as complete")
    print("4. Logout")
    Print_Separator()


def Get_Option(min_option, max_option):
    while True:
        choice = input(f"Enter an option ({min_option}-{max_option}): ").strip()
        if not choice:
            Print_Error(f"Please enter a number between {min_option} and {max_option}.")
            continue

        try:
            option = int(choice)
        except ValueError:
            Print_Error(f"Invalid input. Enter a number between {min_option} and {max_option}.")
            continue

        if option < min_option or option > max_option:
            Print_Error(f"Invalid option. Choose a number between {min_option} and {max_option}.")
            continue

        return option


def Get_Username():
    while True:
        username = input("Enter username: ").strip()
        if not username:
            Print_Error("Username cannot be empty.")
            continue
        return username


def Get_Password():
    while True:
        password = input("Enter password: ").strip()
        if not password:
            Print_Error("Password cannot be empty.")
            continue
        return password


def Ensure_File_Exists(filename):
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8"):
            pass


def Space_To_Underscore(value):
    return value.strip().replace(" ", "_")


def Underscore_To_Space(value):
    return value.replace("_", " ")


def Load_Tasks():
    Ensure_File_Exists("Tasks.txt")

    tasks = []
    with open("Tasks.txt", "r", encoding="utf-8") as text_file:
        for line in text_file:
            line = line.strip()
            if not line:
                continue

            parts = line.split(" ")
            if len(parts) != 3:
                continue

            owner = parts[0]
            title = Underscore_To_Space(parts[1])
            completed = parts[2] == "1"

            tasks.append(
                {
                    "title": title,
                    "completed": completed,
                    "owner": owner,
                }
            )

    return tasks


def Save_Tasks(tasks):
    with open("Tasks.txt", "w", encoding="utf-8") as text_file:
        for task in tasks:
            owner = task["owner"]
            title = Space_To_Underscore(task["title"])
            completed = "1" if task["completed"] else "0"
            text_file.write(f"{owner} {title} {completed}\n")


def Get_User_Tasks(tasks, current_user):
    return [t for t in tasks if t["owner"] == current_user]


def Print_User_Tasks(user_tasks):
    if len(user_tasks) == 0:
        Print_Error("No tasks found.")
        return

    print("")
    for i in range(0, len(user_tasks), 1):
        check_box = "[✔]" if user_tasks[i]["completed"] else "[ ]"
        print(f"{i + 1}. {check_box} {user_tasks[i]['title']}")
    print("")


def Add_Task(current_user):
    Print_Header("Add Task")
    title = input("Enter title: ").strip()

    if not title:
        Print_Error("Title cannot be empty.")
        return

    tasks = Load_Tasks()
    tasks.append(
        {
            "title": title,
            "completed": False,
            "owner": current_user,
        }
    )
    Save_Tasks(tasks)

    print("Task added successfully.")


def View_My_Tasks(current_user):
    tasks = Load_Tasks()
    user_tasks = Get_User_Tasks(tasks, current_user)

    Print_Header("My Tasks")
    Print_User_Tasks(user_tasks)


def Mark_Task_Complete(current_user):
    tasks = Load_Tasks()
    user_tasks = Get_User_Tasks(tasks, current_user)

    Print_Header("Mark Task as Complete")
    Print_User_Tasks(user_tasks)

    if len(user_tasks) == 0:
        return

    task_choice = Get_Option(1, len(user_tasks))
    selected_task = user_tasks[task_choice - 1]

    if selected_task["completed"]:
        Print_Error("That task is already marked as complete.")
        return

    selected_task["completed"] = True
    Save_Tasks(tasks)

    print("Task marked as complete.")


def Run_Task_Menu(current_user):
    while True:
        Display_Task_Menu(current_user)
        option = Get_Option(1, 4)

        if option == 1:
            Add_Task(current_user)
        elif option == 2:
            View_My_Tasks(current_user)
        elif option == 3:
            Mark_Task_Complete(current_user)
        else:
            print("Logged out.")
            return


def Register_User():
    Print_Header("Register")
    username = Get_Username()
    password = Get_Password()

    Ensure_File_Exists("Users.txt")

    with open("Users.txt", "a+", encoding="utf-8") as text_file:
        text_file.seek(0)
        for line in text_file:
            line = line.strip()
            if not line:
                continue
            existing_username = line.split(" ", 1)[0]
            if existing_username == username:
                Print_Error("That username already exists. Choose another.")
                return

        text_file.write(f"{username} {password}\n")

    print("User registered successfully.")


def Login_User():
    Print_Header("Login")
    username = Get_Username()
    password = Get_Password()

    Ensure_File_Exists("Users.txt")

    with open("Users.txt", "r", encoding="utf-8") as text_file:
        for line in text_file:
            line = line.strip()
            if not line:
                continue

            parts = line.split(" ", 1)
            if len(parts) != 2:
                continue

            line_username = parts[0]
            line_password = parts[1]

            if line_username == username:
                if line_password != password:
                    Print_Error("Wrong password.")
                    return None

                print(f"Logged in as {username}.")
                return username

    Print_Error("User not found.")
    return None


running = True
while running:
    Display_Menu()
    option = Get_Option(1, 3)

    if option == 1:
        Register_User()
    elif option == 2:
        current_user = Login_User()
        if current_user is not None:
            Run_Task_Menu(current_user)
    else:
        print("Goodbye.")
        running = False

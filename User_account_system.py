import os


def Display_Menu():
    print("\n" + "=" * 24)
    print("User Account System")
    print("=" * 24)
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    print("-" * 24)


def Display_Task_Menu(current_user):
    print("\n" + "=" * 24)
    print(f"Task Manager ({current_user})")
    print("=" * 24)
    print("1. Add task")
    print("2. View my tasks")
    print("3. Mark task as complete")
    print("4. Logout")
    print("-" * 24)


def Get_Option(min_option, max_option):
    while True:
        try:
            option = int(input(f"Enter an option ({min_option}-{max_option}): "))
        except ValueError:
            print(f"Enter an option between {min_option} and {max_option}\n")
            continue

        if option < min_option or option > max_option:
            print(f"Enter an option between {min_option} and {max_option}\n")
            continue

        return option


def Get_Username():
    empty = True
    while empty:
        username = input("Enter username: ")
        if not username:
            print("Please enter a valid username\n")
        else:
            empty = False
            return username


def Get_Password():
    empty = True
    while empty:
        password = input("Enter password: ")
        if not password:
            print("Please enter a valid password\n")
        else:
            empty = False
            return password


def Ensure_File_Exists(filename):
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8"):
            pass


def Encode_Field(value):
    return value.strip().replace(" ", "_")


def Decode_Field(value):
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
            if len(parts) != 4:
                continue

            owner = parts[0]
            title = Decode_Field(parts[1])
            description = Decode_Field(parts[2])
            completed = parts[3] == "1"

            tasks.append(
                {
                    "title": title,
                    "description": description,
                    "completed": completed,
                    "owner": owner,
                }
            )

    return tasks


def Save_Tasks(tasks):
    with open("Tasks.txt", "w", encoding="utf-8") as text_file:
        for task in tasks:
            owner = task["owner"]
            title = Encode_Field(task["title"])
            description = Encode_Field(task["description"])
            completed = "1" if task["completed"] else "0"
            text_file.write(f"{owner} {title} {description} {completed}\n")


def Get_User_Tasks(tasks, current_user):
    return [t for t in tasks if t["owner"] == current_user]


def Print_User_Tasks(user_tasks):
    if len(user_tasks) == 0:
        print("\nNo tasks\n")
        return

    print("")
    for i in range(0, len(user_tasks), 1):
        checkBox = "[✔ ]" if user_tasks[i]["completed"] else "[ ]"
        print(f"{i + 1}. {checkBox} {user_tasks[i]['title']}")
    print("")


def Add_Task(current_user):
    print("\n--- Add task ---")
    title = input("Enter title: ").strip()
    description = input("Enter description: ").strip()

    if not title:
        print("\nTitle cannot be empty\n")
        return

    tasks = Load_Tasks()
    tasks.append(
        {
            "title": title,
            "description": description,
            "completed": False,
            "owner": current_user,
        }
    )
    Save_Tasks(tasks)

    print("\nTask added\n")


def View_My_Tasks(current_user):
    tasks = Load_Tasks()
    user_tasks = Get_User_Tasks(tasks, current_user)

    print("\n--- My tasks ---")
    Print_User_Tasks(user_tasks)


def Mark_Task_Complete(current_user):
    tasks = Load_Tasks()
    user_tasks = Get_User_Tasks(tasks, current_user)

    print("\n--- Mark task as complete ---")
    Print_User_Tasks(user_tasks)

    if len(user_tasks) == 0:
        return

    task_choice = Get_Option(1, len(user_tasks))
    selected_task = user_tasks[task_choice - 1]

    selected_task["completed"] = True
    Save_Tasks(tasks)

    print("\nTask marked as complete\n")


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
            print("\nLogged out.\n")
            return


def Register_User():
    print("\n--- Register ---")
    username = Get_Username()
    password = Get_Password()

    Ensure_File_Exists("Users.txt")

    with open("Users.txt", "a+", encoding="utf-8") as text_file:
        text_file.seek(0)
        for line in text_file:
            line = line.strip()
            if not line:
                continue
            existingUsername = line.split(" ", 1)[0]
            if existingUsername == username:
                print("\nThat username already exists. Choose another.\n")
                return
        text_file.write(f"{username} {password}\n")

    print("\nUser registered\n")


def Login_User():
    print("\n--- Login ---")
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

            lineUsername = parts[0]
            linePassword = parts[1]

            if lineUsername == username:
                if linePassword != password:
                    print("\nWrong password\n")
                    return None
                else:
                    print(f"\nLogged in as {username}\n")
                    return username

    print("\nUser not found\n")
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
        print("\nGoodbye.\n")
        running = False
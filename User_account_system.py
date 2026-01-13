def Display_Menu():
    print("\n" + "=" * 24)
    print("User Account System")
    print("=" * 24)
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    print("-" * 24)


def Get_Option():
    valid = False
    while valid == False:
        option = int(input("Enter an option (1-3): "))
        if option < 1 or option > 3:
            print("Enter an option between 1 and 3\n")
        else:
            valid = True
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


def Register_User():
    print("\n--- Register ---")
    username = Get_Username()
    password = Get_Password()
    with open("Users.txt", "a+") as text_file:
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
    text_file.close()


def Login_User():
    print("\n--- Login ---")
    username = Get_Username()
    password = Get_Password()
    with open("Users.txt", "r") as text_file:
        text_file.seek(0)
        for line in text_file:
            line = line.strip()
            if not line:
                continue
            lineUsername = line.split(" ", 1)[0]
            linePassword = line.split(" ", 1)[1]
            if lineUsername == username:
                if linePassword != password:
                    print("\nWrong password\n")
                    return False
                else:
                    print(f"\nLogged in as {username}\n")
                    return True
        print("\nUser not found\n")
        return False


running = True
while running:
    Display_Menu()
    option = Get_Option()
    if option == 1:
        Register_User()
    elif option == 2:
        Login_User()
    else:
        print("\nGoodbye.\n")
        running = False

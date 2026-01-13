def Display_Menu():
    print("User account System\n\n1. Register\n2. Login\n3. Exit\n\n")

def Get_Option():
    valid = False
    while valid == False:
        option = int(input("Enter an option: "))
        if option < 1 or option > 3:
            print ("Enter an option between 1 and 3\n")
        else:
            valid = True
            return option

def Register_User():
    empty = True
    while empty:
        username = input("\nEnter username: ")
        password = input("Enter password: ")
        if not username and not password:
            print("\nPlease enter a valid username and passsword")
        elif not password:
            print("\nPlease enter a valid password")
        elif not username:
            print("\nPlease enter a valid username")
        else:
            empty = False
    with open("Users.txt", "a+") as text_file:
        text_file.seek(0)
        for line in text_file:
            line = line.strip()
            if not line:
                continue
            existingUsername = line.Split(" ", 1)[0]
            if existingUsername == username:
                print("\nThat username already exists. Choose another.\n")
                return 
        text_file.write(f"{username} {password}\n")
    print("User registered")

running = True
while running:
    Display_Menu()
    option = Get_Option()
    if option == 1:
        Register_User()
    elif option == 2:
        print("Login selected\n\n")
    else:
        running = False

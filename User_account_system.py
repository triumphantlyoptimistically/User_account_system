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





running = True
while running:
    Display_Menu()
    option = Get_Option()
    if option == 1:
        print("Register selected\n\n")
    elif option == 2:
        print("Login selected\n\n")
    else:
        running = False

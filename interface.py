import mini_project_1_291 as backend
import os
from getpass import getpass
from time import sleep

def showFive(fullList):
    start = 0
    end = min(4, len(fullList)-1)
    
    while True:
        os.system('clear')
        for i, option in enumerate(fullList[start:end+1]):
            print(start+i+1, ": ", option, sep="")

        print()
        if start > 0:
            print("-1: prev")
        if end != len(fullList)-1:
            print("0: next")

        print()
        choice = int(input("Make a choice by entering a number: "))

        if choice == -1 and start > 0:
            start -= 5
            end = min(start+4, len(fullList)-1)
        elif choice == 0 and end != len(fullList)-1:
            start += 5
            end = min(start+4, len(fullList)-1)
        elif choice >= start+1 and choice <= end+1:
            print(fullList[choice-1])
            return(fullList[choice-1])
        

def offerRide():
    return
    #print()
    #date = input("Enter date (YYYY-MM-DD): ")
    #seats = int(input("Enter the number of seats: "))
    #price = int(input("Enter the price per seat: "))
    #lugg = input("Enter the luggage description: ")
    #source = input("Enter source location: ")
    #matches = backend.findLoc(source)   


def searchRide():
    return


def bookings():
    return


def postRequest():
    return


def manageRequests():
    return


def menu(email):
    os.system('clear')

    messages = backend.getUnreadMessages(email)

    if len(messages) > 0:
        print("--------------------")
        print("Unseen Messages:\n")

        for message in messages:
            print(message[0])
        print("--------------------")
        print("\n")

    print("1: Offer a ride")
    print("2: Search for rides")
    print("3: Book members or cancel bookings")
    print("4: Post a ride request")
    print("5: Manage ride requests")
    print("6: Logout")
    print()
    
    choice = input("Pick an option by entering a number: ")
    
    if choice == "1":
        offerRide()
    elif choice == "2":
        searchRide()
    elif choice == "3":
        bookings()
    elif choice == "4":
        postRequest()
    elif choice == "5":
        manageRequests()
    elif choice == "6":
        loginScreen()
    else:
        print("\n Incorrect choice, try again")
        menu(email)


def loginScreen():
    os.system('clear')
    while True:
        choice = input("Enter 'e' for existing user or 'n' for new user: ")
        
        if choice == 'n':
            # new member
            os.system('clear')
            email = input("Enter your email: ")
            name = input("Enter your name: ")
            phone = input("Enter your phone number (xxx-xxx-xxxx): ")
            password = getpass(prompt="Enter a password: ")
            unique = backend.addMember(email, name, phone, password)

            if unique:
                print("Account creation successful")
                sleep(2) # give time for message to show before clearing screen and showing menu  
                menu(email)
            else:
                print("Account creation failed, email not unique")            

        elif choice == 'e':
            # existing member
            os.system('clear')
            email = input("Enter your email: ")
            password = getpass(prompt="Enter your password: ")

            valid = backend.checkLogin(email, password)

            if valid:
                menu(email)
            else:
                os.system('clear')
                print("Incorrect email/password")


backend.main() # initialize cursor and connection

#showFive([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]) # for testing
#print(backend.checkLogin("bob@123.ca", "bpass"))
#print(backend.getUnreadMessages("don@mayor.yeg")) # should print both messages
#print(backend.getUnreadMessages("don@mayor.yeg")) # should print no messages (they have been read)

# should be True, False, False
#print(backend.addMember("foo@bar.baz", "foobar", "123-456-7890", "foopass"))
#print(backend.addMember("foo@bar.baz", "foobar", "123-456-7890", "foopass"))
#print(backend.addMember('don@mayor.yeg', 'Don Iveson', '780-382-8239', 'dpass'))

loginScreen()
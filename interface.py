import mini_project_1_291 as backend
import os
from getpass import getpass
from time import sleep

# Written by Noah

def showFive(fullList, label):
    start = 0
    end = min(4, len(fullList)-1)
    
    while True:
        os.system('clear')
        print(label)
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
    # Menu for offering a ride, feature 1 in spec

    os.system('clear')
    # date = input("Enter date (YYYY-MM-DD): ")
    # seats = int(input("Enter the number of seats: "))
    # price = int(input("Enter the price per seat: "))
    # lugg = input("Enter the luggage description: ")
    source = input("Enter source location: ")
    matches = backend.findLoc(source)


    if len(matches) == 1:
        lcode = matches[0]
    else:
        lcode = showFive(matches, "")



def searchRide(email):
    # Menu for searching for a ride and messaging the driver, feature 2 in spec

    os.system('clear')

    keywords = input("Enter 1-3 keywords separated by commas: ").split(",")

    matches = backend.rideSearchFromKeyword(tuple(keywords))

    ride = showFive(matches, "cno, make, model, year, car seats, owner, rno, price, date, offered seats, luggage, src, dst, driver, cno, lcode")

    message = input("Enter message content: ")
    backend.sendMessage(ride[5], email, message, ride[6])

    input("Message sent, press enter to continue: ")
    menu(email)


def bookings(email):
    # Booking management menu, feature 3 in spec

    os.system('clear')
    print("1: List or cancel bookings")
    print("2: Book a member")
    choice = input("Make a selection by entering a number: ")

    if choice == "1":
        os.system('clear')
        matches = backend.findMatchingBookings(email)
        for match in matches:
            print(match)
    elif choice == "2":
        os.system('clear')
        


def postRequest(email):
    # Menu for posting a request, feature 4 in spec

    os.system('clear')

    date = input("Enter date (YYYY-MM-DD): ")
    src = input("Enter pickup location code: ")
    dst = input("Enter destination location code: ")
    amount = int(input("Enter amount willing to pay per seat: "))

    backend.postRideRequest(date, email, src, dst, amount)
    menu(email)


def manageRequests(email):
    # Viewing and deleting ride requests, feature 5 in spec

    os.system('clear')
    print("1: List all your ride requests")
    print("2: Delete ride request")
    print("3: Search for ride requests")
    choice = input("Make a selection by entering a number: ")

    if choice == "1":
        rides = backend.retRequest(email)
        showFive(rides, "")
    elif choice == "2":
        rides = backend.retRequest(email)
        ride = showFive(rides, "")
        backend.deleteRequest(ride)       
                


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
        searchRide(email)
    elif choice == "3":
        bookings(email)
    elif choice == "4":
        postRequest(email)
    elif choice == "5":
        manageRequests(email)
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

#offerRide()
#searchRide("don@mayor.yeg")
#postRequest("don@mayor.yeg")

#loginScreen()
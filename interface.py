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
        

def offerRide(email):
    # Menu for offering a ride, feature 1 in spec

    os.system('clear')
    date = input("Enter date (YYYY-MM-DD): ")
    seats = int(input("Enter the number of seats: "))
    price = int(input("Enter the price per seat: "))
    lugg = input("Enter the luggage description: ")

    src = input("Enter source location: ")
    matches = backend.findLoc(src)
    if len(matches) == 0:
        input("No matches found, press enter to continue")
        offerRide(email)
    elif len(matches) == 1:
        srclcode = matches[0][0]
    else:
        location = showFive(matches, "lcode, city, prov, address")
        srclcode = location[0]
    
    dst = input("Enter destination location: ")
    matches = backend.findLoc(dst)
    if len(matches) == 0:
        input("No matches found, press enter to continue")
        offerRide(email)
    elif len(matches) == 1:
        dstlcode = matches[0][0]
    else:
        location = showFive(matches, "lcode, city, prov, address")
        dstlcode = location[0]
    
    cno = input("Enter car number, or -1 if none: ")
    if cno == "-1":
        cno = None
    enroutes = input("Enter enroute locations, separated by commas, or -1 for none: ").split(",")

    if enroutes[0] == "-1":
        enrouteslcode = None
    else:
        enrouteslcode = []
        for route in enroutes:
            matches = backend.findLoc(route)
            location = showFive(matches, "lcode, city, prov, address")
            lcode = location[0]
            enrouteslcode.append(lcode)    
    
    backend.offerRide(email, date, seats, price, lugg, srclcode, dstlcode, enrouteslcode, cno)


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

    while True:
        os.system('clear')
        print("1: List bookings")
        print("2: Cancel a booking")
        print("3: Book a member")
        print("4: Return to menu")
        choice = input("Make a selection by entering a number: ")

        if choice == "1":
            os.system('clear')
            matches = backend.findMatchingBookings(email)

            print("|booking number|email|ride number|cost|seats|pickup|dropoff|\n")
            for match in matches:
                print(match)
            input("Press enter to continue")

        elif choice == "2":
            os.system('clear')
            matches = backend.findMatchingBookings(email)
            booking = showFive(matches, "|booking number|email|ride number|cost|seats|pickup|dropoff|")

            backend.deleteBooking(booking[0])
            message = "Your booking from " + str(booking[5]) + " to " + str(booking[6]) + " has been cancelled"
            backend.sendMessage(booking[1], email, message, booking[2])

        elif choice == "3":
            os.system('clear')

            matches = backend.findMatchingRides(email)

            ride = showFive(matches, "rno, price, rdate, seats, lugDesc, src, dst, driver, cno")

            bookedEmail = input("Enter the email of the member to book: ")
            seatsBooked = input("Enter the number of seats to book: ")
            seatCost = input("Enter cost per seat: ")
            pickup = input("Enter pickup location code: ")
            dropoff = input("Enter dropoff location code: ")

            backend.issueBooking(bookedEmail, ride[0], seatCost, seatsBooked, pickup, dropoff)

        elif choice == "4":
            menu(email)
        


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
    while True:
        os.system('clear')
        print("1: List all your ride requests")
        print("2: Delete ride request")
        print("3: Search for ride requests and message the reqesting member")
        print("4: Return to menu")
        choice = input("Make a selection by entering a number: ")

        if choice == "1":
            requests = backend.retRequest(email)
            
            if len(requests) == 0:
                input("\nNo requests to show, press enter to continue")
                manageRequests(email)

            showFive(requests, "rid, email, pickup, dropoff, date, amount")
        elif choice == "2":
            requests = backend.retRequest(email)

            if len(requests) == 0:
                input("\nNo requests to show, press enter to continue")
                manageRequests(email)

            request = showFive(requests, "rid, email, pickup, dropoff, rdate, amount")
            backend.deleteRequest(request[0])

        elif choice == "3":
            keyword = input("Enter lcode or pickup city: ")
            requests = backend.retLocation(keyword)

            if len(requests) == 0:
                input("\nNo requests to show, press enter to continue")
                manageRequests(email)

            request = showFive(requests, "rid, email, pickup, dropoff, rdate, amount")

            message = input("Enter message content: ")
            backend.sendMessage(request[1], email, message, int(request[0]))         
            print("Message sent, press enter to continue")

            menu(email)
        elif choice == "4":
            menu(email)

def menu(email):
    while True:
        os.system('clear')
        print("Logged in as:", email)
        print()

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
            offerRide(email)
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
#menu("don@mayor.yeg")


loginScreen()
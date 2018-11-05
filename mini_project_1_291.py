# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "ohi-i"
__date__ = "$Oct 25, 2018 3:26:05 PM$"

import sqlite3
import time
import hashlib

connection = None
cursor = None

class MismatchError(Exception):
    def __init__(self, message):
        self.message = message
        

def connect(path):
    # Taken from Lab
    global connection, cursor
    
    connection = sqlite3.connect(path)
    cursor = connection.cursor()    
    connection.commit()
    return
    
def initTables():
    # written by ohiwere
    global connection, cursor
    
    cursor.execute("DROP TABLE IF EXISTS requests;")
    cursor.execute("DROP TABLE IF EXISTS enroute;")
    cursor.execute("DROP TABLE IF EXISTS bookings;")
    cursor.execute("DROP TABLE IF EXISTS rides;")
    cursor.execute("DROP TABLE IF EXISTS locations;")
    cursor.execute("DROP TABLE IF EXISTS cars;")
    cursor.execute("DROP TABLE IF EXISTS members;")
    cursor.execute("DROP TABLE IF EXISTS inbox;")
    
    cursor.execute("PRAGMA foreign_keys=ON")
                    
    cursor.execute(""" CREATE TABLE members (
                    email		CHAR(15),
                    name		CHAR(20),
                    phone		CHAR(12),
                    pwd                 CHAR(6),
                    PRIMARY KEY (email));
                    """)
                    
    cursor.execute(""" CREATE TABLE cars (
                    cno		INT,
                    make	CHAR(12),
                    model	CHAR(12),
                    year	INT,
                    seats	INT,
                    owner	CHAR(15),
                    PRIMARY KEY (cno),
                    FOREIGN KEY (owner) REFERENCES members);
                    """)

    cursor.execute(""" CREATE TABLE locations (
                    lcode	CHAR(5),
                    city	CHAR(16),
                    prov	CHAR(16),
                    address	CHAR(16),
                    PRIMARY KEY (lcode));
                    """)

    cursor.execute("""CREATE TABLE rides (
                    rno		INT,
                    price	INT,
                    rdate	DATE,
                    seats	INT,
                    lugDesc	CHAR(10),
                    src		CHAR(5),
                    dst		CHAR(5),
                    driver	CHAR(15),
                    cno		INT,
                    PRIMARY KEY (rno),
                    FOREIGN KEY (src) REFERENCES locations,
                    FOREIGN KEY (dst) REFERENCES locations,
                    FOREIGN KEY (driver) REFERENCES members,
                    FOREIGN KEY (cno) REFERENCES cars);
                    """)
    
    cursor.execute("""CREATE TABLE bookings (
                    bno		INT,
                    email       CHAR(15),
                    rno		INT,
                    cost	INT,
                    seats	INT,
                    pickup	CHAR(5),
                    dropoff	CHAR(5),
                    PRIMARY KEY (bno),
                    FOREIGN KEY (email) REFERENCES members,
                    FOREIGN KEY (rno) REFERENCES rides,
                    FOREIGN KEY (pickup) REFERENCES locations,
                    FOREIGN KEY (dropoff) REFERENCES locations);
                    """)
    
    cursor.execute("""CREATE TABLE enroute (
                    rno		INT,
                    lcode	CHAR(5),
                    PRIMARY KEY (rno,lcode),
                    FOREIGN KEY (rno) REFERENCES rides,  
                    FOREIGN KEY (lcode) REFERENCES locations);
                    """)
    
    cursor.execute("""CREATE TABLE requests (
                    rid		INT,
                    email	CHAR(15),
                    rdate	date,
                    pickup	CHAR(5),
                    dropoff	CHAR(5),
                    amount	INT,
                    PRIMARY KEY (rid),
                    FOREIGN KEY (email) REFERENCES members,
                    FOREIGN KEY (pickup) REFERENCES locations,
                    FOREIGN KEY (dropoff) REFERENCES locations);
                    """)
                    
    cursor.execute("""CREATE TABLE inbox(
                    email CHAR(15),
                    msgTimestamp DATE,
                    sender CHAR(20),
                    content TEXT,
                    rno INT,
                    seen CHAR(1),
                    PRIMARY KEY(email, msgTimestamp)
                    FOREIGN KEY(email) REFERENCES members   
                    FOREIGN KEY(sender) REFERENCES members   
                    FOREIGN KEY(rno) REFERENCES rides);
                    """)
                    
    connection.commit()
                
    return


def initInserts():
    # written by ohiwere
    # insert test data into database, data courtesy of  Tanner Chell and Nicholas Leong, tchell@ualberta.ca and nleong1@ualberta.ca respectively
    global connection, cursor
    cursor.execute("""insert into members values 
        ('jane_doe@abc.ca', 'Jane Maria-Ann Doe', '780-342-7584', 'jpass'),
        ('bob@123.ca', 'Bob Williams', '780-342-2834', 'bpass'),
        ('maria@xyz.org', 'Maria Calzone', '780-382-3847', 'mpass'),
        ('the99@oil.com', 'Wayne Gretzky', '780-382-4382', 'tpass'),
        ('connor@oil.com', 'Connor Mcdavid', '587-839-2838', 'cpass'),
        ('don@mayor.yeg', 'Don Iveson', '780-382-8239', 'dpass'),
        ('darryl@oil.com', 'Darryl Katz', '604-238-2380', 'dpass'),
        ('reilly@esks.org', 'Mike Reilly', '780-389-8928', 'rpass'),
        ('mess@marky.mark', 'Mark Messier', '516-382-8939', 'mpass'),
        ('mal@serenity.ca', 'Nathan Fillion', '780-389-2899', 'mpass'),
        ('kd@lang.ca', 'K. D. Lang', '874-384-3890', 'kpass'),
        ('nellie@five.gov', 'Nellie McClung', '389-930-2839', 'npass'),
        ('marty@mc.fly', 'Micheal J. Fox', '780-382-3899', 'mpass'),
        ('cadence@rap.fm', 'Roland Pemberton', '780-938-2738', 'cpass'),
        ('john@acorn.nut', 'John Acorn', '780-389-8392', 'jpass');""")
        
    cursor.execute("""insert into cars values 
        (1, 'Honda', 'Civic', 2010, 4, 'jane_doe@abc.ca'),
        (2, 'Ford', 'E-350', 2012, 15, 'bob@123.ca'),
        (3, 'Toyota', 'Rav-4', 2016, 4, 'don@mayor.yeg'),
        (4, 'Subaru', 'Forester', 2017, 4, 'reilly@esks.org'),
        (5, 'Ford', 'F-150', 2018, 4, 'connor@oil.com'),
        (6, 'Ram', '2500', 2017, 4, 'mess@marky.mark'),
        (7, 'Toyota', 'Matrix', 2007, 4, 'maria@xyz.org'),
        (8, 'Dodge', 'Caravan', 2013, 6, 'mess@marky.mark'),
        (9, 'Ford', 'Flex', 2011, 4, 'maria@xyz.org'),
        (10, 'Volkswagon', 'Vanagon', 1974, 5, 'the99@oil.com'),
        (11, 'Toyota', 'Sienna', 2012, 6, 'john@acorn.nut'),
        (12, 'Honda', 'Accord', 2010, 4, 'john@acorn.nut'),
        (13, 'Jeep', 'Wrangler', 2007, 2, 'cadence@rap.fm');""")
    
    cursor.execute("""insert into locations values
        ('cntr1', 'Edmonton', 'Alberta', 'Rogers Place'),
        ('cntr2', 'Edmonton', 'Alberta', 'City Hall'),
        ('sth1', 'Edmonton', 'Alberta', 'Southgate'),
        ('west1', 'Edmonton', 'Alberta', 'West Ed Mall'),
        ('cntr3', 'Edmonton', 'Alberta', 'Tyrell Museum'),
        ('cntr4', 'Edmonton', 'Alberta', 'Citadel Theater'),
        ('cntr5', 'Edmonton', 'Alberta', 'Shaw Center'),
        ('sth2', 'Edmonton', 'Alberta', 'Black Dog'),
        ('sth3', 'Edmonton', 'Alberta', 'The Rec Room'),
        ('sth4', 'Edmonton', 'Alberta', 'MEC South'),
        ('nrth1', 'Edmonton', 'Alberta', 'MEC North'),
        ('nrth2', 'Edmonton', 'Alberta', 'Rexall Place'),
        ('nrth3', 'Edmonton', 'Alberta', 'Commonwealth'),
        ('nrth4', 'Edmonton', 'Alberta', 'Northlands'),
        ('yyc1', 'Calgary', 'Alberta', 'Saddledome'),
        ('yyc2', 'Calgary', 'Alberta', 'McMahon Stadium'),
        ('yyc3', 'Calgary', 'Alberta', 'Calgary Tower'),
        ('van1', 'Vancouver', 'British Columbia', 'BC Place'),
        ('van2', 'Vancouver', 'British Columbia', 'Rogers Arena'),
        ('sk1', 'Regina', 'Saskatchewan', 'Mosaic Field'),
        ('sk2', 'Saskatoon', 'Saskatchewan', 'Wanuskewin'),
        ('ab1', 'Jasper', 'Alberta', 'Jasper Park Lodge');
        --('van3', 'Abbotsford', 'British Columbia', 'Abbotsford Airport');""")
        
    cursor.execute("""insert into rides values
        (1, 50, '2018-11-01', 4, 'Large Bag', 'cntr1', 'yyc1', 'the99@oil.com', 10),
        (2, 50, '2018-11-05', 4, 'Large Bag', 'yyc1', 'cntr2', 'the99@oil.com', 10),
        (3, 50, '2018-11-30', 4, 'Medium Bag', 'cntr1', 'yyc1', 'mess@marky.mark', 8),
        (4, 30, '2018-11-17', 15, '5 large bags', 'nrth1', 'yyc2', 'bob@123.ca', 2),
        (5, 50, '2018-11-23', 3, 'Backpack', 'cntr2', 'yyc3', 'maria@xyz.org', 7),
        (6, 10, '2018-07-23', 4, 'Medium Bag', 'west1', 'sth4', 'don@mayor.yeg', 3),
        (7, 10, '2018-09-30', 4, 'Medium Bag', 'cntr2', 'cntr3', 'reilly@esks.org', 4),
        (8, 10, '2018-10-11', 4, 'Medium Bag', 'nrth1', 'sth2', 'connor@oil.com', 4),
        (9, 10, '2018-10-12', 4, 'Medium Bag', 'cntr5', 'sth3', 'jane_doe@abc.ca', 1),
        (10, 10, '2018-04-26', 4, 'Medium Bag', 'cntr4', 'cntr2', 'bob@123.ca', 2),
        (11, 100, '2018-08-08', 4, 'Medium Bag', 'cntr1', 'van1', 'mess@marky.mark', 6),
        (12, 100, '2018-05-13', 2, 'Medium Bag', 'sk1', 'van2', 'bob@123.ca', 2),
        (13, 75, '2018-06-11', 3, 'Large Bag', 'yyc1', 'sk2', 'the99@oil.com', 10),
        (14, 10, '2018-10-13', 4, 'Large Bag', 'sth4', 'yyc1', 'reilly@esks.org', 4),
        (15, 15, '2018-10-05', 5, 'Medium Bag', 'nrth4', 'yyc1', 'the99@oil.com', 10),
        (16, 75, '2018-10-03', 2, 'Small Bag', 'yyc3', 'sk2', 'connor@oil.com', 5),
        (17, 150, '2018-10-11', 3, 'Medium Bag', 'sk2', 'van1', 'jane_doe@abc.ca', 1),
        (18, 10, '2018-10-23', 3, 'Large Bag', 'nrth3', 'yyc1', 'don@mayor.yeg', 3),
        (19, 10, '2015-04-22', 4, 'Small Bag', 'cntr1', 'cntr2', 'bob@123.ca', 2),
        (20, 50, '2018-12-11', 1, 'Large Bag', 'cntr2', 'yyc2', 'the99@oil.com', 10),
        (21, 50, '2018-12-12', 1, 'Large Bag', 'cntr2', 'yyc3', 'the99@oil.com', 10),
        (22, 10, '2018-09-13', 1, 'Large Bag', 'cntr2', 'cntr4', 'the99@oil.com', 10),
        (23, 10, '2018-09-14', 1, 'Large Bag', 'cntr2', 'cntr5', 'the99@oil.com', 10),
        (24, 10, '2018-09-15', 1, 'Large Bag', 'cntr2', 'sth1', 'the99@oil.com', 10),
        (25, 10, '2018-09-16', 1, 'Large Bag', 'cntr2', 'sth2', 'the99@oil.com', 10),
        (26, 50, '2018-12-06', 1, 'Large Bag', 'cntr2', 'yyc1', 'bob@123.ca', 2),
        (27, 53, '2018-09-07', 2, 'Large Bag', 'cntr2', 'yyc3', 'bob@123.ca', 2),
        (28, 10, '2018-09-08', 1, 'Large Bag', 'cntr2', 'cntr4', 'bob@123.ca', 2),
        (29, 10, '2018-09-09', 1, 'Large Bag', 'cntr2', 'cntr5', 'bob@123.ca', 2),
        (30, 10, '2018-09-10', 1, 'Large Bag', 'cntr2', 'sth1', 'bob@123.ca', 2),
        (31, 10, '2018-09-11', 1, 'Large Bag', 'cntr2', 'sth2', 'bob@123.ca', 2),
        (32, 10, '2018-09-12', 1, 'Large Bag', 'cntr2', 'sth3', 'bob@123.ca', 2),
        (33, 10, '2018-09-01', 1, 'Large Bag', 'cntr2', 'cntr1', 'don@mayor.yeg', 3),
        (34, 10, '2018-09-02', 1, 'Large Bag', 'cntr2', 'nrth1', 'don@mayor.yeg', 3),
        (35, 10, '2018-09-03', 1, 'Large Bag', 'cntr2', 'cntr3', 'don@mayor.yeg', 3),
        (36, 10, '2018-09-04', 1, 'Large Bag', 'cntr2', 'cntr4', 'don@mayor.yeg', 3),
        (37, 10, '2018-09-05', 1, 'Large Bag', 'cntr2', 'sth1', 'don@mayor.yeg', 3),
        (38, 10, '2018-09-06', 1, 'Large Bag', 'cntr2', 'sth2', 'don@mayor.yeg', 3),
        (39, 10, '2018-09-07', 1, 'Large Bag', 'cntr2', 'sth3', 'don@mayor.yeg', 3),
        (40, 50, '2018-09-08', 1, 'Large Bag', 'cntr2', 'yyc1', 'don@mayor.yeg', 3),
        (41, 100, '2018-11-05', 2, 'Large Bag', 'cntr1', 'sk1', 'don@mayor.yeg', 3),
        (42, 150, '2018-11-05', 2, 'Large Bag', 'van2', 'nrth2', 'don@mayor.yeg', 3),
        (43, 10, '2018-10-14', 4, 'Large Bag', 'sth4', 'yyc1', 'jane_doe@abc.ca', 1);""")
    
    cursor.execute("""insert into bookings values
        (1, 'connor@oil.com', 1, null, 1, null, null),
        (2, 'connor@oil.com', 2, null, 1, null, null),
        (3, 'kd@lang.ca', 3, 45, 1, 'cntr2', null),
        (4, 'reilly@esks.org', 4, 30, 13, null, null),
        (5, 'don@mayor.yeg', 5, 50, 1, 'cntr2', 'yyc3'),
        (6, 'marty@mc.fly', 18, null, 3, null, null),
        (7, 'darryl@oil.com', 20, null, 1, null, null),
        (8, 'john@acorn.nut', 26, null, 1, null, null),
        (9, 'cadence@rap.fm', 27, null, 1, null, null),
        (10, 'connor@oil.com', 5, 45, 1, null, null),
        (11, 'mal@serenity.ca', 41, null, 1, null, null),
        (12, 'nellie@five.gov', 42, null, 1, null, null);""")
    
    cursor.execute("""insert into enroute values
        (12, 'yyc1'),
        (16, 'sk1'),
        (17, 'cntr2');""")
    
    cursor.execute("""insert into requests values
        (1, 'darryl@oil.com', '2018-07-23', 'nrth1', 'cntr1', 10),
        (2, 'nellie@five.gov', '2018-07-22', 'west1', 'sth4', 10),
        (3, 'mal@serenity.ca', '2018-10-11', 'nrth2', 'sth3', 10),
        (4, 'don@mayor.yeg', '2018-10-11', 'nrth2', 'sth3', 10),
        (5, 'the99@oil.com', '2018-10-11', 'nrth1', 'ab1', 10),
        (6, 'marty@mc.fly', '2018-10-11', 'sk1', 'sth3', 10),
        (7, 'mess@marky.mark', '2018-10-11', 'nrth2', 'sth3', 1),
        (8, 'mess@marky.mark', '2018-10-11', 'nrth2', 'sth3', 100),
        (9, 'jane_doe@abc.ca', '2018-04-26', 'cntr3', 'cntr2', 10);""")
    
    cursor.execute("""insert into inbox values
        ('don@mayor.yeg', '2018-08-04', 'darryl@oil.com', 'message content is here', 36, 'n'),
        ('jane_doe@abc.ca', '2018-09-04', 'darryl@oil.com', '2nd message content is here', 43, 'n'),
        ('don@mayor.yeg', '2018-10-04', 'darryl@oil.com', '3rd message content is here', 42, 'n');""")
        
    connection.commit()
    return


def offerRide(member, date, seats, seatprice, luggage_descrip, source, dest, enroute = None, cno = None):
    # written by ohiwere
    # create a ride that a member is offering and add it to database
    # assumes all location vars are lcodes
    global connection, cursor
    
    # generate new ride number
    cursor.execute("SELECT MAX(rno) FROM rides;")
    rno = cursor.fetchone() # done this way because can return None
    
    if rno is None:
        rno = 1
    else:
        rno = int(rno[0])
        rno += 1

    if cno is not None:
        cursor.execute("SELECT cno FROM members, cars WHERE email = ? AND owner = email;", (member,))
        list = cursor.fetchall() # could potentially own more than one car
        flag = False
        for l in list:
            if l[0] is not None and l[0] is cno:
                flag = True
        if flag is False:
            raise MismatchError("Specified car number didn't match one of yours!")            

    # rides(rno, price, rdate, seats, lugDesc, src, dst, driver, cno)
    cursor.execute("""INSERT INTO rides VALUES(?,?,?,?,?,?,?,?,?);
                    """, (rno, seatprice, date, seats, luggage_descrip, source, dest, member, cno))
                    
    # now handle enroutes, if any
    if enroute is not None:
        for e in enroute: # expecting e to be list of lcodes
            cursor.execute("INSERT INTO enroute VALUES(?,?);", (rno, e))
      
    # all done
    connection.commit()
    return

def findLoc(location):
    # written by ohiwere
    # get a string that could be lcode or a substring of city, address, or province. Call before offerRide to get src,dest
    # in both cases, will return a list, but if location is an lcode, there will only be 1 item
    global connection, cursor
    
    retlist = []
    cursor.execute("SELECT lcode FROM locations WHERE (lcode = ?);", (location,))
    list = cursor.fetchall()        
    for l in list:
        retlist.append(l[0])
    cursor.execute("SELECT lcode FROM locations WHERE (city LIKE ? OR prov LIKE ? OR address LIKE ?);", ('%'+location+'%','%'+location+'%','%'+location+'%'))
    list = cursor.fetchall()        
    for l in list:
        retlist.append(l[0])    
    
    return retlist

def rideSearchFromKeyword(keywords):
    # keywords is a tuple
    global connection, cursor
    
    potentialMatches = []
    
    for kw in keywords:
        cursor.execute("""SELECT c.cno, c.make, c.model, c.year, c.seats, c.owner, matching.rno, matching.price, matching.rdate, matching.seats, matching.lugDesc, matching.src, matching.dst, matching.driver, matching.cno, matching.lcode
                        FROM cars c, (SELECT *
                                    FROM rides r, locations l
                                    WHERE (lcode = r.src OR lcode = r.dst OR lcode IN(SELECT lcode 
                                                                                            FROM enroute
                                                                                            WHERE enroute.rno = r.rno)
                                    ) AND (lcode = ? OR city LIKE ? OR prov LIKE ? OR address LIKE ?)) matching
                        WHERE matching.cno = c.cno""", (kw, "%"+kw+"%", "%"+kw+"%", "%"+kw+"%"))
                        
        potentialMatches.append(set(cursor.fetchall()))
        
#        cursor.execute("""SELECT r.rno, r.price, r.rdate, r.seats, r.lugDesc, r.src, r.dst, r.driver, r.cno, lcode
#                          FROM rides r, locations 
#                          WHERE lcode = r.src OR lcode = r.dst OR lcode IN(SELECT lcode 
#                                                                            FROM enroute
#                                                                            WHERE enroute.rno = r.rno); """)

        cursor.execute("""SELECT *
                        FROM rides, locations
                        WHERE (lcode = src OR lcode = dst OR lcode IN(SELECT lcode
                                                                       FROM enroute
                                                                       WHERE enroute.rno = rides.rno))AND (lcode = ? OR city LIKE ? OR prov LIKE ? OR address LIKE ?) """, ('berta', '%berta%', '%berta%', '%berta%'))
#        t = cursor.fetchall()
#        for q in t:
#            pass
##            print(q)        
#        
#        print()
    
    if not potentialMatches:
        return []
    
    finalSet = potentialMatches[0]
    for i in range(1, len(potentialMatches)):
        finalSet = finalSet.intersection(potentialMatches[i])
        
    return list(finalSet)

def findMatchingBookings(member):
#    written by ohiwere
    global connection, cursor
    
#    |bno|email|rno|cost|seats|pickup|dropoff|
    cursor.execute("""SELECT bno, email, b.rno, b.cost, b.seats, pickup, dropoff
                    FROM rides r, bookings b
                    WHERE r.rno = b.rno AND driver = ?;""", (member,))
    
    return cursor.fetchall()

def deleteBooking(bno):
#    written by ohiwere
    global connection, cursor
    
    cursor.execute(""" DELETE FROM bookings 
                        WHERE bno = ?;
                    """, (bno,))
                    
    connection.commit()

def issueBooking(email, rno, cost, seats, pickup, dropoff):
#    written by ohiwere
    global connection, cursor
#    |bno|email|rno|cost|seats|pickup|dropoff|

    cursor.execute("""SELECT MAX(bno) FROM bookings;""")
    
    bno = cursor.fetchone()
    
    if bno is None:
        bno = 1
    else:
        bno = int(bno[0]) + 1
        
    cursor.execute("""INSERT INTO bookings VALUES(?,?,?,?,?,?,?); """, (bno, email, rno, cost, seats, pickup, dropoff))
    connection.commit()
    

def sendMessage(to, from_, message, rno):
    # written by ohiwere
    global connection, cursor
    
    # make sure that rno matches a ride offered by either sender or recipient
    check1 = True
    cursor.execute("""SELECT driver
                    FROM rides
                    WHERE rno = ? AND driver = ?;""", (rno, from_))
    res = cursor.fetchone()
    if res is None:
        check1 = False
    
    check2 = True
    cursor.execute("""SELECT driver
                    FROM rides
                    WHERE rno = ? AND driver = ? ;""", (rno, to))
    res = cursor.fetchone()
    if res is None:
        check2 = False
    
    if (check1 or check2) is False:
        raise MismatchError("Ride not associated with message participants!")
    
    cursor.execute("""INSERT INTO inbox VALUES(?, date('now), ?, ?, ?, 'n');""", (to, from_, message, rno))
    connection.commit()

# written by Shiv
def postRideRequest(rdate, email, pickup, dropoff, amount):

    global connection, cursor

    cursor.execute("""SELECT MAX(rid) FROM requests;""")
    rid = cursor.fetchone()

    # handles unique rid
    if rid is None:
        rid = 1
    else:
        rid = int(rid[0])
        rid += 1

    cursor.execute("""INSERT INTO requests VALUES(?, ?, ?, ?, ?, ?);""", (rid, email, rdate, pickup, dropoff, amount))

    connection.commit()


def checkLogin(email, password):
    # written by Noah
    # checks if a username and password pair is valid. 
    # Returns True if valid, False if not

    global connection, cursor

    cursor.execute("""SELECT pwd FROM members WHERE email = ? """, (email, ))
    storedPwd = cursor.fetchone()

    if storedPwd[0] is None:
        return False

    return (password == storedPwd[0])


def getUnreadMessages(email):
    # written by Noah
    # Returns a list of the contents of all unread messages for a given user
    # Sets messages to read

    global connection, cursor

    cursor.execute("""SELECT content FROM inbox WHERE seen = 'n' AND email = ? """, (email, ))
    messages = cursor.fetchall()

    cursor.execute("""UPDATE inbox SET seen = 'y' """)

    return(messages)


def addMember(email, name, phone, password):
    # written by Noah
    # Adds a new member if the email is unique
    # Returns True if successful, False if not

    global connection, cursor

    cursor.execute("""SELECT email FROM members WHERE email = ?""", (email, ))
    existingEmail = cursor.fetchall()

    if existingEmail == []: 
        cursor.execute("""INSERT INTO members VALUES(?, ?, ?, ?)""", (email, name, phone, password))
        connection.commit()
        return True
    else:
        return False

# written by Shiv
def retRequest(email):

    global connection, cursor

    cursor.execute("""SELECT rid FROM requests WHERE email = ?;""", (email, ))

    return rid

# written by Shiv
def deleteRequest(email):

    global connection, cursor

    cursor.execute("""DELETE FROM requests WHERE email = ?;""", (email, ))

    connection.commit()

# written by Shiv
def retLocation(pickup):

    global connection, cursor

    cursor.execute("""SELECT rid FROM requests WHERE pickup = ?""", (pickup, ))

    return rid

def main():
    global connection, cursor
    connect("Delivery_Service.db")
    initTables()
    initInserts()
    
#    Testing Stuff
#    offerRide("jane_doe@abc.ca", '2018-10-31', 3, 1.50, 'No bag', findLoc('berta')[0], findLoc('berta')[1], enroute = ['van1', 'van2'])
#    cursor.execute("SELECT * FROM rides WHERE rno >= (SELECT MAX(rno) FROM rides);")
#    print(cursor.fetchall())
    
#    r = rideSearchFromKeyword(("berta", "all"))
#    for thing in r:
#        print(thing)
    
    
#    print(findLoc('MEC'))
    print("\nDone.")
    return

if __name__ == "__main__":
    main()
    

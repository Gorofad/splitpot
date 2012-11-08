#!/usr/bin/python
#
# Parse database
#

import sqlite3 as lite
import sys
import random
import hashlib
import logging

sys.path.append('utils/')
import Encryption

DB_FILE = 'resource/splitpotDB_DEV.sqlite'
SALT_LENGTH = 30

log = logging.getLogger("appLog")

# connects to a given database file
log.info("connecting to database...")
connection = lite.connect(DB_FILE, check_same_thread = False)

def clear():
  """
  Clears *ALL THE FUCKING DATA* from the Database
  """
  log.info("kill database - right now")
  with connection:
    cur = connection.cursor()
    cur.execute("DELETE FROM splitpot_participants")
    cur.execute("DELETE FROM splitpot_events")
    cur.execute("DELETE FROM splitpot_users")


def verifyLogin(email, password):
    log.info("verify user and given password")
    with connection:
        cur = connection.cursor()
        cur.execute("SELECT salt FROM splitpot_users WHERE email = ?", [email])
        userSalt = (cur.fetchone() or [""])[0]
        if (userSalt == ""): return False
        cur.execute("SELECT password FROM splitpot_users WHERE email = ?", [email])
        hashedPw = cur.fetchone()[0]

    return True if (Encryption.hashPassword(userSalt, password) == hashedPw) else False

# returns a list with all events
def listEvents():
    with connection:
        cur = connection.cursor()
        cur.execute("SELECT * FROM splitpot_events")
        events = cur.fetchall()

    return events

def listEventsFor(user):
  with connection:
    cur = connection.cursor()
    cur.execute("SELECT splitpot_events.id, date, comment, amount FROM splitpot_events, splitpot_participants WHERE splitpot.participants.event = splitpot_events.id AND (owner = 'user' or user = 'user'")
    events = cur.fetchalll()
  return events

# inserting a new event with the given parameters and return the event ID
def insertEvent(owner, date, amount, participants, comment):
    with connection:
        cur = connection.cursor()
        if not userExists(owner):
            tmpPassword = Encryption.generateRandomChars(6)
            registerUser(owner, "Not Registered", tmpPassword)

        for curParticipant in participants:
             if not userExists(curParticipant):
                 tmpPassword = Encryption.generateRandomChars(6)
                 registerUser(curParticipant, "Not Registered", tmpPassword)

        cur.execute("INSERT INTO splitpot_events VALUES (?,?,?,?,?,?)", (None, owner, date, amount, str(participants), comment))

        cur.execute("SELECT * FROM splitpot_events ORDER BY ID DESC limit 1")
        eventID = cur.fetchone()[0]
        updateParticipantTable(participants, eventID, "new")
    return eventID

# update the participant table with a given event and list of
# participants
def updateParticipantTable(participants, eventID, status):
    log.info("update participants table")
    with connection:
        cur = connection.cursor()
        for curParticipant in participants:
            cur.execute("INSERT INTO splitpot_participants VALUES (?, ?, ?)", (curParticipant, eventID, status))
    return True

# checks if an user already exists
def userExists(email):
    log.info("check if email: " + email + " exists.")
    with connection:
        cur = connection.cursor()
        cur.execute("SELECT count(*) FROM splitpot_users WHERE email = ?", [email.lower()])
        exists = cur.fetchone()[0]
    return False if exists == 0 else True

# register a new user
def registerUser(email, name, password):
    if not userExists(email):
         with connection:
              salt = Encryption.generateRandomChars(SALT_LENGTH)
              hashedPassword = Encryption.hashPassword(salt, password)

              cur = connection.cursor()
              cur.execute("INSERT INTO splitpot_users VALUES (?, ?, ?, ?, ?)", (email.lower(), name, 0, salt, hashedPassword))

         return True
    else:
         print "User already exists"
         return False

# return hashedPassword
def getPassword(email):
     if userExists(email):
          with connection:
               cur = connection.cursor()
               cur.execute("SELECT password FROM splitpot_users WHERE email = ?", [email])
               pw = cur.fetchone()[0]
               return pw
     else:
          log.warning("Can't return password of " + email + ", because user doesn't exist")

# set the event status for a given user
def setEventStatus(email, event, status):
     with connection:
          cur = connection.cursor()
          cur.execute("SELECT COUNT(*) FROM splitpot_participants WHERE user = ? AND event = ?", (email, event))
          curEvent = cur.fetchone()[0]
          if curEvent != 0:
               cur.execute("UPDATE splitpot_participants SET status = ? WHERE user = ? AND event = ?", (status, email, event))
               return True
          else:
               log.warning(str(event) + " or " + email + " doesn't exist")

def main():
    listEvents() #TODO  move to testcase
    print getPassword("martin@0xabc.de")
    print setEventStatus("tobstu@gmail.com", 2, "paid")
    insertEvent("martin@dinhnet.de", "4.11.2012", 312.33,
                ["martin@dinhmail.de", "tobstu@gmail.com", "peter@0xabc.de", "hans@0xabc.de"],
                "New Event")

# call main method
main()

# isValidResetUrl
    # email
    # url-key

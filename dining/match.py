import sqlite3 as lite
from sendEmail import sendEmail
import sys
import json
def match():
    # declare local variables
    matches = dict()
    favorites = dict()

    # connect with the database
    con = lite.connect('db.sqlite3')

    # read and evaluate today.json
    global today
    file = open('today.json')
    today = json.load(file)
    file.close()

    # fetch IDs for dining items corresponding with today's menu items
    with con:
	for dhall in today:
            for meals in dhall['menus']:
		    item = meals['name']
                    cur = con.cursor()

		    # fetch ID corresponding with the dining item
                    cur.execute("SELECT id FROM users_item WHERE name = '"+item+"'")
                    item_ID = cur.fetchone()
		    
		    # fetch netID IDs corresponding with IDs previously fetched
		    cur.execute("SELECT netid_id FROM users_netid_favorites WHERE item_id = '"+ str(item_ID[0])+ "'")
		    #netID_ID = cur.fetchone() # fetch all?
                    for netID_ID in cur.fetchall():

                        # fetch the netid corresponding with the netID ID
                        cur.execute("SELECT netid FROM users_netid WHERE id = '" + str(netID_ID[0])+"'")
                        netID = cur.fetchone()[0]		    

                        # add item from today's menu to list corresponding with user if user favorited the item
                        if netID in matches:
			    tup = (item, dhall['dhall'], dhall['meal'])
                            matches[netID].append(tup)
                        else:		    
                            matches[netID] = [(item, dhall['dhall'], dhall['meal'])]			
	
    # eventually the comparisons will be made with database items instead of dictionary items
    sendEmail(matches)

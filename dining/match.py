import sqlite3 as lite
from sendEmail import sendEmail
import sys
import json
def main():
    # declare local variables
    matches = dict()
    favorites = dict()

    # connect with the database
    con = lite.connect('db.sqlite3')

    # fetch data from the database
    #with con:                                                                                                                                                
        #cur = con.cursor()
        #cur.execute("SELECT * FROM users_item")
        #rows = cur.fetchall()
        #for row in rows:
        #    print row

    # read and evaluate today.json
    global today
    file = open('today.json')
    today = json.load(file)
    file.close()

    # fetch IDs for dining items corresponding with today's menu items
    with con:
	for dhall in today:
            for meal in dhall['menus']:
                for item in meal:
                    cur = con.cursor()
                    cur.execute("SELECT id FROM users_item WITH '" + item + "'")
                    item_ID = cur.fetchone()
		    
		    # fetch dining items corresponding with IDs previously fetched
		    cur.execute("SELECT netid_id FROM users_netid_favorites WITH '" + item_ID + "'")
		    netID_ID = cur.fetchone() # fetch all?
		    cur.execute("SELECT netid FROM users_netid WITH '" + netID_ID + "'")
		    netID = cur.fetchone()		    

		    # add item from today's menu to list corresponding with user if user favorited the item
		    if netID in matches:
                        matches[netID].append((item, dhall, meal))
                    else:		    
			matches[netID] = [(item, dhall, meal)]			
	
	

    # eventually the comparisons will be made with database items instead of dictionary items
    # favorites[0] = {'user': 'Lisa Kim', 'items': ['Penne Pasta']}
    # favorites[1] = {'user': 'Diogo Adrados', 'items': ['Banana & Chocolate French Toast', 'Country Fried Southern Chicken']}
    # favorites[2] = {'user': 'David Paulk', 'items': ['Filet Mignon']}
    #for i in range(len(today)):
    #    for j in range(len(today[i]['menus'])):
    #        # (access database to get users' favorite dining items)
    #        for k in range(len(favorites)):
    #            if today[i]['menus'][j]['name'] in favorites[k]['items']:
    #                if favorites[k]['user'] in matches:
    #                    matches[favorites[k]['user']].append(today[i]['menus'][j]['name'])
    #                else:
    #                    matches[favorites[k]['user']] = [today[i]['menus'][j]['name']]
    #for netID in matches.keys():
    #    print ('user netID: ' + netID)
    #    print ('favorites served today:')
    #    for item in matches[netID]:
    #        print item
    
    sendEmail(matches)
main()

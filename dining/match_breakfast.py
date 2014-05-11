#!/usr/bin/env python
import MySQLdb
from sendEmail2 import sendEmail
import sys, os
import json
import Levenshtein
def match():

    # declare local variables
    matches = dict()
    dictation = dict() # for matches tuplets (value) organized by dhall (key)
    favorites = dict()

    # connect with the database
    con = MySQLdb.connect(user='tigerbites', db='db_mysql',passwd='princetoncos333', host='localhost') 
    #con = lite.connect('db.sqlite3')

    # read and evaluate today.json
    global today
    file = open('today.json')
    today = json.load(file)
    file.close()
    # fetch IDs for dining items corresponding with today's menu items
    with con:
	for dhall in today:
            if dhall['meal'] == 'BREAKFAST':
                for meals in dhall['menus']:
                    #print meals#['meal']#.encode('utf-8')
                    #print 'hello david!'
                    item_long = meals['name']
                    if len(item_long) > 50:
                        item = item_long[0:50]
                    else: 
                        item = item_long
                    cur = con.cursor()
                    
                    # fetch ID corresponding with the dining item
                    cur.execute("SELECT id FROM users_item WHERE name = '"+item+"'")
                    item_ID = cur.fetchone()
                    
                    cur.execute("SELECT isVegan FROM users_item WHERE name = '"+item+"'")
                    item_isVegan = cur.fetchone()[0]
                    
                    cur.execute("SELECT isVegetarian FROM users_item WHERE name = '"+item+"'")
                    item_isVegetarian = cur.fetchone()[0]
                    
                    cur.execute("SELECT isPork FROM users_item WHERE name = '"+item+"'")
                    item_isPork = cur.fetchone()[0]
                    
                    cur.execute("SELECT hasNuts FROM users_item WHERE name = '"+item+"'")
                    item_hasNuts = cur.fetchone()[0]
                    
                    cur.execute("SELECT * FROM users_item")
                    similarItems = []
                    for food in cur.fetchall():
                        
                        # check to make sure potential similar item has same allergen attributes
                        if item_isVegan != food[1] or item_isVegetarian != food[2] or item_isPork != food[3] or item_hasNuts != food[4]:
                            continue
                        similarity = Levenshtein.ratio(food[6], item.encode('utf-8'))
                        if (len(food[6]) > len(item)):
                            ratio = float(len(item))/float(len(food[6]))
                        else:
                            ratio = float(len(food[6]))/float(len(item))
                        if (similarity > 0.8) and (ratio < 1.0) and (ratio > 0.5):
                            cur.execute("SELECT id FROM users_item WHERE name = '"+food[6]+"'")
                            similarItem_ID = cur.fetchone()
                            cur.execute("SELECT netid_id FROM users_netid_favorites WHERE item_id = '"+ str(similarItem_ID[0])+ "'")
                            for similarNetID_ID in cur.fetchall():
                                
                                # fetch the netid corresponding with the netID ID                                       
                                cur.execute("SELECT netid FROM users_netid WHERE id = '" + str(similarNetID_ID[0])+"'")
                                similarNetID = cur.fetchone()[0]
                                
                            # add item from today's menu to list corresponding with user if user favorited the item
                                if similarNetID in matches:
                                    #similarTup = (item, dhall['dhall'], dhall['meal'], food[6])
                                    similarTup = (item, dhall['meal'], food[6]) 
                                    if dhall['dhall'] in matches[similarNetID].keys():
                                        matches[similarNetID][dhall['dhall']].append(similarTup)
                                    else:
                                        matches[similarNetID][dhall['dhall']] = [similarTup]
                                        #matches[similarNetID].append(similarTup)
                                else:
                                    #matches[similarNetID] = [(item, dhall['dhall'], dhall['meal'], food[6])]
                                    matches[similarNetID] = {dhall['dhall'] : [(item, dhall['meal'], food[6])]}
                        # fetch netID IDs corresponding with IDs previously fetched
                        cur.execute("SELECT netid_id FROM users_netid_favorites WHERE item_id = '"+ str(item_ID[0])+ "'")
                    for netID_ID in cur.fetchall():
                        
                        # fetch the netid corresponding with the netID ID
                        cur.execute("SELECT netid FROM users_netid WHERE id = '" + str(netID_ID[0])+"'")
                        netID = cur.fetchone()[0]		    
                        
                            # add item from today's menu to list corresponding with user if user favorited the item
                        if netID in matches:
                            somevar = False
                            for foodtup in matches[netID]:
                                if (foodtup[0] == item):
                                    if (foodtup[3] != None):
                                        matches[netID].remove(foodtup)
                                        newtup = (item, dhall['dhall'], dhall['meal'], None)
                                        matches[netID].append(newtup)
                                        somevar = True
                                        break
                            if somevar == False:
                                #tup = (item, dhall['dhall'], dhall['meal'], None) # DHALL ORDERING CHANGE
                                tup = (item, dhall['meal'], None)
                                if dhall['dhall'] in matches[netID].keys():
                                    matches[netID][dhall['dhall']].append(tup)
                                else:
                                    matches[netID][dhall['dhall']] = [tup]
                        else:
                            #matches[netID] = [(item, dhall['dhall'], dhall['meal'], None)] # DHALL ORDERING CHANGE			
                            matches[netID] = {dhall['dhall'] : [(item, dhall['meal'], None)]}
    # eventually the comparisons will be made with database items instead of dictionary items
    sendEmail(matches)

os.chdir("/home/ubuntu/TigerBites/dining")    
match()

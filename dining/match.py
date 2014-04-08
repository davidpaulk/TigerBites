import sqlite3 as lite
import sys
import json

def main():

    # connect with the database
    con = lite.connect('../db.sqlite3')

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

    # attempt at getting ids for today's dining items
    #with con:
    #    cur = con.cursor()
    #    cur.execute("SELECT * FROM menus")
    #    rows = cur.fetchall()
    #    for row in rows:
    #        for field in row:
    #            print field
    #        for dhall in today:
    #            for meal in dhall['menus']:
    #                for item in meal:
    #                    blah = 1
    # eventually the comparisons will be made with database items instead of dictionary items
    matches = dict()
    favorites = dict()
    favorites[0] = {'user': 'Lisa Kim', 'items': ['Penne Pasta']}
    favorites[1] = {'user': 'Diogo Adrados', 'items': ['Banana & Chocolate French Toast', 'Country Fried Southern Chicken']}
    favorites[2] = {'user': 'David Paulk', 'items': ['Filet Mignon']}
    for i in range(len(today)):
        for j in range(len(today[i]['menus'])):
            # (access database to get users' favorite dining items)
            for k in range(len(favorites)):
                if today[i]['menus'][j]['name'] in favorites[k]['items']:
                    if favorites[k]['user'] in matches:
                        matches[favorites[k]['user']].append(today[i]['menus'][j]['name'])
                    else:
                        matches[favorites[k]['user']] = [today[i]['menus'][j]['name']]
    for i in matches.keys():
        print ('user: ' + i)
        print ('favorites served today:')
        for j in matches[i]:
            print i
            # sendEmail({netid : [dining_item, dining_hall, meal_time], ...})
main()

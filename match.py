import sys
import json

def main():

    # read and evaluate today.json
    global today
    file = open('today.json')
    today = json.load(file)
    file.close()

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
            print j
main()

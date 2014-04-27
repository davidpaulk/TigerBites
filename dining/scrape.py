#!/usr/bin/env python

import urllib
from bs4 import BeautifulSoup
import os, sys, json
from datetime import date
from subprocess import call
import subprocess
import MySQLdb
from match import match

# function that returns menu url based on dining hall input
def getMealUrl(str):   

   dhallcodes = {"ROCKY":"01",
                "WILSON":"02",
                "FORBES":"03",
                "GRADCOLLEGE":"04",
                "CJL":"05",
                "WHITMAN":"08", }
   
   # replace dining hall name with number in url
   code = dhallcodes[str]   
   url = "http://facilities.princeton.edu/dining/_Foodpro/menu.asp?locationNum="+code
   return url;

# parses query and gets desired meal and dhall
def getMeals(str, today):
    # Get URL
    url = getMealUrl(str)
    
    # Fetch HTML
    f = urllib.urlopen(url)
    html = f.read()

    # Get BeautifulSoup Object
    soup = BeautifulSoup(html)

    # get list and length
    foodlist = soup.find_all('div') 
    length = len(foodlist)

    first = False
    if str == "ROCKY":
      first = True

    outfile = open(today, 'a')
    meals = dict()


    # go through and find all meals, and all foods in the meals
    for meal in soup.find_all('meal'):
        if first:
          outfile.write('[\n')
          first = False
        else:
          outfile.write(',\n')
        meals = dict()
        meals["dhall"] = str
        mealName =  meal['name'].upper()
        meals["meal"] = mealName
        mealMenuList = list()
        for entree in meal.find_all('entree'):
          entreeType = entree['type'].upper()
          entreeType = entreeType.replace("-- ","")
          entreeType = entreeType.replace(" --","")
          dish = dict()
          for food in entree.find_all('name'):
            dish["type"] = entreeType

            dish["name"] = food.get_text().replace("'","")
            

          for isVegan in entree.find_all('vegan'):
             if (isVegan.get_text() == 'y'):
                dish["vegan"]=True
             else:
                dish["vegan"]=False

          for isVegetarian in entree.find_all('vegetarian'):
             if (isVegetarian.get_text() == 'y'):
                dish["vegetarian"]=True
             else:
                dish["vegetarian"]=False
          for isPork in entree.find_all('pork'):
             if (isPork.get_text() == 'y'):
                dish["pork"]=True
             else:
                dish["pork"]=False
          for hasNuts in entree.find_all('nuts'):
             if (hasNuts.get_text()=='y'):
                dish["nuts"]=True
             else:
                dish["nuts"]=False
             mealMenuList.append(dish)
          
#          try:
#             c.execute(""" INSERT INTO users_item(isVegan, isVegetarian, isPork, hasNuts, type, name) VALUES (%s, %s, %s, %s, %s, %s)""", (dish["vegan"], dish["vegetarian"],dish["pork"],dish["nuts"],dish["type"],dish["name"]))
#          except MySQLdb.IntegrityError:
#             continue

          c.execute(""" SELECT * FROM users_item where name = %s """,dish["name"])
          if c.fetchall():
             continue
          else:
             c.execute(""" INSERT INTO users_item(isVegan, isVegetarian, isPork, hasNuts, type, name) VALUES (%s, %s, %s, %s, %s, %s)""", (dish["vegan"], dish["vegetarian"],dish["pork"],dish["nuts"],dish["type"],dish["name"]))

         # mealMenuList.append(dish)
          
        meals["menus"] = mealMenuList
        json.dump(meals, outfile)

    return meals

   
def main():
  call(["rm", "-f", "today.json"])
  
  today = 'today.json'
  with open(today, 'w') as outfile:
    getMeals("ROCKY", today)
    getMeals("WILSON", today)
    getMeals("WHITMAN", today)
    getMeals("FORBES", today)
    getMeals("CJL", today)
    getMeals("GRADCOLLEGE", today)

  outfile = open(today, 'a') 
  outfile.write('\n]\n')

os.chdir("/home/ubuntu/TigerBites/dining")
conn = MySQLdb.connect(user='tigerbites', db='db_mysql',passwd='princetoncos333', host='localhost')
c = conn.cursor()
main()
conn.commit()
conn.close() 


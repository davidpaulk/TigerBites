import urllib
from bs4 import BeautifulSoup
import os, sys, json
from datetime import date
from subprocess import call
import subprocess

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

            dish["name"] = food.get_text()

          for isVegan in entree.find_all('vegan'):
            dish["vegan"] = isVegan.get_text()

          for isVegetarian in entree.find_all('vegetarian'):
            dish["vegetarian"] = isVegetarian.get_text()

          for isPork in entree.find_all('pork'):
            dish["pork"] = isPork.get_text()

          for hasNuts in entree.find_all('nuts'):
            dish["nuts"] = hasNuts.get_text()
            mealMenuList.append(dish)

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

main()
 

import urllib
from bs4 import BeautifulSoup
import os, sys
from datetime import date

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
def getMeals(str):
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

    #create meal dictionary
    meals = dict()

    # create dhall name entry
    meals["dhall"] = str

    # go through and find all meals, and all foods in the meals
    for meal in soup.find_all('meal'):
        mealName =  meal['name'].upper()
        mealMenuList = ""
        for entree in meal.find_all('entree'):
          entreeType = entree['type'].upper()
          entreeType = entreeType.replace("-- ","")
          entreeType = entreeType.replace(" --","")
          for food in entree.find_all('name'):
            mealMenuList+=entreeType+", "
            mealMenuList+=food.get_text()+", "
          for isVegan in entree.find_all('vegan'):
            mealMenuList+=isVegan.get_text()+", "
          for isVegetarian in entree.find_all('vegetarian'):
            mealMenuList+=isVegetarian.get_text()+", "
          for isPork in entree.find_all('pork'):
            mealMenuList+=isPork.get_text()+", "
          for hasNuts in entree.find_all('nuts'):
            mealMenuList+=hasNuts.get_text()+ "\n"
        meals[mealName] = mealMenuList

    return meals


def parse_query(query):
    dhall = ""
    meal = ""
    laundry = ""

    query = query.lower()
    
    #dhall dictionary
    dhalls   = {
       "wilson": "WILSON",
       "butler": "BUTLER",
       "forbes": "FORBES",
       "whitman": "WHITMAN",
       "rocky": "ROMA",
       "mathey": "ROMA",
       "gradcollege":"GRADCOLLEGE",
       "cjl":"CJL"
       }

    # meal dictionary
    meals    = {
       "lunch": "Lunch",
       "breakfast": "Breakfast",
       "brunch": "Brunch",
       "dinner": "Dinner"
       }


    #dhall case
    for key in dhalls:
        if key in query:
            type = "food"
            dhall = dhalls[key]

             # search for meal
            for key in meals:
                 if key in query:
                     meal = meals[key]

        
            return [type, dhall, meal]
         

def getMenu(query):

    
     
    # pass dhall to getMeals and get dictionary
    meals = getMeals(query)

    meal1 = "BREAKFAST"
    meal2 = "BRUNCH"
    meal3 = "LUNCH"
    meal4 = "DINNER"
    response = ""
    # print menu
    if (meals.has_key(meal1)):
      response = (meals["dhall"] + " " + meal1 + "\n")
      
      response+=meals[meal1]
    if (meals.has_key(meal2)):
      response+=(meals["dhall"] + " " + meal2 + "\n")
      response+=meals[meal2]

    if (meals.has_key(meal3)):
      response+=(meals["dhall"] + " " + meal3 + "\n")
      response+=meals[meal3]

    if (meals.has_key(meal4)):
      response+=(meals["dhall"] + " " + meal4 + "\n")
      response+=meals[meal4]


    
 
    return response
   
def main():
  print date.today()
  print getMenu("ROCKY").encode('utf-8')
  print getMenu("WILSON").encode('utf-8')
  print getMenu("WHITMAN").encode('utf-8')
  print getMenu("FORBES").encode('utf-8')
  print getMenu("CJL").encode('utf-8')
  print getMenu("GRADCOLLEGE").encode('utf-8')

main()
 

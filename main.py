#This is the Dorc For a discord Bot that allows user to pull prices for cards from www.facetofacegames.com
#This Bot is for personal use and I have no affiliation to FaceToFaceGames
#Program By Brandon Cuthbertson
import discord #for Bot
import os #imports form the .env file
import urllib.parse #for converting to url encoded
import re #regex modual
from bs4 import BeautifulSoup #for web Scraping
import requests #for web Scraping
from keep_alive import keep_alive

client = discord.Client() #discord Connection

discordColor = 0xc64d23 #At top so I dont have to search for it

@client.event
async def on_ready():
  print('Jacking into Discord {0.user}'.format(client)) #replacing 0 with client

@client.event
async def on_message(message):
  if message.author == client.user: #if author of the message is the bot do nothing
    return

  text = message.content  
  #get all words between $$ while there are two $$ that are not equal
  if text.find('$$') != -1 and text.rfind('$$') != -1 and text.find('$$') !=text.rfind('$$') != -1:
    #variables
    cardList = []
    num = 0
    #loops for each word
    while '$$' in text and num !=30:
      #to stop infintie loop while testing
      num += 1
      print("Num Count:" + str(num))
      #finds first two indexes
      start = text.find('$$') + 2
      end = text.find('$$', start)
      #sets word to variable and  adds word to list
      cardName = text[start:end]
      cardList.append(cardName)
      #removes word from string
      text = text.replace('$$'+ cardName +'$$', "" )    
      
    
    num = 0 #resets num after loop

    for x in cardList:
     #if cardname is empty or not a string
      if not x or x.isspace():
        #returns nothing
        return 
      
     
      elif "help" in x.casefold():
      #Gets How to use
          
        embedHelp=discord.Embed(title="HELP", description="This is my personal scraper, which will get you card prices Face to Face Games.\nTo search a Card just place the card name between two $$ \n\n eg. $$Ankle Shanker$$ \n\n\n", color=discordColor)
        
        await message.channel.send(embed=embedHelp)
      else:
        await message.channel.send(embed=search_card(x)) #sends a cards
        


def search_card(card_name):
  
  #Converts to url encoded 
  cardURL = urllib.parse.quote(joinSplit(card_name))
  print('\n\nLoading HTML for '+ joinSplit(card_name))
  
  #sets url for search based on insert
  url = os.getenv('url1') + cardURL + os.getenv('url2')
  response = requests.get(url, timeout=5) 
  print("status code is : " + str(response.status_code))
  print(response.reason)
  #set content to html page
  content = BeautifulSoup(response.content, "html.parser")
  

  #get result heading and remove whitespece
  isCardFound = joinSplit(content.find('h1',attrs={'class': 'page-heading'}).text)
  print(isCardFound)
  #pulls numbers out of isCardFound
  howManyFound = int(re.search(r'\b\d+\b', isCardFound).group(0))
  
  if howManyFound == 0:
   #if no results found print No Results Found
    return cardNotFound(card_name + " Not Found", "CARD SEARCH INCONCLUSIVE")
  elif len(card_name) <= 4 and howManyFound >= 200 :
      return cardNotFound("TO MANY CARDS", "PLEASE REFINE SEARCH")
      

  #else Do card retreval
  else:
    #list to verify items have been passed
    cardArray = []
    #Default embeded string
    embededVar = discord.Embed(title=card_name.upper() + " Search",url=url , color=discordColor)

    #pulls up all page results
    for cardDetails in content.find_all('article', attrs={"class": "card"}):
      
      #gets the card name for only the cards with card name
      #fixes issue of cardname, not appearing under card_name
      cardHeading = re.sub('[^A-Za-z0-9 ]+', '', cardDetails.h4.text)
      theCard = re.sub('[^A-Za-z0-9 ]+', '', card_name)
      print(cardHeading)
      #use casefold() to match regardless of case
      if theCard.casefold() in cardHeading.casefold():           
        #puts creates obj
        class cardObj:
          def __init__(card, name, theSet, price, currency, hyperLink):
            card.name = name
            card.theSet = theSet
            card.price = price
            card.currency = currency
            card.link = hyperLink

	#puts variables into obj
        theCard = cardObj(
                    cardDetails.h4.a.text.upper(),
                    cardDetails.find('p', attrs={"class": "card-set"}).text,
                    cardDetails.find('span', attrs={"class": "price--withoutTax"}).text,
                    cardDetails.find('span', attrs={"class": "currencyCode"}).text,
		    cardDetails.h4.a['href']
                   
          )
        #puts object in an array
        cardArray.append(cardObj)
        #puts obj into embededVar
        theCardText = '[' + theCard.theSet + ']' + '(' + theCard.link +')'
        embededVar.add_field(name=theCard.name, value=theCardText + "\n" + theCard.price +" | " + theCard.currency, inline=True)

        
    #if search returns no data then array will be empty
    if cardArray == []:
      return cardNotFound("Card Not Found", "CARD SEARCH INCONCLUSIVE")
    else:
      return embededVar

#retunrs an error message into discord
def cardNotFound(errortitle, errorReason):
  
   #defaults to error message
  embededError = discord.Embed(title=errortitle, color=discordColor)
  embededError.add_field(name=errorReason, value="Please Try Again", inline=False)
  return embededError



def joinSplit(myString):
  #removes excess white space 
  cleanString = " ".join(myString.split())
  return cleanString
  
keep_alive()
client.run(os.getenv('TOKEN')) #RUNS BOT using token in .env
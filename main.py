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
  textLength = len(text)
  #get all words between $$ while there are two $$ that are not equal
  if text.find('$$') != -1 and text.rfind('$$') != -1 and text.find('$$') !=text.rfind('$$') and text.find('$$',1,textLength-2) !=text.rfind('$$'):
    #print(text.find('$$'));
    #print(text.rfind('$$'));
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
        print(x + " IS NOT A STRING")
        return 
      
     
      elif "help" in x.casefold():
      #Gets How to use
        
        embedHelp=discord.Embed(title="HELP", description="This is my personal scraper, which will get you card prices from Face to Face Games.", color=discordColor)
        embedHelp.add_field(name="To search a Card just place the card name between two \"$$\"", value="eg. $$Ankle Shanker$$", inline=False)
        embedHelp.add_field(name="It is also compatible with the Scryfall search Bot by embedding the Scryfall bracket within the \"$$\"", value="\u200b", inline=False) 
	#value is required, using empy space \u200b 
        #embedHelp.add_field(name="Test", value="test", inline=True)

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
    return cardNotFound(toCamel(card_name) + "Not Found", "url", False, "CARD SEARCH INCONCLUSIVE")
    #if cards have a name shorter than 3 letters AND there are more than 200 results
  elif len(card_name) <= 4 and howManyFound >= 200 :
      return cardNotFound("To Many Cards for " + toCamel(card_name) ,url, True, "PLEASE REFINE SEARCH")
      

  #else Do card retreval
  else:
    #list to verify items have been passed
    cardArray = []
    #Default embeded string
    embededVar = discord.Embed(title=toCamel(card_name) + "Search",url=url , color=discordColor)
    
    #pulls up all page results
    for cardDetails in content.find_all('article', attrs={"class": "card"}):
      
      #gets the card name for only the cards with card name
      #replaces symbols with Empty so card's name or card-s name gets cards name
      cardHeadingReplaceEmpty = re.sub('[^A-Za-z0-9 ]+', '', cardDetails.h4.text)
      #replaces symbols with Empty so card's name or card-s name gets card s name
      cardHeadingReplaceSpace = re.sub('[^A-Za-z0-9 ]+', ' ', cardDetails.h4.text)

      theCard = re.sub('[^A-Za-z0-9]+', ' ', card_name)
      
      print(cardHeadingReplaceEmpty +"\n" + cardHeadingReplaceSpace);
      #use casefold() to match regardless of case
      
      #first 2 check if CARD's NA-ME is equal to cards name or card s na memoryview 
      if set(theCard.casefold().split()) <= set(cardHeadingReplaceEmpty.casefold().split()) or      set(theCard.casefold().split()) <= set(cardHeadingReplaceSpace.casefold().split()):
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
      return cardNotFound("Card Not Found",url, True,  "CARD SEARCH INCONCLUSIVE")
    else:
      return embededVar

#retunrs an error message into discord
def cardNotFound(errortitle,errorLink,isLinkOn, errorReason):

  if isLinkOn == True:
   	#Error Message with Link
  	embededError = discord.Embed(title=errortitle,url=errorLink, color=discordColor)
  	embededError.add_field(name=errorReason, value="Please Try Again", inline=False)
  	return embededError
  else:
	#Error Message without link
  	embededError = discord.Embed(title=errortitle, color=discordColor)
  	embededError.add_field(name=errorReason, value="Please Try Again", inline=False)
  	return embededError

def toCamel(text):
	#converts to only letters and spaces
	text =  re.sub('[^A-Za-z0-9 ,-]+', ' ', text)
	#removes extra white speace and convert word to lower case
	text = joinSplit(text.lower())
	#will break apart each word into list
	words = text.split()
	 
	fullWord = ""
	for x in words:
		#for each list it will remove letter at index 1 and replace it wiht a capital
		#join word and re join full string
		fullWord += x.title() + " "
	return fullWord
	


def joinSplit(myString):
	#removes excess white space 
	cleanString = " ".join(myString.split())
	return cleanString
  
keep_alive()
client.run(os.getenv('TOKEN')) #RUNS BOT using token in .env
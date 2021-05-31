#This holds most of the functions for the searching of the cards
import debug_log as printLog
import validate
import discord
#Imports for Web Parsing
import urllib.parse #for converting to url encoded
from bs4 import BeautifulSoup #for web Scraping
import requests #for web Scraping


#Get the Search objects
def get_card_names(message, list_of_games, help_me):
	print('Beginning get_card_names for\n' + message.center(80))
	

	#search list for later
	search_list = []
	#object to put information in
	class CardInformation:
		def __init__(self, card_name, card_set, card_game):
			self.name = card_name
			self.set = card_set
			self.the_game = card_game
	
	#removes Help messages
	if (message.casefold()).find(help_me.casefold()) != -1:
			printLog.debug("The Message before Help is: \n\"" + message.center(70) + "\"")
			#add Search onto the list
			Help = CardInformation(
					'Help',
					'Help',
					'Help'
			)
			#adds Help to list
			search_list.append(Help)
			printLog.debug(help_me + ' Removed')
			#replaces help
			start = (message.casefold()).find(help_me.casefold())
			end = start + 6
			message = message[:start] + message[end:]
			

	printLog.debug("The Message is: \n\"" + message + "\"")
	#for each bracket type in list_of_games
	for games in list_of_games:
		#resets text with each interval
		text = message
		#brackets
		b1 = games.first
		b2 = games.last
		printLog.debug((('\tBegin searching for {} and {}').format(b1,b2)).center(80))

		counter = 0
		while validate.is_not_empty_or_space(text) == True and validate.are_symbols_mentioned(b1,b2,text) == True and validate.storm_counter(counter) == True:
			printLog.debug('Initial text is '+ text)
			#Gets the Card name between symbols
			begin = text.find(b1) + 2
			end  = text.find(b2)
			name_of_card = text[begin:end]

			#get the set from card_name
			if name_of_card.find('|') != -1:
				#splits once at first |
				card_details = name_of_card.split('|')
				print(card_details)
				card_name = card_details[0]
				card_set = card_details[1]
				printLog.debug(('[The Card Set is {}]').format(card_set))

			else: 
				printLog.debug(('[The Card Set is Empty').center(80))
				card_name = name_of_card
				card_set = ""

			printLog.debug(('The Card Name is {}').format(card_name))
			#sets up CardInfo object
			MyCard = CardInformation(
				card_name,
				card_set,
				games.game
			)
			#adds card object to list
			search_list.append(MyCard)
			#removes card text from text
			text = text.replace(b1 + name_of_card + b2, '')
			print(("\tCard: {} \n\tSet:{} \n\tGame: {}").format(MyCard.name, MyCard.set, MyCard.the_game))
			printLog.debug('Text is now ' + text)
			#so no more than 100 cards can be set
			counter += 1
		printLog.debug((('\tDone searching for {} and {}').format(b1,b2)).center(80))

	print('Finished get_card_names')
	printLog.dash(40)
	print('\n')
	return search_list
				
def get_card_embed(card_details, game_list, error_color, url_token):
	printLog.debug(("Searching for {} | {} | {}").format(card_details.name, card_details.set, card_details.the_game))
	#If it triggers Help
	
	if card_details.name == "Help" and card_details.set == "Help" and card_details.the_game == "Help":
		#returns Help embed
		return Help()
		print(("Got Help Command").center(80))
	else:
		the_card_name = remove_whitespace(card_details.name)
		the_card_set = remove_whitespace(card_details.set)
		printLog.debug(("The Card Name is:{} and the Set is: {}").format(the_card_name, the_card_set))
		#If card doesnt have a set set set_search to false
		if card_details.set == "" or (card_details.set).isspace() == True:
			printLog.debug("Expansion search [OFF]")
			expansion_search = False
			name_to_url = the_card_name
		else:
			printLog.debug("Expansion search [ON]")
			expansion_search = True
			name_to_url = the_card_name + " " + the_card_set
		#removes all left over brackets or slashes in card name
		printLog.debug(remove_char('[ ] ( ) < > $', '', name_to_url))

		#gets second half URL and gets color
		for game in game_list:
			if card_details.the_game == game.game:
				#sets embedColor based on game
				embedColor = game.color
				if expansion_search == True:
					url_part_2 = game.surl
				else:
					url_part_2 = game.gurl
		if expansion_search == True:
			printLog.title("Loading Html For " + name_to_url + " in Singles")
		else:
			printLog.title("Loading Html For " + name_to_url + " in General")
		#parses card to url
		parsedUrl = urllib.parse.quote(name_to_url)

		#makes url
		my_url = url_token + parsedUrl + url_part_2
		printLog.debug("The Url Is \n" + my_url)
		#Try and Connect to Website or return error message
		try:
			response = requests.get(my_url, timeout=5) 
			print((("The Status Code is: [{}]").format(str(response.status_code)).center(80)))

			print(response.reason)
		except:
			#return error could not connect
			return error_message("404" ,my_url,"Could Not Connect to Face to Face", "Please Try Again", -1)
			printLog.debug("Could Not Connect")
		#Puts HTML content into html_content
		html_content = BeautifulSoup(response.content, "html.parser")

		#Checks the header to see how many are found
		find_header = html_content.find('h1',attrs={'class': 'page-heading'}).text
		is_card_found = remove_whitespace(find_header)
		print(is_card_found)
		printLog.dash(len(is_card_found))

		#Gets number from String
		how_many_found = [int(i) for i in is_card_found.split() if i.isdigit()]
		printLog.debug(str(how_many_found))
		#sets first number to int
		num_found= how_many_found[0]

		#if found None
		if num_found == 0:
			#return Error Card Not Found
			return error_message(("No Cards Found for {}").format(the_card_name.title()),my_url,"Please Refine Search", "Please Try Again", error_color)
			printLog.debug("Card Not Found")
		#if cards name was short and there is more than 200 requests 
		elif len(the_card_name) <= 4 and num_found>= 200:
			#return Error Card TO Many Cards Found
			return error_message(("To Many Cards Found for {}").format(the_card_name.title()),my_url,"Please Refine Search", "Please Try Again", error_color)
			printLog.debug("Card Not Found")
		#pull cards
		else:
			#list to Verify that items have been print
			card_result_list = []
			#removes all unwanted glyphs
			card_title = remove_char("[ ] ( ) < > $ ! @ # % ^ * + = / \ : ; ? ` ~", '', the_card_name)

			#default Embed String to return 
			embeded_card_title = ("{} Search").format((card_title).title())
			card_embed = discord.Embed(title=embeded_card_title,url=my_url , color=embedColor)

			#pulls up page_results for each card
			for page_details in  html_content.find_all('article', attrs={"class": "card"}):
				#Sets card name to have no special Glyphs
				search_name = remove_char("[ ] ( ) < > $ ! @ # % ^ * + = / \ : ; ? ` ~  \" ", '', the_card_name)
				search_name = remove_char("- , \'", " ", search_name)
				printLog.debug("Searching for " + search_name)
				#sets Two header types for compile
				header = page_details.h4.text
				header_with_spaces = remove_char("[ ] , - ( ) < > $ ! @ # % ^ * + = / \ : ; ? ` ~ \' \" ", ' ', header) #ca-rdna'me --> cardname
				header_without_spaces = remove_char("[ ] , - ( ) < > $ ! @ # % ^ * + = / \ : ; ? ` ~ \' \" ", '', header) #ca-rdna'me --> ca rdna me
				
				#puts all three cariables in a casefold split set to compare
				set_search_name = set(search_name.casefold().split())
				set_header_with_spaces = set(header_with_spaces.casefold().split())
				set_header_without_spaces = set(header_without_spaces.casefold().split())

				#discord embed Card Object
				class card_anatomy:
					def __init__(card, name, theSet, price, currency, hyperLink):
						card.name = name
						card.theSet = theSet
						card.price = price
						card.currency = currency
						card.link = hyperLink
				if expansion_search == False:
					printLog.debug("[Expansion Search is FALSE]")
				#Find all card names on page that match either header
					if set_search_name <= set_header_with_spaces or set_search_name <= set_header_without_spaces:
						
						#out puts an object
						playing_card = card_anatomy(
							page_details.h4.a.text.upper(),
							page_details.find('p', attrs={"class": "card-set"}).text,
							page_details.find('span', attrs={"class": "price--withoutTax"}).text,
							page_details.find('span', attrs={"class": "currencyCode"}).text,
							page_details.h4.a['href']
						)
						#puts object into list to vereify
						card_result_list.append(playing_card)
						#makes hyperlink text for card_embed
						hyperlink_text = '[' + playing_card.theSet + ']' + '(' + playing_card.link +')'
						#puts playing card into card_embed
						card_embed.add_field(name=playing_card.name, value=hyperlink_text + "\n" + playing_card.price +" | " + playing_card.currency, inline=True)
					#If it has a set
				elif expansion_search == True:
					printLog.debug("[Expansion Search is TRUE]")
					if set_search_name <= set_header_with_spaces or set_search_name <= set_header_without_spaces:
						
						#will only pull the card out where the sets match
						expansion_name = remove_char("[ ] , - ( ) < > $ ! @ # % ^ * + = / \ : ; ? ` ~ \' \" ", '', the_card_set)

						expansion = page_details.find('p', attrs={"class": "card-set"}).text
						#gets expansion name and converts like the headers
						expansion_without_spaces = remove_char("[ ] , - ( ) < > $ ! @ # % ^ * + = / \ : ; ? ` ~ \' \" ", '', expansion) #ca-rdna'me --> cardname
						expansion_with_spaces = remove_char("[ ] , - ( ) < > $ ! @ # % ^ * + = / \ : ; ? ` ~ \' \" ", ' ', expansion) #ca-rdna'me --> cardname

						#puts all 3 into sets

						set_expansion_name = set(expansion_name.casefold().split())
						set_expansion_with_spaces = set(expansion_with_spaces.casefold().split())
						set_expansion_without_spaces = set(expansion_without_spaces.casefold().split())
						if set_expansion_name <= set_expansion_with_spaces or set_expansion_name <= set_expansion_without_spaces:
							#out puts an object
							playing_card = card_anatomy(
								page_details.h4.a.text.upper(),
								page_details.find('p', attrs={"class": "card-set"}).text,
								page_details.find('span', attrs={"class": "price--withoutTax"}).text,
								page_details.find('span', attrs={"class": "currencyCode"}).text,
								page_details.h4.a['href']
							)
							#puts object into list to vereify
							card_result_list.append(playing_card)
							#makes hyperlink text for card_embed
							hyperlink_text = '[' + playing_card.theSet + ']' + '(' + playing_card.link +')'
							#puts playing card into card_embed
							card_embed.add_field(name=playing_card.name, value=hyperlink_text + "\n" + playing_card.price +" | " + playing_card.currency, inline=True)
					

			#if array is empty - card not found url "cardsearch inconclusov"
			if card_result_list == []:
				# returns card search inconclusive
				return error_message("Card Not Found",my_url,"Card Search Inconclusive", "Please Try Again", error_color)
				printLog.debug("Card Result List is Empty")
			#else return embed
			else:
				print("Sending Embed")
				return card_embed


#Error Message returns an embed 
def error_message(error_header, url_link,error_title,error_text,error_colour):
	#if Error_color is not an int
	if error_colour == -1:
		error_colour = 0xd3202a

	#if Error Has no Link or Link is " "
	if url_link.isspace() == True or url_link == "":
		error=discord.Embed(title=error_header, color=error_colour)
		error.add_field(name=error_title, value=error_text, inline=False)
	else:
		error=discord.Embed(title=error_header, url=url_link, color=error_colour)
		error.add_field(name=error_title, value=error_text, inline=False)
	return error
def Help():
	Help=discord.Embed(title="Help", description="This is my personal scraper, which will get you card prices from Face to Face Games.")
	Help.add_field(name="To search for a Card just surround the card name with dollar signs and the appropriate brackets.", value="\u2022\t$[Magic the Gathering]$\n\u2022\t$(Pokemon)$\n\u2022\t$<Yu-Gi-Oh>$", inline=False)
	Help.add_field(name="The general search will look up a product of that brand. If you include a \"|\" in the search it will look up only cards from that set", value="eg. $[ Card Name | Set ]$", inline=True)
	Help.set_footer(text="This Bot is also compatible with the Scryfall Search Bot and will work with it as long as the set isn't abbreviated and the dollar signs are surrounding the Scryfall command")

	return Help
#clears Whitespace
def remove_whitespace(text):
	#split breaks up the word and removes outside whitespace
	#join rejoins the word with " " between them
	clean_string = " ".join(text.split())
	return clean_string

#removes characters and replaces them with desired so i dont have to regex, because it slows down load time on current server
def remove_char(characters_I_want_removed, replace_them_with, text):
	#puts a character in a list
	remove_list = characters_I_want_removed.split()
	for i in remove_list:
		text = text.replace(i,replace_them_with)
	return text


#This is the Dorc For a discord Bot that allows user to pull prices for cards from www.facetofacegames.com
#This Bot is for personal use and I have no affiliation to FaceToFaceGames
#Program By Brandon Cuthbertson

#IMPORTS#
import discord
import os #for secret tokens
from keep_alive import keep_alive
#Project Imports
import debug_log as printLog
import validate 
import card_search as cs

#Other

#from keep_alive import keep_alive
#Global


#Connection to Client
client = discord.Client()

#Quick Reference
##Colors
ftfColor = 0xc64d23 #orange

PokeColor = 0xffcb05 #yellow
YugiColor = 0x78412a #Brown
DigiColor = 0x31a1da #blue

colorW = 0xf9faf4
colorU = 0x0e68ab
colorB = 0xa69f9d
colorR = 0xd3202a
colorG = 0x009b3e

colorP = 0x784e78 #purple

##Search Variables
class CardSearchParameters:
	def __init__(self, first_bracket, last_bracket, card_game,general_url, single_url, color):
		self.first = first_bracket
		self.last = last_bracket
		self.game = card_game
		self.gurl = general_url
		self.surl = single_url
		self.color = color
#gurl is for all product look up surl is for single cards that have sets
MTG = CardSearchParameters("$[","]$","Magic",os.getenv('gurlMTG'),os.getenv('surlMTG'), colorP)
YGO = CardSearchParameters("$<",">$","YuGiOh",os.getenv('gurlYGO'),os.getenv('surlYGO'), YugiColor)
PKMN = CardSearchParameters("$(",")$","Pokemon",os.getenv('gurlPKMN'),os.getenv('surlPKMN'), PokeColor)

game_list = [MTG,YGO, PKMN]

#keyword for Help feature
help_me = '$Help$'

#On Ready
@client.event
async def on_ready():
	printLog.title(('Jacking into Discord {0.user}'.format(client)).center(80)) 
	printLog.debug(('[Debug Mode is ON]').center(80))
	

#On Message
@client.event
async def on_message(message):

	#checks to see if this is the bot
	if validate.is_this_the_bot(message.author, client.user) == True:
		return
	else:
		discord_message = message.content
		#only searches if help_me or has proper brackets
		if (discord_message.casefold()).find(help_me.casefold()) != -1 or validate.does_it_have_triggers(game_list, discord_message) == True:
			
			#puts the card names into a list
			what_to_search = cs.get_card_names(discord_message,game_list,help_me)
			
			for card_obj in what_to_search:
				#get Card info and outputs embed
				UrlToken = os.getenv('Url')
				card_embed = cs.get_card_embed(card_obj,game_list,ftfColor, UrlToken)
				await message.channel.send(embed=card_embed)

			
			printLog.title(("End of Search").center(80))
	
		
#On Edit
#discord.on_message_edit(before, after)

#On React to Message

#Keeps the Bot Running as long as replit Doesnt Crash
keep_alive()
#Runs the Bot With the Token Hidden in .env
client.run(os.getenv('TOKEN'))
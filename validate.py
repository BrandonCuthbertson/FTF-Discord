#This File is used for storing functions related to validation
import debug_log as printLog


#This makes sure the bot isnt replying to itself
def is_this_the_bot(author, user):
	if author == user:
		return True
	else: 
		return False

#Are the Keywords Mentioned
def are_symbols_mentioned(begining_keyword,ending_keyword, message):
	begin = begining_keyword
	end = ending_keyword
	#Keywords are true and not the same
	if message.find(begin) != -1 and message.find(end,message.find(begin)) != -1:
		printLog.debug((message + " is True").rjust(80))

		#if its the same symbol and there is only one it returns False
		if begin == end and message.count(begin) <= 1:
			return False

		return True
	else:
		printLog.debug((message + " is False").rjust(80))
		return False

#verifies insert isnt empty
def is_not_empty_or_space(my_string):
	
	if my_string != '' and my_string.isspace() != True:
		printLog.debug((my_string + " is not Empty").rjust(80))
		return True
	else: 
		printLog.debug(("The String is Empty").rjust(80))
		return False

#Loop Counter to Stop Infinite loops
def storm_counter(my_int):
	counter = my_int
	if counter < 10:
		printLog.debug(('Storm Counter is at ' + str(my_int)).rjust(80))
		return True
	else: 
		print(('Storm Counter Has Reached Maximum').center(80))
		printLog.dash(80)
		return False
#takes in an object and verifies that the first brackets are in the message
def does_it_have_triggers(game_object, message):
	#counter to see if any of the bracket sets comes up at least once
	counter = 0
	for obj in game_object:
		if are_symbols_mentioned(obj.first, obj.last,message) == True:
			counter += 1
		else: 
			pass
	if counter > 0:
		return True
	else: return False


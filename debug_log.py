#This File is used to improve the readability of the console log during debugging and operation.

#Switch To turn On and Off secret Logs
turnLogOn = False

#Simple Print function for Console that creates as many dashes as I as the words
def title(title):
	initial = 0
	dash = ""
	
	while initial < len(title):
		dash += '='
		initial += 1
	print(dash)
	print(title)
	print(dash  + '\n')
	
#On most Console prints if off does nothing
def debug(word):
	
	if turnLogOn == True:
		print(word)
	else:
		pass
	
#creates a dash line
def dash(num):
	a=1
	dash = "="
	while a < num:
		dash += '='
		a += 1
	print(dash)

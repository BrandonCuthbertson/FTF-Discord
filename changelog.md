# FTF Bot 2.0
 Changes with 2.0 *[May 30, 2021]*
### Added
 - Added validate.py to store validation for ease of use and access
 - Added debug_log.py to improve console readability
	- Added a turnLogOn toggle allowing the debug function to only out put when turnLogOn == True 
 - Added card_search.py to reduce clutter on main.py
 - Added gurl(General Uniform Resource Locator) for General Product look up in .env for each game type
 - Added surl(Singleton Uniform Resource Locator) for single card set look up in .env for each game type

## Changes
 - Most of the code on main.py has been reworked into card_search.py for easier understanding and to make it easier to improve upon at a later date
 - Card Search no longer searches only card, you can now search products in that category
 - Brackets have been changed so $$Card Name$$ no longer works
	- $Help$ replaces $$Help$$
		- The Help embed has been improved
	- $[Card Name]$ is now set for Magic The Gathering
	- $(Card Name)$ is now set for Pokémon
	- $<Card Name>$ is now set for Yu-Gi-Oh
 - Added The functionality to look up cards in sets with '|'
	- Searching with '|' will only look up card singles and not products like boosters
 - Improved Error Embed for easier use in coding
 - The message embed now has different colors depending on its response
	- Black for Help
	- Red for "Cannot Connect to Website"
	- Orange for Negative Search Results on Site
	- Purple is for Magic the Gathering (in Reference the the proposed 6th Mana Symbol)
	- Yellow is for Pokemon
	- Brow is for Yu-Gi-Oh
	- A list of other colors has also been added but not implemented
		- One for each of the mana colors in Magic sans red which is in use for connection errors
 - The Card results now taste like candy

### Removed
 - Removed Regex Module for increased reload time
 - Removed $$ trigger for card search in favor of brackets
### Known Errors
 - The Bot still works with Scryfall But will produce an error as Scryfall uses abbreviations and Face to Face does not for sets


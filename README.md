# Pokemon Showdown Replay Scraping and Analysis for Pokemon Draft Leagues
This repository contains files which, together, allow you to scrape replay.pokemonshowdown.com links from a Discord server and analyze them.

scraper_bot.py is to be run in tandem with a .env file containing your relevant bot's secret token. After creating a discord bot profile through the developer portal, associating this code with it creates a slash command that allows the user to scrape discord channel(s) for showdown replay links. It gathers them, converts them to .json files, and downloads them locally.
Users can specify which dates they want the bot to scrape between, to allow users to scrape replays only from a specified draft season. Users can also specify one or multiple channels, to allow replay scraping of only some certain division(s).

parse_json.py is to be run after the bot successfully downloads those replays as .json files. It parses the file for various information about the battles, showing statistics such as each player in a league's most commonly used moves, or which players were most active in in-game chats. Different print statements can be (un-)commented depending on if you want easily readable output to console, or output easily portable to spreadsheets.

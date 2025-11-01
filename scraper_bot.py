import re
import discord
from discord import option
import os # default module
from dotenv import load_dotenv #env values
import datetime
import urllib.request

load_dotenv() # load all the variables from the env file
bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

#scrapes all replay files from the specified channel(s)
@bot.slash_command(name="scrape", description="Scrape for links after a given date")
@option("year", description="Scrape messages sent starting from this year", required=True, min_value=2000, max_value=datetime.datetime.now().year)
@option("month", description="Scrape messages sent starting from this month", required=True, min_value=1, max_value=12)
@option("day", description="Scrape messages sent starting from this day", required=True, min_value=1, max_value=31)
@option("channel ID", description="ID of the channel you want to scrape for replays", required=True)
@option("second channel", required=False, default=None)
@option("third channel", required=False, default=None)
@option("fourth channel", required=False, default=None)
@option("fifth channel", required=False, default=None)
async def scrape(ctx: discord.ApplicationContext,
                 year: int,
                 month: int,
                 day: int,
                 channel_id: str,
                 second_channel: str = None,
                 third_channel: str = None,
                 fourth_channel: str = None):
    # scrape links from the given start date until today; could prompt for end date as well, to avoid postseason
    season_start = datetime.datetime(year, month, day)
    channel_ids = [channel_id, second_channel, third_channel, fourth_channel]
    channels = []
    # have to take IDs as strings and convert to ints after because of length
    # then, convert those strings into channels usable by the bot
    for channel_id in channel_ids:
        if channel_id:
            channels.append(bot.get_channel(int(channel_id)))
    i = 1
    # iterate through each channel, checking messages from the given date for replay links
    # turn them into .json files and download them
    for channel in channels:
        async for msg in channel.history(after=season_start):
            if 'https://replay.pokemonshowdown' in msg.content:
                links = re.findall(r'(https?://\S+)', msg.content)
                for link in links:
                    file_path = 'replay_' + str(i) + '.json'
                    i = i + 1
                    link = link + ".json"
                    urllib.request.urlretrieve(link, file_path)
    await ctx.respond("Links scraped", ephemeral=True)

bot.run(os.getenv('TOKEN')) # run the bot with the token
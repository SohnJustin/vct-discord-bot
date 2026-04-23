import discord
from discord.ext import commands
import os
import logging
from dotenv import load_dotenv
from datetime import datetime
import data_fetcher

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Bot setup
TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    raise ValueError("DISCORD_TOKEN not found in .env file")

intents = discord.Intents.default()
intents.message_content = True  # Enable if needed for message commands

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user}')
    print(f'Bot is ready! Logged in as {bot.user}')


@bot.command()
async def ping(ctx):
    """Test command to check if bot is responsive"""
    await ctx.send('Pong!')


@bot.command()
async def ongoing(ctx):
    """List current live VCT games in North America"""
    try:
        data = await data_fetcher.get_ongoing_games()
        segments = data.get('data', {}).get('segments', [])
        if not segments:
            await ctx.send("No ongoing games in NA right now.")
            return

        embed = discord.Embed(
            title="Ongoing VCT Games (NA)",
            color=0x00ff00,
            timestamp=datetime.utcnow()
        )
        for match in segments[:5]:  # Limit to 5 matches
            team1 = match.get('team1', 'Unknown')
            team2 = match.get('team2', 'Unknown')
            score = f"{match.get('score1', '0')}-{match.get('score2', '0')}"
            event = match.get('match_event', 'Unknown Event')
            match_page = match.get('match_page', '')
            link = f"https://vlr.gg/{match_page}" if match_page else "No link available"
            embed.add_field(
                name=f"{team1} vs {team2}",
                value=f"Score: {score}\nEvent: {event}\n[Watch Match]({link})",
                inline=False
            )
        await ctx.send(embed=embed)
    except Exception as e:
        logging.error(f"Error in ongoing command: {e}")
        await ctx.send(f"Error fetching ongoing games: {e}")


@bot.command()
async def previous(ctx, year: int = datetime.now().year):
    """List previous VCT game results for the specified year (default: current year)"""
    try:
        data = await data_fetcher.get_previous_games(year)
        segments = data.get('data', {}).get('segments', [])
        if not segments:
            await ctx.send(f"No previous games found for {year} in NA.")
            return

        embed = discord.Embed(
            title=f"Previous VCT Games (NA, {year})",
            color=0xff0000,
            timestamp=datetime.utcnow()
        )
        for match in segments[:5]:  # Limit to 5 matches
            team1 = match.get('team1', 'Unknown')
            team2 = match.get('team2', 'Unknown')
            score = f"{match.get('score1', '0')}-{match.get('score2', '0')}"
            event = match.get('match_event', 'Unknown Event')
            match_page = match.get('match_page', '')
            link = f"https://vlr.gg/{match_page}" if match_page else "No link available"
            embed.add_field(
                name=f"{team1} vs {team2}",
                value=f"Final Score: {score}\nEvent: {event}\n[Match Details]({link})",
                inline=False
            )
        await ctx.send(embed=embed)
    except Exception as e:
        logging.error(f"Error in previous command: {e}")
        await ctx.send(f"Error fetching previous games: {e}")


@bot.command()
async def future(ctx):
    """List upcoming VCT matches in North America"""
    try:
        data = await data_fetcher.get_future_games()
        segments = data.get('data', {}).get('segments', [])
        if not segments:
            await ctx.send("No upcoming games in NA right now.")
            return

        embed = discord.Embed(
            title="Upcoming VCT Games (NA)",
            color=0x0000ff,
            timestamp=datetime.utcnow()
        )
        for match in segments[:5]:  # Limit to 5 matches
            team1 = match.get('team1', 'Unknown')
            team2 = match.get('team2', 'Unknown')
            event = match.get('match_event', 'Unknown Event')
            timestamp = match.get('unix_timestamp', '')
            match_page = match.get('match_page', '')
            link = f"https://vlr.gg/{match_page}" if match_page else "No link available"
            embed.add_field(
                name=f"{team1} vs {team2}",
                value=f"Event: {event}\nTime: {timestamp}\n[Match Page]({link})",
                inline=False
            )
        await ctx.send(embed=embed)
    except Exception as e:
        logging.error(f"Error in future command: {e}")
        await ctx.send(f"Error fetching future games: {e}")


@bot.command()
async def team(ctx, team_id: str):
    """Get information about a VCT team by ID"""
    try:
        data = await data_fetcher.get_team_info(team_id)
        team_data = data.get('data', {})
        if not team_data:
            await ctx.send(f"No team found with ID {team_id}.")
            return

        name = team_data.get('name', 'Unknown')
        tag = team_data.get('tag', '')
        region = team_data.get('region', 'Unknown')
        rank = team_data.get('rank', 'Unknown')
        roster = team_data.get('roster', [])

        embed = discord.Embed(
            title=f"{name} ({tag})",
            color=0xffff00,
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Region", value=region, inline=True)
        embed.add_field(name="Rank", value=rank, inline=True)
        if roster:
            players = ", ".join([p.get('name', 'Unknown') for p in roster[:5]])
            embed.add_field(name="Players", value=players, inline=False)
        await ctx.send(embed=embed)
    except Exception as e:
        logging.error(f"Error in team command: {e}")
        await ctx.send(f"Error fetching team info: {e}")


@bot.command()
async def players(ctx, team_id: str):
    """List players for a VCT team by team ID"""
    try:
        data = await data_fetcher.get_team_info(team_id)
        team_data = data.get('data', {})
        roster = team_data.get('roster', [])
        if not roster:
            await ctx.send(f"No roster found for team ID {team_id}.")
            return

        team_name = team_data.get('name', 'Unknown Team')
        embed = discord.Embed(
            title=f"Players of {team_name}",
            color=0xffa500,
            timestamp=datetime.utcnow()
        )
        for player in roster:
            name = player.get('name', 'Unknown')
            role = player.get('role', 'Unknown')
            embed.add_field(name=name, value=f"Role: {role}", inline=True)
        await ctx.send(embed=embed)
    except Exception as e:
        logging.error(f"Error in players command: {e}")
        await ctx.send(f"Error fetching players: {e}")

# Add more commands here in future sprints

# Run the bot
if __name__ == '__main__':
    bot.run(TOKEN)

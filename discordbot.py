import discord
from discord.ext import commands, tasks
import os
import logging
from dotenv import load_dotenv
from datetime import datetime
import data_fetcher

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Global tracking for automated posts
posted_live_matches = set()
posted_completed_matches = set()
TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    raise ValueError("DISCORD_TOKEN not found in .env file")

intents = discord.Intents.default()
intents.message_content = True  # Enable if needed for message commands

bot = commands.Bot(command_prefix='!', intents=intents)


@tasks.loop(minutes=5)
async def post_live_games():
    """Automatically post live games to #live-games channel"""
    try:
        data = await data_fetcher.get_ongoing_games()
        segments = data.get('data', {}).get('segments', [])
        if not segments:
            return  # No live games

        for guild in bot.guilds:
            channel = discord.utils.get(guild.text_channels, name='live-games')
            if not channel:
                continue  # Channel not found

            for match in segments:
                match_id = match.get('match_page', '')
                if not match_id or match_id in posted_live_matches:
                    continue

                embed = discord.Embed(
                    title="🔴 Live VCT Game (NA)",
                    color=0xff0000,
                    timestamp=datetime.utcnow()
                )
                team1 = match.get('team1', 'Unknown')
                team2 = match.get('team2', 'Unknown')
                score = f"{match.get('score1', '0')}-{match.get('score2', '0')}"
                event = match.get('match_event', 'Unknown Event')
                link = f"https://vlr.gg/{match_id}" if match_id else "No link"
                embed.add_field(
                    name=f"{team1} vs {team2}", value=f"Score: {score}\nEvent: {event}\n[Watch Live]({link})", inline=False)
                await channel.send(embed=embed)
                posted_live_matches.add(match_id)
                logging.info(f"Posted live match: {match_id}")
    except Exception as e:
        logging.error(f"Error in post_live_games: {e}")


@tasks.loop(minutes=10)
async def post_match_results():
    """Automatically post match results to #match-results channel"""
    try:
        data = await data_fetcher.get_previous_games()
        segments = data.get('data', {}).get('segments', [])
        if not segments:
            return

        for guild in bot.guilds:
            channel = discord.utils.get(
                guild.text_channels, name='match-results')
            if not channel:
                continue

            for match in segments[:3]:  # Post only recent ones
                match_id = match.get('match_page', '')
                if not match_id or match_id in posted_completed_matches:
                    continue

                embed = discord.Embed(
                    title="🏆 Match Result (NA)",
                    color=0x00ff00,
                    timestamp=datetime.utcnow()
                )
                team1 = match.get('team1', 'Unknown')
                team2 = match.get('team2', 'Unknown')
                score = f"{match.get('score1', '0')}-{match.get('score2', '0')}"
                event = match.get('match_event', 'Unknown Event')
                link = f"https://vlr.gg/{match_id}" if match_id else "No link"
                embed.add_field(
                    name=f"{team1} vs {team2}", value=f"Final Score: {score}\nEvent: {event}\n[Match Details]({link})", inline=False)
                await channel.send(embed=embed)
                posted_completed_matches.add(match_id)
                logging.info(f"Posted match result: {match_id}")
    except Exception as e:
        logging.error(f"Error in post_match_results: {e}")


@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user}')
    print(f'Bot is ready! Logged in as {bot.user}')
    # Start automated tasks
    post_live_games.start()
    post_match_results.start()


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


@bot.command()
@commands.has_permissions(manage_channels=True)
async def setup(ctx):
    """Set up the server environment for the VCT bot (requires Manage Channels permission)"""
    try:
        guild = ctx.guild
        existing_channels = [ch.name for ch in guild.text_channels]

        channels_to_create = ['live-games', 'match-results', 'team-info']
        created = []

        for ch_name in channels_to_create:
            if ch_name not in existing_channels:
                await guild.create_text_channel(ch_name)
                created.append(ch_name)
            else:
                created.append(f"{ch_name} (already exists)")

        embed = discord.Embed(
            title="VCT Bot Setup Complete",
            description="The bot has set up the necessary channels for VCT information.",
            color=0x00ff00,
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="Created Channels",
                        value="\n".join(created), inline=False)
        embed.add_field(
            name="Next Steps",
            value="Use commands like `!ongoing`, `!future`, etc., to get VCT data. The bot will also post updates to these channels automatically in future sprints.",
            inline=False
        )
        await ctx.send(embed=embed)
    except commands.MissingPermissions:
        await ctx.send("You need 'Manage Channels' permission to run this command.")
    except Exception as e:
        logging.error(f"Error in setup command: {e}")
        await ctx.send(f"Error during setup: {e}")

# Add more commands here in future sprints

# Run the bot
if __name__ == '__main__':
    bot.run(TOKEN)

# VCT Discord Bot

A Discord bot focused on Valorant Champions Tour (VCT) data, with emphasis on the North American league. Provides information on ongoing games, previous results, future matches, teams, and players using data from vlr.gg.

## Features

- **Ongoing Games**: Get details on live matches with scores and VOD links.
- **Previous Games**: View results from the current year.
- **Future Games**: See upcoming matches and teams.
- **Team Info**: Lookup team details and rosters.
- **Automated Posting**: Posts to dedicated channels for live games, match results, and team updates.

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- A Discord bot token (create one at https://discord.com/developers/applications)

### Installation

1. Clone or navigate to the project directory.
2. Clone the VLR API dependency:
   ```
   git clone https://github.com/axsddlr/vlrggapi.git vlr-api
   ```
3. Create a virtual environment:
   ```
   python3 -m venv venv
   ```
4. Activate the virtual environment:
   - On macOS/Linux: `source venv/bin/activate`
   - On Windows: `venv\Scripts\activate`
5. Install dependencies:
   ```
   pip install -r requirements.txt
   pip install -r vlr-api/requirements.txt
   ```
6. Create a `.env` file in the root directory and add your Discord bot token:
   ```
   DISCORD_TOKEN=your_bot_token_here
   ```
7. Invite the bot to your Discord server with the following permissions:
   - Send Messages
   - Read Message History
   - Manage Channels (required for !setup command)
   - Use Slash Commands (if using slash commands)
   - Manage Messages (optional, for cleanup)

### Running the Bot

1. Activate the virtual environment if not already.
2. Start the VLR API server (in a separate terminal):
   ```
   cd vlr-api && source ../venv/bin/activate && uvicorn main:app --host 127.0.0.1 --port 3001
   ```
3. Run the bot (in another terminal):
   ```
   python discordbot.py
   ```
4. The bot should log in and be ready.
5. Use commands in Discord (prefix: `!`): - `!setup`: Set up server channels for the bot (requires Manage Channels permission). - `!ongoing`: List current live VCT games in North America.
   - `!previous [year]`: List previous game results (default: current year).
   - `!future`: List upcoming VCT matches in North America.
   - `!team <team_id>`: Get information about a VCT team by ID.
   - `!players <team_id>`: List players for a VCT team by team ID.

### Development

- Add new commands in `discordbot.py`.
- For data fetching, create `data_fetcher.py` in future sprints.
- Test commands with `!ping` initially.

## Project Structure

- `discordbot.py`: Main bot file with commands and events.
- `data_fetcher.py`: (Future) Module for fetching VCT data from vlr.gg API.
- `.env`: Environment variables (not committed to git).
- `requirements.txt`: Python dependencies.
- `venv/`: Virtual environment (not committed).

## Contributing

- Follow the sprint plan for development.
- Commit changes regularly.

## License

This project is for educational purposes. Ensure compliance with vlr.gg terms of service.

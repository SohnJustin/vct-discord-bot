# VCT Discord Bot

A Discord bot focused on Valorant Champions Tour (VCT) data, with emphasis on the North American league. Provides information on ongoing games, previous results, future matches, teams, and players using data from vlr.gg.

## Features

- **Ongoing Games**: Get details on live matches with scores and VOD links.
- **Previous Games**: View results from the current year.
- **Future Games**: See upcoming matches and teams.
- **Team Info**: Lookup team details and rosters.
- **Automated Posting**: Posts live games to #live-games every 5 minutes, match results to #match-results every 10 minutes.

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
7. Invite the bot to your Discord server with the following permissions (or grant Administrator for simplicity):
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
4. The bot will automatically start posting updates to the channels created by !setup.
5. The bot should log in and be ready.
6. Use commands in Discord (prefix: `!`): - `!setup`: Set up server channels for the bot (requires Manage Channels permission). - `!ongoing`: List current live VCT games in North America.
   - `!previous [year]`: List previous game results (default: current year).
   - `!future`: List upcoming VCT matches in North America.
   - `!team <team_id>`: Get information about a VCT team by ID.
   - `!players <team_id>`: List players for a VCT team by team ID.
   - `!info`: Display help and usage information for the bot.

### Development

- Add new commands in `discordbot.py`.
- For data fetching, create `data_fetcher.py` in future sprints.
- Test commands with `!ping` initially.

## Deployment

To deploy the bot to a server for 24/7 operation:

1. **Choose a hosting platform**: Options include Railway, Heroku, DigitalOcean, or AWS. Railway is recommended for simplicity.
2. **Set environment variables**: In your hosting platform, set `DISCORD_TOKEN` to your bot token.
3. **Deploy the code**: Upload the repository (excluding `vlr-api/` and `venv/`) and install dependencies.
4. **Run the API**: In a separate process or container, run the VLR API server as described in the running instructions.
5. **Monitor**: Use logging and check for errors. The bot will restart automatically on most platforms.

Example Railway deployment:

- Connect your GitHub repo.
- Set build command: `pip install -r requirements.txt && pip install -r vlr-api/requirements.txt`
- Set start command: `uvicorn vlr-api.main:app --host 0.0.0.0 --port 3001 & python discordbot.py`

## Testing

Run unit tests with:

```
python -m pytest tests/
```

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

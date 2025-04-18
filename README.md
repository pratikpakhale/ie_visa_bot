# IE Visa Bot

A Python bot to track Irish visa application status and send notifications via Pushbullet.

## Features

- Automatically checks Irish visa application status
- Monitors specific application numbers
- Sends notifications through Pushbullet when updates are found
- Processes ODS/Excel files from the official Ireland visa website

## Setup

1. Install Python 3.8 or higher
2. Clone this repository
3. Install dependencies:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install .
   ```

4. Create a `.env` file with your Pushbullet access token:
   ```
   PUSHBULLET_ACCESS_TOKEN=your_token_here
   ```

5. Update `config.py` with your application numbers:
   ```python
   APPLICATIONS = {
       "application_number": "Name"
   }
   ```

## Usage

Run the script:
```bash
python main.py
```

The bot will:
1. Check the Ireland visa website for new decision files
2. Download and process any available ODS/Excel files
3. Search for your application numbers
4. Send a Pushbullet notification if your application is found

## Setup Cron Job

To automatically run the visa checking script periodically:

1. Open your crontab configuration:
```bash
crontab -e
```

2. Add one of these example schedules:

```bash
# Run every hour
0 * * * * cd /path/to/ie_via && python3 main.py

# Run every 30 minutes
*/30 * * * * cd /path/to/ie_via && python3 main.py

# Run every 15 minutes between 9 AM and 6 PM
*/15 9-18 * * * cd /path/to/ie_via && python3 main.py
```

3. Save and exit the editor. The cron service will automatically load your new schedule.

Note: Make sure to replace `/path/to/ie_via` with the actual path to your project directory.

Basic crontab format:
```
* * * * * command
│ │ │ │ │
│ │ │ │ └─ day of week (0-7, 0 and 7 are Sunday)
│ │ │ └─── month (1-12)
│ │ └───── day of month (1-31)
│ └─────── hour (0-23)
└───────── minute (0-59)
```

## Dependencies

- requests
- beautifulsoup4
- pandas
- pyexcel-ods
- openpyxl
- python-dotenv

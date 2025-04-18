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

## Dependencies

- requests
- beautifulsoup4
- pandas
- pyexcel-ods
- openpyxl
- python-dotenv

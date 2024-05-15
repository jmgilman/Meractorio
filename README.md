# Mercatorio Scraping

This repository contains code for syncing data from [Mercatorio] to an [AirTable].
The scraped data is reformated into a table-structure that is suitable for AirTable.

## Setup

### 1. Install Poetry and Docker
You'll need to ensure you have poetry installed first (pip install poetry).

You can install Docker in numerous ways depending on your OS.

### 2. Setup Airtable
You must provide an Airtable API key (aka a personal access token).
- Create a new workspace in [AirTable].
- Create a new Personal Access Token. 
- Give the personal access token all permissions to the new workspace.
- Create a new Base within the workspace called "Raw Data".

It's recommended you keep it in a local `.env` file, formatted like so:

### 3. Generate API Key for [Mercatorio]
- Generate API Credentials for Mercatorio [here](https://play.mercatorio.io/settings/api).

### 4. Setup .env file
Store both sets of credentials in a local `.env` file in the following format:

```text
AIRBASE_API_KEY="abc123"
MERC_API_USER="email@domain.com"
MERC_API_TOKEN="123abc"
```

### 5. Setup cache.db
- Create a file called "cache.db" in the working directory.
- Make sure the proper permissions are given for the working directory and cache.db.

### 6. Run the Migration
Run the migration script:

```shell
poetry run python migrate.py
```

This will configure the base with the required table structure.

## Usage
Run the script using:

```shell
docker compose up
```

## Testing

To start a Python session with an authenticated scraper:

```shell
$ poetry run ipython
>>> from shell import main
>>> await main()
>>> from shell import airtable, api, cache
>>> # Now you can use airtable, api, and cache
```

[AirTable]: https://airtable.com/
[Mercatorio]: https://mercatorio.io
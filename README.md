# Mercatorio Scraping

This repository contains code for syncing data from [Mercatorio] to an [AirTable].
The scraped data is reformated into a table-structure that is suitable for AirTable.

## Usage

You must first [generate API credentials](https://play.mercatorio.io/settings/api).
You must also [generate an Airtable PAT](https://support.airtable.com/docs/creating-personal-access-tokens).
Both credentials should be stored in a local `.env` file in the following format:

```text
AIRBASE_API_KEY="abc123"
MERC_API_USER="email@domain.com"
MERC_API_TOKEN="123abc"
```

Next, create a new Airtable base named `Raw Data`.
Run the migration script:

```shell
python migrate.py
```

This will configure the base with the required table structure.

Finally, run it with:

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
[IndexedDB Exporter]: https://chromewebstore.google.com/detail/indexeddb-exporter/kngligbmoipnmljnpphhocajldjplgcj
[Mercatorio]: https://mercatorio.io
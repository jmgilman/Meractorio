# Mercatorio Scraping

This repository contains code for syncing data from [Mercatorio] to an [AirTable].
The scraped data is reformated into a table-structure that is suitable for AirTable.

## Usage

You must have a local file containing cookies from an authenticated [Mercatorio] session.
By default, the scraper looks for a local `session.json` file (this can be changed with the `--session` flag).

Additionally, you must expose an AirTable API key via the `AIRTABLE_API_KEY` environment variable.

Run it with:

```shell
poetry run python main.py
```

## Testing

To start a Python session with an authenticated scraper:

```shell
poetry run python -i test.py
```

Then you can test endpoints with:

```python
>>> r = scraper.get("https://play.mercatorio.io/api/towns/181001062/marketdata")
>>> r.text
```

[AirTable]: https://airtable.com/
[Mercatorio]: https://mercatorio.io
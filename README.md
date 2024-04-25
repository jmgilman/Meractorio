# Mercatorio Scraping

> Automation for scraping data from the [Mercatorio] API.

## Usage

You must have a local file containing cookies from an authenticated [Mercatorio] session.
By default, the scraper looks for a local `cookies.json` file (this can be changed with the `--cookies` flag).

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
>>> r = scraper.session.get("https://play.mercatorio.io/api/towns/181001062/marketdata")
>>> r.text
```

[Mercatorio]: https://mercatorio.io
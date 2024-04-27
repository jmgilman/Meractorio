# Mercatorio Scraping

This repository contains code for syncing data from [Mercatorio] to an [AirTable].
The scraped data is reformated into a table-structure that is suitable for AirTable.

## Usage

You must provide an Airbase API key.
It's recommended you keep it in a local `.env` file, formatted like so:

```text
AIRBASE_API_KEY="patabc123"
```

Additionally, you must setup the initial `auth.json` file like so:

```json
{
    "id_token": "<ID_TOKEN>",
    "refresh_token": "<REFRESH_TOKEN>",
    "current_time": 00000000000.0000000,
    "expires_in": "3600"
}
```

Replacing the `ID_TOKEN` and `REFRESH_TOKEN` fields with the correct values.
These values can be obtained by using the [IndexedDB Exporter] on a page of the game where you are authenticated.
Select the `firebaseLocalStorageDb` database.
In the dumped data, you will find the `ID_TOKEN` field under the field called `accessToken`.
You will also find the `REFRESH_TOKEN` under the field called `refreshToken`.
This only needs to be done once as the script will keep the token refreshed after running it.

Run it with:

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
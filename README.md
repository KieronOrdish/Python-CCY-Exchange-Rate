
Scraping live currency exchange rate data from
https://uk.finance.yahoo.com/currencies/

## Getting started

You should make a python3.8 virtual env, and then install the dependencies in
requirements.txt

```bash
python3 -m venv env
. ./env/bin/activate
pip install -r requirements.txt
```

Inside `yahoo_scraper/__main__.py` you'll find a simple server that listens on
localhost 8080. Make sure you've activated the env and then start it with:

```bash
python -m yahoo_scraper
```

In another terminal you can connect to it as a client with `nc localhost 8080`
and send some requests, this is how we will test your solution.

```bash
$ nc localhost 8080
Connected!
EUR:USD
0.0
USD:EUR
0.0
```
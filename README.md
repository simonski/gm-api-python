# gm

Python GrayMeta API bindings.

This project is used to access your GrayMeta installation API using python.

## Installation

This is avaialble on pypy

    pip install gmapi

## Usage

`gmapi` can be used directly via the terminal with the `gm` command, or via the API.

## Usage (Terminal)

You must first make the `GRAYMETA_SERVER_URL` and your `GRAYMETA_API_KEY` available as environment variables, then you can call `gm`

```
export GRAYMETA_SERVER_URL=https://your-installation-of-graymeta
export GRAYMETA_API_KEY=your-api-keye
```

> See your Admin for details of these values

Next, you can just call `gm`:

```
gm	
```

## Usage (API)

Having installed gmapi via `pip`, you can then use it directly in your python, for example

(demo.py)

```
from gmapi import gmapi.GraymetaClient

SERVER_URL="https://your-server"
API_KEY="your-gm-api-key"
client = GraymetaClient(SERVER_URL, API_KEY)
client.search()
```

## API Documentation

TODO
	


	


    

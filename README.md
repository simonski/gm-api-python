# gm

Python GrayMeta API bindings.

This project is used to access your GrayMeta installation API using python.  For  `go`, please use [this](https://github.com/simonski/gm-api-go).

## Installation

This is avaialble on pypy

    pip install gmapi

## Usage

Can be used directly via the terminal with the `gm` command, or via the API in your own python.

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

This will print out the commands you can perform on your server.

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

Please refer to your Graymeta Platform Documentation for the API Docs.  I have tried to make the calls in `gmapi.py` as closely named as possible to the documentation.  Typing `gm` in the terminal will list all API calls that are currently implemented.

> **Note** Currently only a subset of calls are implemented around initiating harvest, searching the index, querying containers/locations and fetching item metadata.
	


	


    

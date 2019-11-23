# py-imdb-challenge

A programming challenge to retrieve the films that actors have appeared in from imdb

# Usage
To do

# What's the source of the data?

There is no official imdb API.  Some alternatives exist (a few on rapidapi.com, omdb, themoviedb), but these would require users to sign up and grab an API key which is a pain (and they also don't meet the spec of getting the data FROM imdb).  Instead this tool directly queries the imdb website and cleans up the returned HTML.  

This will break if the webpage changes.  

# For Developers

## Environment
Use a virtual environment when developing this project

`python3 -m venv venv`

`. ./venv/bin/activate`

## Updating Requirements

This project makes use of pip-tool's `pip-compile` tool for managing its requirements.  To update, please run

`pip-compile`

`pip install -rrequirements.txt`

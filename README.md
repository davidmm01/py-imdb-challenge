# py-imdb-challenge

A programming challenge to retrieve the films that actors have appeared in from imdb

# Usage

## Set up

First create a safe environment to run the program from:

`python3 -m venv venv`

`. ./venv/bin/activate`

`pip3 install -rrequiements.txt`

## Run it

`python3 actors_films.py <ACTOR NAME>`

Optional arguments:

`--descending` can be supplied to return the films from most to least recent

`--save-to-disk` will save the additionally save the output of the program in JSON to a file on disk

## Example 

`python3 actors_films.py "will ferrell" --descending --save-to-disk`


# Good example Candidates

`bruce willis` has many films and is the only actor by that name.

`will ferrell` has many films and there are 3 people by that name in imdb.

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

`pip3 install -rrequirements.txt`

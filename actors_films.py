import argparse
from bs4 import BeautifulSoup
import datetime
import json
import requests


class Actor:
    def __init__(self, name, slug, example_job=None, example_film=None):
        self.name = name
        self.slug = slug
        self.example_job = example_job
        self.example_film = example_film


class Movie:
    def __init__(self, title, year):
        self.title = title
        self.year = year


# CMD LINE ARGS
parser = argparse.ArgumentParser()
parser.add_argument(
    "actor", help="name of actor for which films will be displayed", type=str
)

parser.add_argument(
    "--descending", help="return the movie list from most to least recent", action="store_true"
)

parser.add_argument(
    "--save-to-disk", help="save the output to a JSON document on disk", action="store_true"
)

arguments = parser.parse_args()
actor_search_term = arguments.actor
save_to_disk = arguments.save_to_disk

order = 1 if arguments.descending else -1

# s=nm query param searches for celebs
response = requests.get(f"https://www.imdb.com/find?s=nm&q={actor_search_term}&ref_=nv_sr_sm")

bs = BeautifulSoup(response.text, features="html.parser")

# only grab result text, not the accompanying "primary_photo"
table_rows = bs.find_all('td', class_="result_text")

actors = []

for row in table_rows:

    # do a case-insensitive match
    if row.a.string.lower() == actor_search_term.lower():

        # all returned results have a name and slug
        name = row.a.string
        slug = row.a["href"]

        # some returned results will not have an example work of the actor
        if row.small:
            try:
                example_job = row.small.contents[0].strip("(").strip(", ")
                example_film = (row.small.contents[1].string)
            except KeyError:
                # this except might not be required, but keeping for defense
                example_job = None
                example_film = None
        else:
            example_job = None
            example_film = None

        actors.append(Actor(name, slug, example_job, example_film))


actor_matches = len(actors)


if actor_matches == 0:
    print(f"No actors found named {actor_search_term}")
    exit
elif actor_matches > 1:
    print(f"Found {actor_matches} actors with name {actor_search_term}")
    print("Please select one actor by entering the corresponding number:\n")

    count = 1
    for actor in actors:
        print(f"{count}) {actor.name}")
        if actor.example_job is not None and actor.example_film is not None:
            print(f"   Known as")
            print(f"   {actor.example_job} in {actor.example_film}")
        count += 1
        print("")
    while True:
        selection = input("Selection: ")
        try:
            selection = int(selection) - 1
            actor = actors[selection]
        except ValueError:
            print("Ensure your selection is a number")
        except IndexError:
            print(f"Ensure your selection is between 1 and {actor_matches}")
        else:
            break
else:
    actor = actors[0]

# TODO: decide if we actually need this #actor on the slug, prolly not
response = requests.get(f"https://www.imdb.com{actor.slug}#actor")

# the returned HTML from the page is not nicely broken into a parent-children
# structure for the lists of films under the actor/producer/... sections
# so we forceably cut out everything before and after the actor tag before
# putting it into beautiful soup
start_cut_index = response.text.find('<a name="actor">Actor</a>')
trimmed_response = response.text[start_cut_index:]
# skip the first 8 chars, since they already match
end_cut_index = trimmed_response[8:].find('<a name="')
trimmed_response = trimmed_response[0:end_cut_index]


bs = BeautifulSoup(trimmed_response, features="html.parser")

movies = []
for movie in bs.find_all(class_="filmo-row"):
    title = movie.a.string
    year = movie.span.string.strip()

    if len(year) == 0:
        year = "Upcoming"

    movies.append(Movie(title, year))


count = 1
for movie in movies[::order]:
    print(f"{count}) {movie.title}, {movie.year}")
    count += 1


if save_to_disk:
    contents = dict(
        actor=actor_search_term, 
        movies=[dict(title=movie.title, year=movie.year) for movie in movies[::order]]
        )
    # contents = json.dumps(contents, indent=4)
    with open(f"{actor_search_term}-{datetime.datetime.now()}.json", "x") as f:
        json.dump(contents, f, indent=4)

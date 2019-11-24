import argparse
import datetime
import json

from bs4 import BeautifulSoup

import imdb_calls
from classes import Actor, Movie


def get_arguments():
    """
        returns: actor_search_term, the actor being requested
                 descending flag, if True will reverse order of output
                 save-to-disk flag, if True will trigger method to save to disk
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "actor", help="name of actor for which films will be displayed", type=str
    )

    parser.add_argument(
        "--descending",
        help="return the movie list from most to least recent",
        action="store_true",
    )

    parser.add_argument(
        "--save-to-disk",
        help="save the output to a JSON document on disk",
        action="store_true",
    )

    arguments = parser.parse_args()
    actor_search_term = arguments.actor
    save_to_disk = arguments.save_to_disk
    order = 1 if arguments.descending else -1

    return actor_search_term, save_to_disk, order


def get_actor(actor_search_term):
    """
        input: actor_search_term, the term to match to an imdb actor
        returns: actor, an instance of Actor object
    """

    raw_html = imdb_calls.retrieve_celebs(actor_search_term)

    bs = BeautifulSoup(raw_html, features="html.parser")

    # only grab result text, not the accompanying "primary_photo"
    table_rows = bs.find_all("td", class_="result_text")

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
                    example_film = row.small.contents[1].string
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

    return actor


def get_movies(actor):
    """
        input: actor, an instance of Actor
        returns: movies, list of Movie objects
    """

    raw_html = imdb_calls.retrieve_movies(actor.slug)

    # the returned HTML from the page is not nicely broken into a parent-children
    # structure for the lists of films under the actor/producer/... sections
    # so we forceably cut out everything before and after the actor tag before
    # putting it into beautiful soup
    start_cut_index = raw_html.find('<a name="actor">Actor</a>')

    if start_cut_index == -1:
        start_cut_index = raw_html.find('<a name="actress">Actress</a>')

    trimmed_html = raw_html[start_cut_index:]
    # skip the first 12 chars, since they already match
    end_cut_index = trimmed_html[12:].find('<a name="')
    trimmed_html = trimmed_html[0:end_cut_index]

    bs = BeautifulSoup(trimmed_html, features="html.parser")

    movies = []
    for movie in bs.find_all(class_="filmo-row"):
        title = movie.a.string
        year = movie.span.string.strip()

        if len(year) == 0:
            year = "Upcoming"

        movies.append(Movie(title, year))
    return movies


def display_output(movies, order):
    """
        responsible for printing output to the user
        input: movies, a list of Movie objects
               order, 1 or -1, controls which way movies are represented
    """

    print("Movies:")
    count = 1
    for movie in movies[::order]:
        print(f"{count}) {movie.title}, {movie.year}")
        count += 1


def write_to_disk(actor, movies, order):
    """
        responsible for printing output to the user
        input: actor, an instance of Actor object
               movies, a list of Movie objects
               order, 1 or -1, controls which way movies are represented
    """

    contents = dict(
        actor=actor.name,
        movies=[dict(title=movie.title, year=movie.year) for movie in movies[::order]],
    )
    with open(f"{actor.name}-{datetime.datetime.now()}.json", "x") as f:
        json.dump(contents, f, indent=4)


def main():
    actor_search_term, save_to_disk, order = get_arguments()

    actor = get_actor(actor_search_term)
    movies = get_movies(actor)

    display_output(movies, order)

    if save_to_disk:
        write_to_disk(actor, movies, order)


if __name__ == "__main__":
    main()

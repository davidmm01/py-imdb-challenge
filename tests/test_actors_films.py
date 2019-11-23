import json
import os

import pytest
from freezegun import freeze_time

from actors_films import display_output, get_actor, get_movies, write_to_disk
from classes import Actor, Movie


@pytest.fixture
def mock_retrieve_celebs(monkeypatch):
    monkeypatch.setattr(
        "imdb_calls.retrieve_celebs",
        lambda x: open("tests/bruce_willis_actor_sample_html").read(),
    )


@pytest.fixture
def mock_retrieve_movies(monkeypatch):
    monkeypatch.setattr(
        "imdb_calls.retrieve_movies",
        lambda x: open("tests/bruce_willis_movie_sample_html").read(),
    )


def test_get_actor(mock_retrieve_celebs):
    expected_actor = Actor("Bruce Willis", "/name/nm0000246/", "Actor", "Die Hard")
    actual_actor = get_actor("bruce willis")

    assert actual_actor.name == expected_actor.name
    assert actual_actor.slug == expected_actor.slug
    assert actual_actor.example_film == expected_actor.example_film
    assert actual_actor.example_job == expected_actor.example_job


def test_get_movies(mock_retrieve_movies):
    actor = Actor("Bruce Willis", "/name/nm0000246/", "Actor", "Die Hard")
    expected_first = Movie("McClane", "Upcoming")
    expected_last = Movie("The First Deadly Sin", "1980")
    expected_num_movies = 125

    actual_movies = get_movies(actor)

    assert actual_movies[0].title == expected_first.title
    assert actual_movies[0].year == expected_first.year

    assert actual_movies[len(actual_movies) - 1].title == expected_last.title
    assert actual_movies[len(actual_movies) - 1].year == expected_last.year

    assert len(actual_movies) == expected_num_movies


def test_display_output(capsys):
    expected = "Movies:\n1) The Godfather, 1972\n2) The Shawshank Redemption, 1994\n"
    movies = [Movie("The Shawshank Redemption", "1994"), Movie("The Godfather", "1972")]
    display_output(movies, -1)
    captured = capsys.readouterr()
    assert captured.out == expected


def test_display_output_reversed_order(capsys):
    expected = "Movies:\n1) The Shawshank Redemption, 1994\n2) The Godfather, 1972\n"
    movies = [Movie("The Shawshank Redemption", "1994"), Movie("The Godfather", "1972")]
    display_output(movies, 1)
    captured = capsys.readouterr()
    assert captured.out == expected


@freeze_time("2001-01-01 01:01:01")
def test_write_to_disk():
    expected_json = {
        "actor": "Bruce Willis",
        "movies": [
            {"title": "The Godfather", "year": "1972"},
            {"title": "The Shawshank Redemption", "year": "1994"},
        ],
    }
    actor = Actor("Bruce Willis", "/name/nm0000246/", "Actor", "Die Hard")
    movies = [Movie("The Shawshank Redemption", "1994"), Movie("The Godfather", "1972")]
    write_to_disk(actor, movies, -1)
    with open("Bruce Willis-2001-01-01 01:01:01.json", "r") as f:
        actual_json = json.loads(f.read())
        assert actual_json == expected_json
    os.remove("Bruce Willis-2001-01-01 01:01:01.json")

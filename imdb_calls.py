import requests

BASE_URL = "https://www.imdb.com"


def retrieve_celebs(search_term):
    # s=nm is the query param searches for celebs
    return requests.get(
        f"{BASE_URL}/find?s=nm&q={search_term}&ref_=nv_sr_sm"
    ).text


def retrieve_movies(search_term):
    return requests.get(f"{BASE_URL}{search_term}#actor").text

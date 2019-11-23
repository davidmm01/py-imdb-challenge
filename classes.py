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

class Film(object):
    __slots__ = ['film_id', 'film_name', 'film_year', 'film_country', 'film_genre', 'film_link']
    def __init__(self, film_id, film_name, film_year, fim_country, film_genre, film_link):
        self.film_id = film_id
        self.film_name = film_name
        self.film_year = film_year
        self.film_country = fim_country
        self.film_genre = film_genre
        self.film_link = film_link

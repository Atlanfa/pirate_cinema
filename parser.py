import requests
from bs4 import BeautifulSoup
from models import Film

page_link = 'https://rezka.ag/page/1/'
genre_list = ('Арт-хаус', 'Биографические', 'Боевики', 'Боевые искусства', 'Вестерны', 'Военные', 'Детективы',
              'Детские', 'Для взрослых', 'Документальные', 'Драмы', 'Зарубежные', 'Исторические', 'Кодомо', 'Комедии',
              'Короткометражные', 'Криминал', 'Махо-сёдзё', 'Мелодрамы', 'Меха', 'Мистические', 'Музыкальные',
              'Мультсериалы', 'Мюзиклы', 'Наши', 'Охота и рыбалка', 'Повседневность', 'Приключения', 'Реалити-шоу',
              'Реальное ТВ', 'Романтические', 'Русские', 'Самурайский боевик', 'Семейные', 'Сказки', 'Советские',
              'Спортивные', 'Сёдзё-ай', 'Телепередачи', 'Триллеры', 'Ужасы', 'Фантастика', 'Фэнтези', 'Юмористические')


def get_films_name_from_page(link):
    main = requests.get(link)
    main_soup = BeautifulSoup(main.text, 'html.parser')
    b_content__inline_items = main_soup.find("div", {"class": "b-content__inline_items"})
    divs = b_content__inline_items.findAll("div", {"class": "b-content__inline_item-link"})
    films_list = []
    for div in divs:
        film_name = div.find('a')
        # print('______________')
        # (film_name['href'])
        # get_full_film_info(film_name['href'])
        film_id = film_name['href'].split('/')[-1].split('-')[0]
        # print(film_name.text)
        film_year_and_genre_div = div.find("div")
        film_year_and_genre = film_year_and_genre_div.text.split(',')
        try:
            year = film_year_and_genre[0].strip()
            country = film_year_and_genre[1].strip()
            genre = film_year_and_genre[2].strip()
            # print(year)
            # print(country)
            # print(genre)
            film = Film(film_id, film_name.text, year, country, genre, film_name['href'])
        except Exception as e:
            print(e)
            if film_year_and_genre[1].strip() in genre_list:
                genre = film_year_and_genre[1].strip()
                film = Film(film_id, film_name.text, year, country, genre, film_name['href'])
        films_list.append(film)
    return films_list


def get_full_film_info(link):
    film_page = requests.get(link)
    film_page_soup = BeautifulSoup(film_page.text, 'html.parser')
    film_name = film_page_soup.find('div', {"class": "b-post__title"})
    film_status = film_page_soup.find('div', {"class": "b-post__infolast"})
    film_data_table = film_page_soup.find('table', {"class": "b-post__info"})
    table_rows = film_data_table.findAll('tr')
    photo = film_page_soup.find('div', {"class": "b-sidecover"}).find('a')['href']
    # print(table_rows)
    film_info = ''
    rating = ''
    tagline = ""
    release_date = ''
    year = ''
    country = ''
    producer = ''
    genre_str = ''
    quality = ''
    translation = ''
    age = ''
    duration_str = ''
    series = ''
    cast = ''
    try:
        film_info += f"{film_name.text}\n"

        for row in table_rows:
            if row.find('h2'):
                row_name = row.find('h2')
            elif row.find('td', {"class": "l"}).text == "Год:":
                row_name = row.find('td', {"class": "l"})
            if row_name.text == "Рейтинги":
                a_s = row.findAll('a')
                ratings = row.findAll('span', {"class": "bold"})
                rating = ''
                rating += f"{row_name.text}: "
                for item in range(len(a_s)):
                    rating += f"{a_s[item].text} {ratings[item].text} "
            elif row_name.text == "Слоган":
                tds = row.findAll('td')
                tagline = f"{row_name.text}: {tds[1].text}"
            elif row_name.text == "Дата выхода":
                tds = row.findAll('td')
                release_date = f"{row_name.text} {tds[1].text}"
            elif row_name.text == "Страна":
                a_s = row.findAll('a')
                country = ''
                country += f"{row_name.text}: "
                for a in a_s:
                    country += f"{a.text} "
            elif row_name.text == "Режиссер":
                names = row.findAll('span', {"itemprop": "name"})
                producer = ''
                producer += f"{row_name.text}: "
                for name in names:
                    producer += f"{name.text} "
            elif row_name.text == "Жанр":
                genres = row.findAll('span', {"itemprop": "genre"})
                genre_str = ''
                genre_str += f"{row_name.text}: "
                for genre in genres:
                    genre_str += f"{genre.text} "
            elif row_name.text == "В качестве":
                tds = row.findAll('td')
                quality = f"{row_name.text}: {tds[1].text}"
            elif row_name.text == "В переводе":
                tds = row.findAll('td')
                translation = f"{row_name.text}: {tds[1].text}"
            elif row_name.text == "Возраст":
                tds = row.findAll('td')
                age = f"{row_name.text}: {tds[1].text}"
            elif row_name.text == "Время":
                duration = row.find('td', {"itemprop": "duration"})
                duration_str = f"{row_name.text}: {duration.text}"
            elif row_name.text == "Из серии":
                a_s = row.findAll('a')
                series = f"{row_name.text}: "
                for a in a_s:
                    series += f"{a.text} "
            elif row_name.text == "В ролях актеры":
                names = row.findAll('span', {"itemprop": "name"})
                cast = f"{row_name.text}: "
                for name in names:
                    cast += f"{name.text} "
                cast += "и другие"
            elif row_name.text == "Год:":
                a = row.find('a')
                year = f"{row_name.text}: {a.text}"
    except Exception:
        pass
    b_post__description_title = film_page_soup.find('div', {"class": "b-post__description_title"}).find('h2')
    b_post__description_text = film_page_soup.find('div', {"class": "b-post__description_text"})
    description = f"{b_post__description_title.text}:\n{b_post__description_text.text[:100]} и т.д."
    film_info += f"{rating}\n{year}\n{country}\n{genre_str}\n{age}\n{description}"
    # print(film_info)
    # print(photo)
    return film_info, photo


def get_max_page_number(link):
    main = requests.get(link)
    main_soup = BeautifulSoup(main.text, 'html.parser')
    b_navigation = main_soup.find('div', {"class": "b-navigation"})
    a_s = b_navigation.findAll('a')
    max_num = 0
    for a in a_s:
        try:
            if int(a.text) > max_num:
                max_num = int(a.text)
        except ValueError:
            print("this is not a number")
    return max_num

# get_films_name_from_page(page_link)
# get_full_film_info("https://rezka.ag/films/fiction/981-matrica-1999.html")

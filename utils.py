from parser import get_films_name_from_page, get_max_page_number
import json
from models import Film


def get_film_id(film_link):
    return film_link.split('/')[-1].split('-')[0]


def do_search(sought):
    films = get_films_name_from_page(f'https://rezka.ag/search/?do=search&subaction=search&q={sought}&page=1')
    try:
        max_number = get_max_page_number(f'https://rezka.ag/search/?do=search&subaction=search&q={sought}&page=1')
        if max_number <= 10:
            max_number += 1
        for page_num in range(2, max_number):
            films += get_films_name_from_page(
                f'https://rezka.ag/search/?do=search&subaction=search&q={sought}&page={page_num}')
    except Exception as e:
        print(e)
    return films


def chunks(lst):
    start = 0
    new_list = []
    for i in range(len(lst) // 6 + 1):
        stop = start + 6
        new_list.append(lst[start:stop])
        start = stop
    return new_list


def post_message(films, page):
    i = 1
    search_result = ""
    for film in films[page]:
        search_result += f"{i}){film.film_name}({film.film_year})\n{film.film_genre} | {film.film_country}\n\n"
        i += 1
    return search_result


def write_into_json(films, current_page, message, post_id):
    def get_list_films(list_films=films):
        films_list = []
        for film in list_films:
            films_list.append({"film_name": film.film_name, "film_year": film.film_year,
                               "film_country": film.film_country, "film_genre": film.film_genre,
                               "film_link": film.film_link})
        return films_list

    def writing_into_json(dict):
        str_dict = json.dumps(dict)
        with open("db.json", "w") as file:
            file.write(str_dict)

    with open("db.json", "r") as file:
        s = file.read()
    dictionary = json.loads(s)
    films_list = get_list_films()
    is_single_chat = 0
    for index_chat in range(len(dictionary['chats'])):
        if dictionary["chats"][index_chat]["chat_id"] == message.chat.id:
            is_single_chat += 1
    if is_single_chat == 0:

        dictionary["chats"].append({"chat_id": message.chat.id, "posts": [{"post_id": post_id,
                                                                           "current_page": current_page,
                                                                           "films": films_list}]})
        writing_into_json(dictionary)
    else:
        for index_chat in range(len(dictionary['chats'])):
            if dictionary["chats"][index_chat]["chat_id"] == message.chat.id:
                is_single_post = 0
                for index_post in range(len(dictionary["chats"][index_chat]["posts"])):
                    if dictionary["chats"][index_chat]["posts"][index_post]["post_id"] == post_id:
                        is_single_post += 1
                if is_single_post == 0:

                    dictionary["chats"][index_chat]["posts"].append({"post_id": post_id,
                                                                     "current_page": current_page,
                                                                     "films": films_list})
                    writing_into_json(dictionary)
                else:
                    for index_post in range(len(dictionary["chats"][index_chat]["posts"])):
                        if dictionary["chats"][index_chat]["posts"][index_post]["post_id"] == post_id:
                            dictionary["chats"][index_chat]["posts"][index_post] = {"post_id": post_id,
                                                                                    "current_page": current_page,
                                                                                    "films": films_list}
                            writing_into_json(dictionary)


def get_from_json(chat_id, post_id):
    with open("db.json", "r") as file:
        s = file.read()
    dictionary = json.loads(s)
    film_list = []
    for index_chat in range(len(dictionary["chats"])):
        if dictionary["chats"][index_chat]["chat_id"] == chat_id:
            for index_post in range(len(dictionary["chats"][index_chat]["posts"])):
                if dictionary["chats"][index_chat]["posts"][index_post]["post_id"] == post_id:
                    for index_film in range(len(dictionary["chats"][index_chat]["posts"][index_post]["films"])):
                        film_name = dictionary["chats"][index_chat]["posts"][index_post]["films"][index_film][
                            "film_name"]
                        film_year = dictionary["chats"][index_chat]["posts"][index_post]["films"][index_film][
                            "film_year"]
                        film_country = dictionary["chats"][index_chat]["posts"][index_post]["films"][index_film][
                            "film_country"]
                        film_genre = dictionary["chats"][index_chat]["posts"][index_post]["films"][index_film][
                            "film_genre"]
                        film_link = dictionary["chats"][index_chat]["posts"][index_post]["films"][index_film][
                            "film_link"]
                        film_id = film_link.split('/')[-1].split('-')[0]
                        film = Film(film_id, film_name, film_year, film_country, film_genre, film_link)
                        film_list.append(film)
    return film_list

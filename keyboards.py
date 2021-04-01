from telebot import types
from curl import get_trailer, get_film, get_episode_list, get_series
from utils import chunks, get_film_id
import datetime


def on_years_keyboard(category, page):
    years = [year for year in range(1916, datetime.datetime.now().year + 1)]
    years.reverse()
    years_chunked = chunks(years)

    def mini_keyboard():
        markup = types.InlineKeyboardMarkup()
        if len(years_chunked[page]) == 1:
            markup.add(types.InlineKeyboardButton(text=years_chunked[page][0],
                                                  callback_data=f"year_{years_chunked[page][0]}_{category}"))
        elif len(years_chunked[page]) == 2:
            markup.add(types.InlineKeyboardButton(text=years_chunked[page][0],
                                                  callback_data=f"year_{years_chunked[page][0]}_{category}"),
                       types.InlineKeyboardButton(text=years_chunked[page][1],
                                                  callback_data=f"year_{years_chunked[page][1]}_{category}"))
        elif len(years_chunked[page]) == 3:
            markup.add(types.InlineKeyboardButton(text=years_chunked[page][0],
                                                  callback_data=f"year_{years_chunked[page][0]}_{category}"),
                       types.InlineKeyboardButton(text=years_chunked[page][1],
                                                  callback_data=f"year_{years_chunked[page][1]}_{category}"),
                       types.InlineKeyboardButton(text=years_chunked[page][2],
                                                  callback_data=f"year_{years_chunked[page][2]}_{category}")
                       )
        elif len(years_chunked[page]) == 4:
            markup.add(types.InlineKeyboardButton(text=years_chunked[page][0],
                                                  callback_data=f"year_{years_chunked[page][0]}_{category}"),
                       types.InlineKeyboardButton(text=years_chunked[page][1],
                                                  callback_data=f"year_{years_chunked[page][1]}_{category}"),
                       types.InlineKeyboardButton(text=years_chunked[page][2],
                                                  callback_data=f"year_{years_chunked[page][2]}_{category}"),
                       types.InlineKeyboardButton(text=years_chunked[page][3],
                                                  callback_data=f"year_{years_chunked[page][3]}_{category}")
                       )
        elif len(years_chunked[page]) == 5:
            markup.add(types.InlineKeyboardButton(text=years_chunked[page][0],
                                                  callback_data=f"year_{years_chunked[page][0]}_{category}"),
                       types.InlineKeyboardButton(text=years_chunked[page][1],
                                                  callback_data=f"year_{years_chunked[page][1]}_{category}"),
                       types.InlineKeyboardButton(text=years_chunked[page][2],
                                                  callback_data=f"year_{years_chunked[page][2]}_{category}"),
                       types.InlineKeyboardButton(text=years_chunked[page][3],
                                                  callback_data=f"year_{years_chunked[page][3]}_{category}"),
                       types.InlineKeyboardButton(text=years_chunked[page][4],
                                                  callback_data=f"year_{years_chunked[page][4]}_{category}")
                       )
        elif len(years_chunked[page]) == 6:
            markup.add(types.InlineKeyboardButton(text=years_chunked[page][0],
                                                  callback_data=f"year_{years_chunked[page][0]}_{category}"),
                       types.InlineKeyboardButton(text=years_chunked[page][1],
                                                  callback_data=f"year_{years_chunked[page][1]}_{category}"),
                       types.InlineKeyboardButton(text=years_chunked[page][2],
                                                  callback_data=f"year_{years_chunked[page][2]}_{category}"),
                       types.InlineKeyboardButton(text=years_chunked[page][3],
                                                  callback_data=f"year_{years_chunked[page][3]}_{category}"),
                       types.InlineKeyboardButton(text=years_chunked[page][4],
                                                  callback_data=f"year_{years_chunked[page][4]}_{category}"),
                       types.InlineKeyboardButton(text=years_chunked[page][5],
                                                  callback_data=f"year_{years_chunked[page][5]}_{category}")
                       )
        return markup

    if len(years_chunked) == 1:
        markup = mini_keyboard()
    else:
        if page == 0:
            markup = mini_keyboard()
            markup.add(types.InlineKeyboardButton(text='Следующая страница',
                                                  callback_data=f'ypage_{page + 1}_{category}'))
        elif page != 0 and page < len(years_chunked) and page + 1 != len(years_chunked):
            markup = mini_keyboard()
            markup.add(types.InlineKeyboardButton(text="Предыдущая страница",
                                                  callback_data=f'ypage_{page - 1}_{category}'),
                       types.InlineKeyboardButton(text="Следующая страница",
                                                  callback_data=f'ypage_{page + 1}_{category}'))
        elif page + 1 == len(years_chunked):
            markup = mini_keyboard()
            markup.add(types.InlineKeyboardButton(text="Предыдущая страница",
                                                  callback_data=f'ypage_{page - 1}_{category}'))
    return markup


def film_viewing_keyboard(film_link, message_id):
    markup = types.InlineKeyboardMarkup()
    if get_trailer(film_link) != "no link":
        markup.add(types.InlineKeyboardButton(text="Трейлер", url=get_trailer(film_link)))
    if get_episode_list(film_link)[0] != "no link":
        markup.add(types.InlineKeyboardButton(text="Выбор зесона",
                                              callback_data=f"choose_season_{get_film_id(film_link)}_{message_id}"))
    if get_film(film_link) != "no link":
        markup.add(types.InlineKeyboardButton(text="Смотреть в высоком качестве", url=get_film(film_link)))
    return markup


def choose_episode_keyboard(film_link, page, message_id, season):
    episodes_list = [i for i in range(1, get_episode_list(film_link)[1][season] + 1)]
    chunked_episode_list = chunks(episodes_list)

    def mini_keyboard():
        markup = types.InlineKeyboardMarkup()
        if len(chunked_episode_list[page]) == 1:
            markup.add(types.InlineKeyboardButton(text=f'эпизод {chunked_episode_list[page][0]}',
                                                  url=get_series(film_link, chunked_episode_list[page][0], season + 1)))
        elif len(chunked_episode_list[page]) == 2:
            markup.add(types.InlineKeyboardButton(text=f'эпизод {chunked_episode_list[page][0]}',
                                                  url=get_series(film_link, chunked_episode_list[page][0], season + 1)),
                       types.InlineKeyboardButton(text=f'эпизод {chunked_episode_list[page][1]}',
                                                  url=get_series(film_link, chunked_episode_list[page][1], season + 1)))
        elif len(chunked_episode_list[page]) == 3:
            markup.add(types.InlineKeyboardButton(text=f'эпизод {chunked_episode_list[page][0]}',
                                                  url=get_series(film_link, chunked_episode_list[page][0], season + 1)),
                       types.InlineKeyboardButton(text=f'эпизод {chunked_episode_list[page][1]}',
                                                  url=get_series(film_link, chunked_episode_list[page][1], season + 1)),
                       types.InlineKeyboardButton(text=f'эпизод {chunked_episode_list[page][2]}',
                                                  url=get_series(film_link, chunked_episode_list[page][2], season + 1))
                       )
        elif len(chunked_episode_list[page]) == 4:
            markup.add(types.InlineKeyboardButton(text=f'эпизод {chunked_episode_list[page][0]}',
                                                  url=get_series(film_link, chunked_episode_list[page][0], season + 1)),
                       types.InlineKeyboardButton(text=f'эпизод {chunked_episode_list[page][1]}',
                                                  url=get_series(film_link, chunked_episode_list[page][1], season + 1)),
                       types.InlineKeyboardButton(text=f'эпизод {chunked_episode_list[page][2]}',
                                                  url=get_series(film_link, chunked_episode_list[page][2], season + 1)),
                       types.InlineKeyboardButton(text=f'эпизод {chunked_episode_list[page][3]}',
                                                  url=get_series(film_link, chunked_episode_list[page][3], season + 1))
                       )
        elif len(chunked_episode_list[page]) == 5:
            markup.add(types.InlineKeyboardButton(text=f'эпизод {chunked_episode_list[page][0]}',
                                                  url=get_series(film_link, chunked_episode_list[page][0], season + 1)),
                       types.InlineKeyboardButton(text=f'эпизод {chunked_episode_list[page][1]}',
                                                  url=get_series(film_link, chunked_episode_list[page][1], season + 1)),
                       types.InlineKeyboardButton(text=f'эпизод {chunked_episode_list[page][2]}',
                                                  url=get_series(film_link, chunked_episode_list[page][2], season + 1)),
                       types.InlineKeyboardButton(text=f'эпизод {chunked_episode_list[page][3]}',
                                                  url=get_series(film_link, chunked_episode_list[page][3], season + 1)),
                       types.InlineKeyboardButton(text=f'эпизод {chunked_episode_list[page][4]}',
                                                  url=get_series(film_link, chunked_episode_list[page][4], season + 1))
                       )
        elif len(chunked_episode_list[page]) == 6:
            markup.add(types.InlineKeyboardButton(text=f'эпизод {chunked_episode_list[page][0]}',
                                                  url=get_series(film_link, chunked_episode_list[page][0], season + 1)),
                       types.InlineKeyboardButton(text=f'эпизод {chunked_episode_list[page][1]}',
                                                  url=get_series(film_link, chunked_episode_list[page][1], season + 1)),
                       types.InlineKeyboardButton(text=f'эпизод {chunked_episode_list[page][2]}',
                                                  url=get_series(film_link, chunked_episode_list[page][3], season + 1)),
                       types.InlineKeyboardButton(text=f'эпизод {chunked_episode_list[page][3]}',
                                                  url=get_series(film_link, chunked_episode_list[page][3], season + 1)),
                       types.InlineKeyboardButton(text=f'эпизод {chunked_episode_list[page][4]}',
                                                  url=get_series(film_link, chunked_episode_list[page][4], season + 1)),
                       types.InlineKeyboardButton(text=f'эпизод {chunked_episode_list[page][5]}',
                                                  url=get_series(film_link, chunked_episode_list[page][5], season + 1))
                       )
        return markup

    if len(chunked_episode_list) == 1:
        markup = mini_keyboard()
    else:
        if page == 0:
            markup = mini_keyboard()
            markup.add(types.InlineKeyboardButton(text='Следующая страница',
                                                  callback_data=f'epage_{season}_{page + 1}_{get_film_id(film_link)}_'
                                                                f'{message_id}'))
        elif page != 0 and page < len(chunked_episode_list) and page + 1 != len(chunked_episode_list):
            markup = mini_keyboard()
            markup.add(types.InlineKeyboardButton(text="Предыдущая страница",
                                                  callback_data=f'epage_{season}_{page - 1}_{get_film_id(film_link)}_'
                                                                f'{message_id}'),
                       types.InlineKeyboardButton(text="Следующая страница",
                                                  callback_data=f'epage_{season}_{page + 1}_{get_film_id(film_link)}_'
                                                                f'{message_id}'))
        elif page + 1 == len(chunked_episode_list):
            markup = mini_keyboard()
            markup.add(types.InlineKeyboardButton(text="Предыдущая страница",
                                                  callback_data=f'epage_{season}_{page - 1}_{get_film_id(film_link)}_'
                                                                f'{message_id}'))
    return markup


def choose_season_keyboard(film_link, page, message_id):
    seasons_list = [i for i in range(1, get_episode_list(film_link)[0] + 1)]
    chunked_season_list = chunks(seasons_list)

    def mini_keyboard():
        markup = types.InlineKeyboardMarkup()
        if len(chunked_season_list[page]) == 1:
            markup.add(types.InlineKeyboardButton(text=f'сезон {chunked_season_list[page][0]}',
                                                  callback_data=f"season_{chunked_season_list[page][0] - 1}_"
                                                                f"{get_film_id(film_link)}_{message_id}"))
        elif len(chunked_season_list[page]) == 2:
            markup.add(types.InlineKeyboardButton(text=f'сезон {chunked_season_list[page][0]}',
                                                  callback_data=f"season_{chunked_season_list[page][0] - 1}_"
                                                                f"{get_film_id(film_link)}_{message_id}"),
                       types.InlineKeyboardButton(text=f'сезон {chunked_season_list[page][1]}',
                                                  callback_data=f"season_{chunked_season_list[page][1] - 1}_"
                                                                f"{get_film_id(film_link)}_{message_id}"))
        elif len(chunked_season_list[page]) == 3:
            markup.add(types.InlineKeyboardButton(text=f'сезон {chunked_season_list[page][0]}',
                                                  callback_data=f"season_{chunked_season_list[page][0] - 1}_"
                                                                f"{get_film_id(film_link)}_{message_id}"),
                       types.InlineKeyboardButton(text=f'сезон {chunked_season_list[page][1]}',
                                                  callback_data=f"season_{chunked_season_list[page][1] - 1}_"
                                                                f"{get_film_id(film_link)}_{message_id}"),
                       types.InlineKeyboardButton(text=f'сезон {chunked_season_list[page][2]}',
                                                  callback_data=f"season_{chunked_season_list[page][2] - 1}_"
                                                                f"{get_film_id(film_link)}_{message_id}")
                       )
        elif len(chunked_season_list[page]) == 4:
            markup.add(types.InlineKeyboardButton(text=f'сезон {chunked_season_list[page][0]}',
                                                  callback_data=f"season_{chunked_season_list[page][0] - 1}_"
                                                                f"{get_film_id(film_link)}_{message_id}"),
                       types.InlineKeyboardButton(text=f'сезон {chunked_season_list[page][1]}',
                                                  callback_data=f"season_{chunked_season_list[page][1] - 1}_"
                                                                f"{get_film_id(film_link)}_{message_id}"),
                       types.InlineKeyboardButton(text=f'сезон {chunked_season_list[page][2]}',
                                                  callback_data=f"season_{chunked_season_list[page][2] - 1}_"
                                                                f"{get_film_id(film_link)}_{message_id}"),
                       types.InlineKeyboardButton(text=f'сезон {chunked_season_list[page][3]}',
                                                  callback_data=f"season_{chunked_season_list[page][3] - 1}_"
                                                                f"{get_film_id(film_link)}_{message_id}")
                       )
        elif len(chunked_season_list[page]) == 5:
            markup.add(types.InlineKeyboardButton(text=f'сезон {chunked_season_list[page][0]}',
                                                  callback_data=f"season_{chunked_season_list[page][0] - 1}_"
                                                                f"{get_film_id(film_link)}_{message_id}"),
                       types.InlineKeyboardButton(text=f'сезон {chunked_season_list[page][1]}',
                                                  callback_data=f"season_{chunked_season_list[page][1] - 1}_"
                                                                f"{get_film_id(film_link)}_{message_id}"),
                       types.InlineKeyboardButton(text=f'сезон {chunked_season_list[page][2]}',
                                                  callback_data=f"season_{chunked_season_list[page][2] - 1}_"
                                                                f"{get_film_id(film_link)}_{message_id}"),
                       types.InlineKeyboardButton(text=f'сезон {chunked_season_list[page][3]}',
                                                  callback_data=f"season_{chunked_season_list[page][3] - 1}_"
                                                                f"{get_film_id(film_link)}_{message_id}"),
                       types.InlineKeyboardButton(text=f'сезон {chunked_season_list[page][4]}',
                                                  callback_data=f"season_{chunked_season_list[page][4] - 1}_"
                                                                f"{get_film_id(film_link)}_{message_id}")
                       )
        elif len(chunked_season_list[page]) == 6:
            markup.add(types.InlineKeyboardButton(text=f'сезон {chunked_season_list[page][0]}',
                                                  callback_data=f"season_{chunked_season_list[page][0] - 1}_"
                                                                f"{get_film_id(film_link)}_{message_id}"),
                       types.InlineKeyboardButton(text=f'сезон {chunked_season_list[page][1]}',
                                                  callback_data=f"season_{chunked_season_list[page][1] - 1}_"
                                                                f"{get_film_id(film_link)}_{message_id}"),
                       types.InlineKeyboardButton(text=f'сезон {chunked_season_list[page][2]}',
                                                  callback_data=f"season_{chunked_season_list[page][2] - 1}_"
                                                                f"{get_film_id(film_link)}_{message_id}"),
                       types.InlineKeyboardButton(text=f'сезон {chunked_season_list[page][3]}',
                                                  callback_data=f"season_{chunked_season_list[page][3] - 1}_"
                                                                f"{get_film_id(film_link)}_{message_id}"),
                       types.InlineKeyboardButton(text=f'сезон {chunked_season_list[page][4]}',
                                                  callback_data=f"season_{chunked_season_list[page][4] - 1}_"
                                                                f"{get_film_id(film_link)}_{message_id}"),
                       types.InlineKeyboardButton(text=f'сезон {chunked_season_list[page][5]}',
                                                  callback_data=f"season_{chunked_season_list[page][5] - 1}_"
                                                                f"{get_film_id(film_link)}_{message_id}")
                       )
        return markup

    if len(chunked_season_list) == 1:
        markup = mini_keyboard()
    else:
        if page == 0:
            markup = mini_keyboard()
            markup.add(types.InlineKeyboardButton(text='Следующая страница',
                                                  callback_data=f'spage_{page + 1}_{get_film_id(film_link)}_'
                                                                f'{message_id}'))
        elif page != 0 and page < len(chunked_season_list) and page + 1 != len(chunked_season_list):
            markup = mini_keyboard()
            markup.add(types.InlineKeyboardButton(text="Предыдущая страница",
                                                  callback_data=f'spage_{page - 1}_{get_film_id(film_link)}_'
                                                                f'{message_id}'),
                       types.InlineKeyboardButton(text="Следующая страница",
                                                  callback_data=f'spage_{page + 1}_{get_film_id(film_link)}_'
                                                                f'{message_id}'))
        elif page + 1 == len(chunked_season_list):
            markup = mini_keyboard()
            markup.add(types.InlineKeyboardButton(text="Предыдущая страница",
                                                  callback_data=f'spage_{page - 1}_{get_film_id(film_link)}_'
                                                                f'{message_id}'))
    return markup


def main_reply_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    btn_movie = types.KeyboardButton('🎥 Фильмы')
    btn_search = types.KeyboardButton('🔎 Поиск')
    btn_serial = types.KeyboardButton('🗂 Сериалы')
    btn_cartoon = types.KeyboardButton('🧸 Мультфильмы')
    btn_anime = types.KeyboardButton('🏯 Аниме')
    markup.add(btn_movie, btn_search, btn_serial, btn_cartoon, btn_anime)
    return markup


def search_filter_reply_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_back = types.KeyboardButton('↩️ Вернуться')
    btn_latest_arrivals = types.KeyboardButton('Последние поступления')
    btn_popular = types.KeyboardButton('Популярные')
    btn_soon = types.KeyboardButton('В ожидании')
    btn_by_year = types.KeyboardButton('По году')
    markup.row(btn_back)
    markup.row(btn_latest_arrivals, btn_popular)
    markup.row(btn_soon, btn_by_year)
    return markup


def back_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_back = types.KeyboardButton('↩️ Вернуться')
    markup.add(btn_back)
    return markup


def list_films_keyboard(list_films, page, message_id):
    def mini_keyboard():
        markup = types.InlineKeyboardMarkup()
        if len(list_films[page]) == 1:
            markup.add(types.InlineKeyboardButton(text=1,
                                                  callback_data=f"film_{list_films[page][0].film_id}_{message_id}"))
        elif len(list_films[page]) == 2:
            markup.add(types.InlineKeyboardButton(text=1,
                                                  callback_data=f"film_{list_films[page][0].film_id}_{message_id}"),
                       types.InlineKeyboardButton(text=2,
                                                  callback_data=f"film_{list_films[page][1].film_id}_{message_id}"))
        elif len(list_films[page]) == 3:
            markup.add(types.InlineKeyboardButton(text=1,
                                                  callback_data=f"film_{list_films[page][0].film_id}_{message_id}"),
                       types.InlineKeyboardButton(text=2,
                                                  callback_data=f"film_{list_films[page][1].film_id}_{message_id}"),
                       types.InlineKeyboardButton(text=3,
                                                  callback_data=f"film_{list_films[page][2].film_id}_{message_id}")
                       )
        elif len(list_films[page]) == 4:
            markup.add(types.InlineKeyboardButton(text=1,
                                                  callback_data=f"film_{list_films[page][0].film_id}_{message_id}"),
                       types.InlineKeyboardButton(text=2,
                                                  callback_data=f"film_{list_films[page][1].film_id}_{message_id}"),
                       types.InlineKeyboardButton(text=3,
                                                  callback_data=f"film_{list_films[page][2].film_id}_{message_id}"),
                       types.InlineKeyboardButton(text=4,
                                                  callback_data=f"film_{list_films[page][3].film_id}_{message_id}")
                       )
        elif len(list_films[page]) == 5:
            markup.add(types.InlineKeyboardButton(text=1,
                                                  callback_data=f"film_{list_films[page][0].film_id}_{message_id}"),
                       types.InlineKeyboardButton(text=2,
                                                  callback_data=f"film_{list_films[page][1].film_id}_{message_id}"),
                       types.InlineKeyboardButton(text=3,
                                                  callback_data=f"film_{list_films[page][2].film_id}_{message_id}"),
                       types.InlineKeyboardButton(text=4,
                                                  callback_data=f"film_{list_films[page][3].film_id}_{message_id}"),
                       types.InlineKeyboardButton(text=5,
                                                  callback_data=f"film_{list_films[page][4].film_id}_{message_id}")
                       )
        elif len(list_films[page]) == 6:
            markup.add(types.InlineKeyboardButton(text=1,
                                                  callback_data=f"film_{list_films[page][0].film_id}_{message_id}"),
                       types.InlineKeyboardButton(text=2,
                                                  callback_data=f"film_{list_films[page][1].film_id}_{message_id}"),
                       types.InlineKeyboardButton(text=3,
                                                  callback_data=f"film_{list_films[page][2].film_id}_{message_id}"),
                       types.InlineKeyboardButton(text=4,
                                                  callback_data=f"film_{list_films[page][3].film_id}_{message_id}"),
                       types.InlineKeyboardButton(text=5,
                                                  callback_data=f"film_{list_films[page][4].film_id}_{message_id}"),
                       types.InlineKeyboardButton(text=6,
                                                  callback_data=f"film_{list_films[page][5].film_id}_{message_id}")
                       )
        return markup

    if len(list_films) == 1:
        markup = mini_keyboard()
    else:
        if page == 0:
            markup = mini_keyboard()
            markup.add(
                types.InlineKeyboardButton(text='Следующая страница', callback_data=f'fpage_{page + 1}_{message_id}'))
        elif page != 0 and page < len(list_films) and page + 1 != len(list_films):
            markup = mini_keyboard()
            markup.add(
                types.InlineKeyboardButton(text="Предыдущая страница", callback_data=f'fpage_{page - 1}_{message_id}'),
                types.InlineKeyboardButton(text="Следующая страница", callback_data=f'fpage_{page + 1}_{message_id}'))
        elif page + 1 == len(list_films):
            markup = mini_keyboard()
            markup.add(
                types.InlineKeyboardButton(text="Предыдущая страница", callback_data=f'fpage_{page - 1}_{message_id}'))
    return markup

import telebot
from parser import get_films_name_from_page, get_full_film_info
from utils import do_search, chunks, post_message, get_from_json, write_into_json, get_film_id
from keyboards import *
import urllib


import db
from SECRET import BOT_KEY

bot = telebot.TeleBot(BOT_KEY)


#with db.create_connection('cinema.db') as connection:
    #users_to_states = db.select_from_users_to_states(connection)
    #for user_to_state in users_to_states:
        #db.update_user_to_state(connection, user_to_state[0], user_to_state[1], 1)
        #bot.send_message(user_to_state[1], 'Привет!!', reply_markup=main_reply_keyboard())
    #db.delete_from_users(connection)
    #db.delete_from_users_to_states(connection)
    #for user in users:
        #db.update_user_to_state()

@bot.message_handler(commands=['start'])
def start_message(message):
    with db.create_connection('cinema.db') as connection:
        try:
            user_info = db.select_from_users_by_telegram_id(connection, message.chat.id)
            if user_info == []:
                db.insert_into_users(connection, message.chat.id)
                user_info = db.select_from_users_by_telegram_id(connection, message.chat.id)
                db.insert_into_users_to_states(connection, user_info[0][0], 1)
                bot.send_message(message.chat.id, "Привет!!", reply_markup=main_reply_keyboard())
            elif user_info[0][1] == message.from_user.id:
                user_to_state_info = db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)
                db.update_user_to_state(connection, user_to_state_info[0][0], user_info[0][0], 1)
                bot.send_message(message.chat.id, f"Привет {message.from_user.first_name} !!",
                                 reply_markup=main_reply_keyboard())
        except Exception as e:
            print(e)


@bot.message_handler(content_types=['text'])
def menu(message):
    if message.text == '🎥 Фильмы':
        with db.create_connection('cinema.db') as connection:
            if db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[0][2] == "main menu":
                db.update_user_to_state(connection,
                                        db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[
                                            0][0],
                                        db.select_from_users_by_telegram_id(connection, message.chat.id)[0][0], 2)
                bot.send_message(message.chat.id, "Выберите категорию", reply_markup=search_filter_reply_keyboard())
    elif message.text == '🔎 Поиск':
        with db.create_connection('cinema.db') as connection:
            if db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[0][2] == "main menu":
                bot.send_message(message.chat.id, "Введите поисковый запрос", reply_markup=back_keyboard())
                db.update_user_to_state(connection,
                                        db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[
                                            0][0],
                                        db.select_from_users_by_telegram_id(connection, message.chat.id)[0][0], 6)
    elif message.text == '🗂 Сериалы':
        with db.create_connection('cinema.db') as connection:
            if db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[0][2] == "main menu":
                db.update_user_to_state(connection,
                                        db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[
                                            0][0],
                                        db.select_from_users_by_telegram_id(connection, message.chat.id)[0][0], 3)
                bot.send_message(message.chat.id, "Выберите категорию", reply_markup=search_filter_reply_keyboard())
    elif message.text == '🧸 Мультфильмы':
        with db.create_connection('cinema.db') as connection:
            if db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[0][2] == "main menu":
                db.update_user_to_state(connection,
                                        db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[
                                            0][0],
                                        db.select_from_users_by_telegram_id(connection, message.chat.id)[0][0], 4)
                bot.send_message(message.chat.id, "Выберите категорию", reply_markup=search_filter_reply_keyboard())
    elif message.text == '🏯 Аниме':
        with db.create_connection('cinema.db') as connection:
            if db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[0][2] == "main menu":
                db.update_user_to_state(connection,
                                        db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[
                                            0][0],
                                        db.select_from_users_by_telegram_id(connection, message.chat.id)[0][0], 5)
                bot.send_message(message.chat.id, "Выберите категорию", reply_markup=search_filter_reply_keyboard())
    elif message.text == '↩️ Вернуться':
        with db.create_connection('cinema.db') as connection:
            if db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[0][2] == "in movie":
                db.update_user_to_state(connection,
                                        db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[
                                            0][0],
                                        db.select_from_users_by_telegram_id(connection, message.chat.id)[0][0], 1)
                bot.send_message(message.chat.id, "Вы находитесь в главном меню", reply_markup=main_reply_keyboard())
            elif db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[0][2] == "in serial":
                db.update_user_to_state(connection,
                                        db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[
                                            0][0],
                                        db.select_from_users_by_telegram_id(connection, message.chat.id)[0][0], 1)
                bot.send_message(message.chat.id, "Вы находитесь в главном меню", reply_markup=main_reply_keyboard())
            elif db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[0][2] == "in cartoon":
                db.update_user_to_state(connection,
                                        db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[
                                            0][0],
                                        db.select_from_users_by_telegram_id(connection, message.chat.id)[0][0], 1)
                bot.send_message(message.chat.id, "Вы находитесь в главном меню", reply_markup=main_reply_keyboard())
            elif db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[0][2] == "in anime":
                db.update_user_to_state(connection,
                                        db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[
                                            0][0],
                                        db.select_from_users_by_telegram_id(connection, message.chat.id)[0][0], 1)
                bot.send_message(message.chat.id, "Вы находитесь в главном меню", reply_markup=main_reply_keyboard())
            elif db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[0][2] == "in search":
                db.update_user_to_state(connection,
                                        db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[
                                            0][0],
                                        db.select_from_users_by_telegram_id(connection, message.chat.id)[0][0], 1)
                bot.send_message(message.chat.id, "Вы находитесь в главном меню", reply_markup=main_reply_keyboard())
    elif message.text == 'Последние поступления':
        with db.create_connection('cinema.db') as connection:
            if db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[0][2] == "in movie":
                films_list = get_films_name_from_page('https://rezka.ag/films/?filter=last')
                films = chunks(films_list)
                search_result = post_message(films, 0)
                message_info = bot.send_message(message.chat.id, search_result)
                bot.edit_message_reply_markup(message.chat.id, message_info.message_id,
                                              reply_markup=list_films_keyboard(films, 0, message_info.message_id))
                write_into_json(films_list, 0, message, message_info.message_id)
            elif db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[0][2] == "in serial":
                films_list = get_films_name_from_page('https://rezka.ag/series/?filter=last')
                films = chunks(films_list)
                search_result = post_message(films, 0)
                message_info = bot.send_message(message.chat.id, search_result)
                bot.edit_message_reply_markup(message.chat.id, message_info.message_id,
                                              reply_markup=list_films_keyboard(films, 0, message_info.message_id))
                write_into_json(films_list, 0, message, message_info.message_id)
            elif db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[0][2] == "in cartoon":
                films_list = get_films_name_from_page('https://rezka.ag/cartoons/?filter=last')
                films = chunks(films_list)
                search_result = post_message(films, 0)
                message_info = bot.send_message(message.chat.id, search_result)
                bot.edit_message_reply_markup(message.chat.id, message_info.message_id,
                                              reply_markup=list_films_keyboard(films, 0, message_info.message_id))
                write_into_json(films_list, 0, message, message_info.message_id)
            elif db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[0][2] == "in anime":
                films_list = get_films_name_from_page('https://rezka.ag/animation/?filter=last')
                films = chunks(films_list)
                search_result = post_message(films, 0)
                message_info = bot.send_message(message.chat.id, search_result)
                bot.edit_message_reply_markup(message.chat.id, message_info.message_id,
                                              reply_markup=list_films_keyboard(films, 0, message_info.message_id))
                write_into_json(films_list, 0, message, message_info.message_id)
    elif message.text == 'Популярные':
        with db.create_connection('cinema.db') as connection:
            if db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[0][2] == "in movie":
                films_list = get_films_name_from_page('https://rezka.ag/films/?filter=popular')
                films = chunks(films_list)
                search_result = post_message(films, 0)
                message_info = bot.send_message(message.chat.id, search_result)
                bot.edit_message_reply_markup(message.chat.id, message_info.message_id,
                                              reply_markup=list_films_keyboard(films, 0, message_info.message_id))
                write_into_json(films_list, 0, message, message_info.message_id)
            elif db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[0][2] == "in serial":
                films_list = get_films_name_from_page('https://rezka.ag/series/?filter=popular')
                films = chunks(films_list)
                search_result = post_message(films, 0)
                message_info = bot.send_message(message.chat.id, search_result)
                bot.edit_message_reply_markup(message.chat.id, message_info.message_id,
                                              reply_markup=list_films_keyboard(films, 0, message_info.message_id))
                write_into_json(films_list, 0, message, message_info.message_id)
            elif db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[0][2] == "in cartoon":
                films_list = get_films_name_from_page('https://rezka.ag/cartoons/?filter=popular')
                films = chunks(films_list)
                search_result = post_message(films, 0)
                message_info = bot.send_message(message.chat.id, search_result)
                bot.edit_message_reply_markup(message.chat.id, message_info.message_id,
                                              reply_markup=list_films_keyboard(films, 0, message_info.message_id))
                write_into_json(films_list, 0, message, message_info.message_id)
            elif db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[0][2] == "in anime":
                films_list = get_films_name_from_page('https://rezka.ag/animation/?filter=popular')
                films = chunks(films_list)
                search_result = post_message(films, 0)
                message_info = bot.send_message(message.chat.id, search_result)
                bot.edit_message_reply_markup(message.chat.id, message_info.message_id,
                                              reply_markup=list_films_keyboard(films, 0, message_info.message_id))
                write_into_json(films_list, 0, message, message_info.message_id)
    elif message.text == 'В ожидании':
        with db.create_connection('cinema.db') as connection:
            if db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[0][2] == "in movie":
                films_list = get_films_name_from_page('https://rezka.ag/films/?filter=soon')
                films = chunks(films_list)
                search_result = post_message(films, 0)
                message_info = bot.send_message(message.chat.id, search_result)
                bot.edit_message_reply_markup(message.chat.id, message_info.message_id,
                                              reply_markup=list_films_keyboard(films, 0, message_info.message_id))
                write_into_json(films_list, 0, message, message_info.message_id)
            elif db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[0][2] == "in serial":
                films_list = get_films_name_from_page('https://rezka.ag/series/?filter=soon')
                films = chunks(films_list)
                search_result = post_message(films, 0)
                message_info = bot.send_message(message.chat.id, search_result)
                bot.edit_message_reply_markup(message.chat.id, message_info.message_id,
                                              reply_markup=list_films_keyboard(films, 0, message_info.message_id))
                write_into_json(films_list, 0, message, message_info.message_id)
            elif db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[0][2] == "in cartoon":
                films_list = get_films_name_from_page('https://rezka.ag/cartoons/?filter=soon')
                films = chunks(films_list)
                search_result = post_message(films, 0)
                message_info = bot.send_message(message.chat.id, search_result)
                bot.edit_message_reply_markup(message.chat.id, message_info.message_id,
                                              reply_markup=list_films_keyboard(films, 0, message_info.message_id))
                write_into_json(films_list, 0, message, message_info.message_id)
            elif db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[0][2] == "in anime":
                films_list = get_films_name_from_page('https://rezka.ag/animation/?filter=soon')
                films = chunks(films_list)
                search_result = post_message(films, 0)
                message_info = bot.send_message(message.chat.id, search_result)
                bot.edit_message_reply_markup(message.chat.id, message_info.message_id,
                                              reply_markup=list_films_keyboard(films, 0, message_info.message_id))
                write_into_json(films_list, 0, message, message_info.message_id)
    elif message.text == 'По году':
        with db.create_connection('cinema.db') as connection:
            if db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[0][2] == "in movie":
                bot.send_message(message.chat.id, "Выберите год", reply_markup=on_years_keyboard('films', 0))
            elif db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[0][2] == "in serial":
                bot.send_message(message.chat.id, "Выберите год", reply_markup=on_years_keyboard('series', 0))
            elif db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[0][2] == "in cartoon":
                bot.send_message(message.chat.id, "Выберите год", reply_markup=on_years_keyboard('cartoons', 0))
            elif db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[0][2] == "in anime":
                bot.send_message(message.chat.id, "Выберите год", reply_markup=on_years_keyboard('animation', 0))
    with db.create_connection('cinema.db') as connection:
        if db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[0][2] == "in search":
            sought = message.text
            if do_search(sought) == []:
                db.update_user_to_state(connection,
                                        db.select_by_telegram_id_from_users_to_states(connection, message.chat.id)[
                                            0][0],
                                        db.select_from_users_by_telegram_id(connection, message.chat.id)[0][0], 1)
                bot.send_message(message.chat.id, "По данному поисковому запросу ничего не найдено",
                                 reply_markup=main_reply_keyboard())
            elif message.text == "🔎 Поиск":
                bot.send_message(message.chat.id, 'Вы находитесь в меню поиска')
            else:
                films_list = do_search(sought)
                films = chunks(films_list)
                db.update_user_to_state(connection,
                                        db.select_by_telegram_id_from_users_to_states(connection,
                                                                                      message.chat.id)[
                                            0][0],
                                        db.select_from_users_by_telegram_id(connection, message.chat.id)[0][0],
                                        1)
                search_result = post_message(films, 0)

                bot.send_message(message.chat.id, "Вот результаты поиска", reply_markup=main_reply_keyboard())
                message_info = bot.send_message(message.chat.id, search_result)
                bot.edit_message_reply_markup(message.chat.id, message_info.message_id,
                                              reply_markup=list_films_keyboard(films, 0, message_info.message_id))
                write_into_json(films_list, 0, message, message_info.message_id)


@bot.callback_query_handler(func=lambda message: True)
def callback(call):
    if 'film_' in call.data:
        films = get_from_json(call.message.chat.id, call.message.message_id)
        for film in films:
            if call.data.split('_')[1] == get_film_id(film.film_link):
                film_link = film.film_link
                film_info = get_full_film_info(film_link)
                resource = urllib.request.urlopen(film_info[1])
                with open('img.jpg', 'wb') as file:
                    file.write(resource.read())
                message_id = call.data.split('_')[2]
                bot.send_photo(call.message.chat.id, photo=open("img.jpg", 'rb'), caption=film_info[0],
                               reply_markup=film_viewing_keyboard(film_link, message_id))
    elif 'fpage_' in call.data:
        films = chunks(get_from_json(call.message.chat.id, call.message.message_id))
        page = int(call.data.split("_")[1])
        search_result = post_message(films, page)
        message_id = call.data.split('_')[2]
        bot.edit_message_text(text=search_result, chat_id=call.message.chat.id, message_id=call.message.message_id,
                              reply_markup=list_films_keyboard(films, page, message_id))
    elif "choose_season_" in call.data:
        message_id = int(call.data.split('_')[-1])
        films = get_from_json(call.message.chat.id, message_id)
        for film in films:
            if call.data.split('_')[-2] == get_film_id(film.film_link):
                bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                              reply_markup=choose_season_keyboard(film.film_link, 0, message_id))
    elif "spage_" in call.data:
        message_id = int(call.data.split('_')[-1])
        films = get_from_json(call.message.chat.id, message_id)
        for film in films:
            if call.data.split('_')[-2] == get_film_id(film.film_link):
                bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                              reply_markup=choose_season_keyboard(film.film_link,
                                                                                  int(call.data.split('_')[-3]),
                                                                                  message_id))
    elif "season" in call.data:
        message_id = int(call.data.split('_')[-1])
        films = get_from_json(call.message.chat.id, message_id)
        for film in films:
            if call.data.split('_')[-2] == get_film_id(film.film_link):
                bot.answer_callback_query(call.id, 'Подождите немного')
                bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                              reply_markup=choose_episode_keyboard(film.film_link,
                                                                                   0,
                                                                                   message_id,
                                                                                   int(call.data.split('_')[-3])))
    elif "epage" in call.data:
        message_id = int(call.data.split('_')[-1])
        films = get_from_json(call.message.chat.id, message_id)
        for film in films:
            if call.data.split('_')[-2] == get_film_id(film.film_link):
                bot.answer_callback_query(call.id, 'Подождите немного')
                bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                              reply_markup=choose_episode_keyboard(film.film_link,
                                                                                   int(call.data.split('_')[-3]),
                                                                                   message_id,
                                                                                   int(call.data.split('_')[-4])))
    elif "ypage" in call.data:
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
                                      reply_markup=on_years_keyboard(call.data.split('_')[-1],
                                                                     int(call.data.split('_')[-2])))
    elif "year" in call.data:
        films_list = get_films_name_from_page(f'https://rezka.ag/{call.data.split("_")[-1]}/best/{call.data.split("_")[-2]}/')
        films = chunks(films_list)
        search_result = post_message(films, 0)
        message_info = bot.send_message(call.message.chat.id, search_result)
        bot.edit_message_reply_markup(call.message.chat.id, message_info.message_id,
                                      reply_markup=list_films_keyboard(films, 0, message_info.message_id))
        write_into_json(films_list, 0, call.message, message_info.message_id)


bot.polling()

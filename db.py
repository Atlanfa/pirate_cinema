import sqlite3
from sqlite3 import Error


def create_connection(db_path):
    connection = None
    try:
        connection = sqlite3.connect(db_path)
    except Error as e:
        print(e)

    return connection


# conn = sqlite3.connect('cinema.db')

# c = conn.cursor()
# c.execute("PRAGMA foreign_keys = ON")

# create_table_users = "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, telegram_id INTEGER)"
# create_table_states = "CREATE TABLE IF NOT EXISTS states(id INTEGER PRIMARY KEY, state_name TEXT)"
# create_table_users_to_states = "CREATE TABLE IF NOT EXISTS usersToStates(id INTEGER PRIMARY KEY , user_id INTEGER," \
# "state_id INTEGER, FOREIGN KEY(user_id) REFERENCES users(id) ON UPDATE CASCADE" \
# " ON DELETE CASCADE, FOREIGN KEY(state_id) REFERENCES states(id) ON UPDATE CASCADE " \
# "ON DELETE CASCADE)"
# create_table_films = "CREATE TABLE IF NOT EXISTS films(id INTEGER PRIMARY KEY, film_name TEXT, film_year TEXT, " \
# "film_country TEXT, film_genre TEXT, film_link TEXT)"

# c.execute(create_table_films)
# c.execute(create_table_users)
# c.execute(create_table_states)
# c.execute(create_table_users_to_states)


def insert_into_users(connection, telegram_id):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users(telegram_id) VALUES(?)", (telegram_id,))
    connection.commit()


def insert_into_states(connection, state_name):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO states(state_name) VALUES(?)", (state_name,))
    connection.commit()


def insert_into_users_to_states(connection, user_id, state_id):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO usersToStates(user_id, state_id) VALUES(?, ?)", (user_id, state_id))
    connection.commit()


def insert_into_films(connection, film_id, film_name, film_year, film_country, film_genre, film_link):
    cursor = connection.cursor()
    cursor.execute("INSERT or REPLACE INTO films(id, film_name, film_year, film_country, film_genre, film_link) "
                   "VALUES(?,?,?,?,?,?)",
                   (film_id, film_name, film_year, film_country, film_genre, film_link))
    connection.commit()


def delete_from_users(connection):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users")
    connection.commit()


def delete_from_states(connection):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM states")
    connection.commit()


def delete_from_users_to_states(connection):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM usersToStates")
    connection.commit()


def delete_from_films(connection):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM films")
    connection.commit()


def delete_by_id_from_users(connection, user_id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    connection.commit()


def delete_by_id_from_states(connection, state_id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM states WHERE id=?", (state_id,))
    connection.commit()


def delete_by_id_from_users_to_states(connection, user_to_state_id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM usersToStates WHERE id=?", (user_to_state_id,))
    connection.commit()


def delete_by_id_from_films(connection, film_id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM films WHERE id=?", (film_id,))
    connection.commit()


def select_by_id_from_users(connection, user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    connection.commit()
    return cursor.fetchall()


def select_by_id_from_states(connection, state_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM states WHERE id=?", (state_id,))
    connection.commit()
    return cursor.fetchall()


def select_by_id_from_users_to_states(connection, user_to_state_id):
    cursor = connection.cursor()
    cursor.execute("SELECT usersToStates.id, u.telegram_id, s.state_name  FROM usersToStates "
                   "LEFT JOIN users u on u.id = usersToStates.user_id "
                   "LEFT JOIN states s on s.id = usersToStates.state_id "
                   "WHERE usersToStates.id=? ", (user_to_state_id,))
    connection.commit()
    return cursor.fetchall()


def select_by_id_from_films(connection, film_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM films WHERE id=?", (film_id,))
    connection.commit()
    return cursor.fetchall()


def select_by_telegram_id_from_users_to_states(connection, user_id):
    cursor = connection.cursor()
    cursor.execute("SELECT usersToStates.id, u.telegram_id, s.state_name  FROM usersToStates "
                   "LEFT JOIN users u on u.id = usersToStates.user_id "
                   "LEFT JOIN states s on s.id = usersToStates.state_id "
                   "WHERE u.telegram_id=? ", (user_id,))
    connection.commit()
    return cursor.fetchall()


def select_by_film_link_from_films(connection, film_link):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM films WHERE film_link=?", (film_link,))
    connection.commit()
    return cursor.fetchall()


def select_from_users(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    connection.commit()
    return cursor.fetchall()


def select_from_users_by_telegram_id(connection, telegram_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE telegram_id=?", (telegram_id,))
    connection.commit()
    return cursor.fetchall()


def select_from_states(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM states")
    connection.commit()
    return cursor.fetchall()


def select_from_users_to_states(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT usersToStates.id, u.telegram_id, s.state_name  FROM usersToStates "
                   "LEFT JOIN users u on u.id = usersToStates.user_id "
                   "LEFT JOIN states s on s.id = usersToStates.state_id ")
    connection.commit()
    return cursor.fetchall()


def select_from_films(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM films")
    connection.commit()
    return cursor.fetchall()


def update_user(connection, user_id, telegram_id):
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET telegram_id=? WHERE id=?", (telegram_id, user_id))
    connection.commit()


def update_state(connection, state_id, state_name):
    cursor = connection.cursor()
    cursor.execute("UPDATE states SET state_name=? WHERE id=?", (state_name, state_id))
    connection.commit()


def update_user_to_state(connection, user_to_state_id, telegram_id, state_id):
    cursor = connection.cursor()
    cursor.execute("UPDATE usersToStates SET user_id=?, state_id=? WHERE id=?",
                   (telegram_id, state_id, user_to_state_id))
    connection.commit()


def update_film(connection, film_id, film_name, film_year, film_country, film_genre, film_link):
    cursor = connection.cursor()
    cursor.execute("UPDATE films SET film_name=?, film_year=?, film_country=?, film_genre=?, film_link=? WHERE id=?",
                   (film_name, film_year, film_country, film_genre, film_link, film_id))


def insert_states():
    delete_from_states(create_connection('cinema.db'))
    states = ['main menu', 'in movie', 'in serial', 'in cartoon', 'in anime', 'in movie years', 'in serial years',
              'in cartoon years', 'in anime years', 'in search']
    for item in states:
        insert_into_states(create_connection('cinema.db'), item)

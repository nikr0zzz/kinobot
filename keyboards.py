from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, \
    KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from prs import URL
button_search_film = KeyboardButton('Искать фильм по названию 🎥')
button_search_person = KeyboardButton('Искать персону по имени 👨‍')
button_search_on_filters = KeyboardButton('Искать по фильтрам ✏')
button_get_favour = KeyboardButton('Избранное 🌟')
button_back_to_menu = KeyboardButton('Возврат в меню 😅')
button_add_to_favor = KeyboardButton('Добавить в избранное ⭐️')
button_back_to_search_film = KeyboardButton('Искать другой фильм, сериал🎦')
button_back_to_search_person = KeyboardButton('Искать другую персону 😎')
button_type_film = KeyboardButton('Фильмы')
button_type_mfilm = KeyboardButton('Мультфильмы')
button_type_serial = KeyboardButton('Сериалы')
button_back_to_filter = KeyboardButton('Предыдущий фильтр')
genres = {'Биография':'2', 'Боевик':'3', 'Вестерн':'4', 'Детектив':'6', 'Документальный':'9', 'Драма':'10', 'Комедия':'13', 'Мелодрама':'17', 'Криминал':'16', 'Триллер':'27', 'Ужасы':'28', 'Фантастика':'29'}
years = ['2010-2020', '2000-2010', '1990-2000', '1980-1990', '1970-1980', '1960-1970','2000-2020','1980-2000', '1960-1980', '1960-2020']
rates = ['Не ниже 8', 'Не ниже 7', 'Не ниже 6', 'Не ниже 5']

menu_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(button_search_film).add(button_search_person).add(button_search_on_filters).add(button_get_favour)
back_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(button_back_to_menu)
search_film_menu_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(button_add_to_favor).add(button_back_to_search_film).add(button_back_to_menu)
search_film_menu_kb_v2 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(button_add_to_favor).add(button_back_to_menu)
choose_type_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).row(button_type_film, button_type_mfilm, button_type_serial).add(button_back_to_menu)
choose_genre_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, row_width=3)
choose_rate_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)

for genre in genres.keys():
    choose_genre_kb.insert(KeyboardButton(text=genre))
choose_genre_kb.add(button_back_to_filter).add(button_back_to_menu)

for rate in rates:
    choose_rate_kb.insert(KeyboardButton(text=rate))
choose_rate_kb.add(button_back_to_filter).add(button_back_to_menu)

choose_year_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='2010-2020'), KeyboardButton(text='2000-2010'), KeyboardButton(text='1990-2000')],
    [KeyboardButton(text='1980-1990'),KeyboardButton(text='1970-1980'),KeyboardButton(text='1960-1970')],
    [KeyboardButton(text='2000-2020'), KeyboardButton(text='1980-2000'), KeyboardButton(text='1960-1980')],
    [KeyboardButton(text='1960-2020')],
    [button_back_to_filter],
    [button_back_to_menu]
], resize_keyboard=True, one_time_keyboard=False)






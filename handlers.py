from aiogram import types
from aiogram.utils.markdown import text, bold, italic, code, pre, hbold
from aiogram.dispatcher.filters import Command
from bot import dp, bot
import states
import keyboards as kb
import prs
import database


class Page:
    film_pos = 0


j = Page

def get_film_caption(film):
    caption = hbold(film['name'] + ' ' + film['year'] + '\n' + ', '.join(film['genre']) + '\n' + ', '.join(film['country'])) + '\n' + \
              film['description'].strip() + '\n' + hbold(film['rating'])
    return caption


def get_person_caption(person):
    caption = hbold(person['name']) + ' ' + person['age'] + '\n\n' + hbold('Деятельность:\n') + ', '.join(person['prof']) + '\n\n'
    for award in person['awards']:
        caption += hbold('🏆 '+ award['name']+':\n') + award['wins'] +' ' + award['noms'] + '\n\n'
    caption += '👇👇ЛУЧШИЕ ФИЛЬМЫ👇👇'
    return caption



@dp.callback_query_handler(lambda call: True, state=[states.Film_Menu.person_ready, states.Film_Menu.filter_films_ready])
async def film_callback(call: types.CallbackQuery):
    if call.data in ['next', 'previous']:
        j.film_pos = j.film_pos+5 if call.data == 'next' else j.film_pos-5
        film_content = prs.filter_films
        link_kb = types.InlineKeyboardMarkup()
        if j.film_pos != 0:
            link_kb.add(types.InlineKeyboardButton(text='⏪⏪ Назад', callback_data='previous'))
        for i in range(j.film_pos, j.film_pos+5):
            if i < len(film_content['names']):
                link_kb.add(types.InlineKeyboardButton(text=film_content['names'][i], callback_data=film_content['urls'][i]))
            else:
                break
        if len(film_content['names']) > (j.film_pos+5):
            link_kb.add(types.InlineKeyboardButton(text='Далее ⏩⏩', callback_data='next'))
        await bot.answer_callback_query(call.id)
        await bot.send_message(call.from_user.id, f'Фильмы по вашему запросу: Cтраница {j.film_pos//5 + 1}', reply_markup=link_kb)
    else:
        film = prs.get_film_content(call.data)
        caption = get_film_caption(film)
        await bot.answer_callback_query(call.id)
        await bot.send_photo(call.from_user.id, photo=film['poster'], caption=caption, parse_mode=types.ParseMode.HTML,
                             reply_markup=kb.search_film_menu_kb_v2)

@dp.message_handler(Command("start"), state=None)
async def menu(message: types.Message):
    await message.answer('Привет я КиноБот помогу найти тебе фильмы и сериалы !', reply_markup=kb.menu_kb)
    await message.answer_sticker(r'CAACAgIAAxkBAAEBsHpf21oHoV4JvJETw9PIdBogMQRI3wACIAADDbbSGVmjiNFDIa13HgQ')
    await states.Start_Menu.start_menu.set()

@dp.message_handler(lambda msg: msg.text in kb.button_search_film.text, state=states.Start_Menu.start_menu)
async def find_fllm(message: types.Message):
    await message.answer('Введите название фильма', reply_markup=kb.back_kb)
    await states.Choose_Func.search_film.set()


@dp.message_handler(lambda msg: msg.text in kb.button_search_person.text, state=states.Start_Menu.start_menu)
async def find_person(message: types.Message):
    await message.answer('Введите название персоны', reply_markup=kb.back_kb)
    await states.Choose_Func.search_person.set()


@dp.message_handler(lambda msg: msg.text in kb.button_back_to_filter.text,
                    state=[states.Filter_Menu.choose_genre,
                           states.Filter_Menu.choose_rate,
                           states.Filter_Menu.choose_year])
async def back_to_prev_filter(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    state = await state.get_state()
    print(state)
    if state == 'Filter_Menu:choose_genre':
        await message.answer('Выберите тип', reply_markup=kb.choose_type_kb)
        await states.Choose_Func.search_on_filter.set()
    elif state == 'Filter_Menu:choose_year':
        await message.answer('Выберите жанр', reply_markup=kb.choose_genre_kb)
        await states.Filter_Menu.choose_genre.set()
    elif state == 'Filter_Menu:choose_rate':
        await message.answer('Выберите дату выхода', reply_markup=kb.choose_year_kb)
        await states.Filter_Menu.choose_year.set()


@dp.message_handler(lambda msg: msg.text in kb.button_search_on_filters.text,
                    state=states.Start_Menu.start_menu)
async def choose_filter_type(message: types.Message):
    await message.answer('Выберите тип', reply_markup=kb.choose_type_kb)
    await states.Choose_Func.search_on_filter.set()


@dp.message_handler(lambda msg: msg.text in [kb.button_type_serial.text, kb.button_type_mfilm.text, kb.button_type_film.text],
                    state=states.Choose_Func.search_on_filter)
async def filter_type(message: types.Message):
    prs.filters_content['type'] = message.text
    await message.answer('Выберите жанр', reply_markup=kb.choose_genre_kb)
    await states.Filter_Menu.choose_genre.set()


@dp.message_handler(lambda msg: msg.text in kb.genres.keys(), state=states.Filter_Menu.choose_genre)
async def choose_filter_genre(message: types.Message):
    prs.filters_content['genre'] = kb.genres[message.text]
    await message.answer('Выберите дату выхода', reply_markup=kb.choose_year_kb)
    await states.Filter_Menu.choose_year.set()

@dp.message_handler(lambda msg: msg.text in kb.years, state=states.Filter_Menu.choose_year)
async def choose_filter_year(message: types.Message):
    prs.filters_content['year'] = message.text
    await message.answer('Выберите порог рейтинга фильма', reply_markup=kb.choose_rate_kb)
    await states.Filter_Menu.choose_rate.set()

@dp.message_handler(lambda msg: msg.text in kb.rates, state=states.Filter_Menu.choose_rate)
async def choose_filter_rate(message: types.Message):
    prs.filters_content['rate'] = message.text
    url = prs.get_url_filter()
    prs.get_urls_from_filter(url)
    film_content = prs.filter_films
    link_kb = types.InlineKeyboardMarkup()
    for i in range(j.film_pos, j.film_pos+5):
        if i < len(film_content['names']):
            link_kb.add(types.InlineKeyboardButton(text=film_content['names'][i], callback_data=film_content['urls'][i]))
        else:
            break
    if len(film_content['names']) > 5:
        link_kb.add(types.InlineKeyboardButton(text='⏩⏩ Далее ⏩⏩', callback_data='next'))
    await message.answer('Фильмы по вашему запросу: Cтраница 1', reply_markup=link_kb)
    await states.Film_Menu.filter_films_ready.set()


@dp.message_handler(lambda msg: msg.text in kb.button_back_to_menu.text, state=[states.Choose_Func.search_film, states.Choose_Func.search_person, states.Film_Menu.film_ready,states.Film_Menu.person_ready,
                                                                                states.Choose_Func.search_on_filter, states.Filter_Menu.choose_rate,states.Filter_Menu.choose_year,
                                                                                states.Filter_Menu.choose_genre, states.Film_Menu.filter_films_ready])
async def back_to_menu(message: types.Message):
    await message.answer('Подумай над выбором', reply_markup=kb.menu_kb)
    await states.Start_Menu.start_menu.set()

@dp.message_handler(lambda msg: msg.text in kb.button_get_favour.text, state=states.Start_Menu.start_menu)
async def get_favour(message: types.Message):
    user_id = message.from_user.id
    s = '🌟Ваше избранное:🌟\n'
    for row in database.cursor.execute("SELECT DISTINCT film FROM favour_films WHERE id = ?", (user_id,)):
        s +=str(row)[2:-3].replace('\\xa0', ' ')+'\n'
    await bot.send_message(message.from_user.id, s)
    database.conn.commit()



@dp.message_handler(lambda msg: msg.text in kb.button_add_to_favor.text, state=[states.Film_Menu.film_ready,
                                                                                states.Film_Menu.person_ready,
                                                                                states.Film_Menu.filter_films_ready])
async def add_to_favor(message: types.Message):
    await message.answer('Добавлено в избранное !')
    user_id = message.from_user.id
    film = prs.films_content['name']
    params = (user_id, film)
    database.cursor.execute("INSERT INTO favour_films VALUES (?, ?)", params)
    database.conn.commit()


@dp.message_handler(state=states.Choose_Func.search_film)
async def searching_film(message: types.Message):
    film_name = message.text
    film = prs.search_film(film_name)
    caption = get_film_caption(film)
    await message.reply_photo(film['poster'], caption=caption, parse_mode=types.ParseMode.HTML, reply_markup=kb.search_film_menu_kb)
    await states.Film_Menu.film_ready.set()


@dp.message_handler(state=states.Choose_Func.search_person)
async def searching_person(message: types.Message):
    person_name = message.text
    person = prs.seacrh_person(person_name)
    link_kb = types.InlineKeyboardMarkup()
    for i in range(3):
        if i < len(person['best_films_names']):
            link_kb.add(
                types.InlineKeyboardButton(text=person['best_films_names'][i], callback_data=person['best_films_urls'][i]))
        else:
            break
    caption = get_person_caption(person)
    await message.reply_photo(person['photo'], caption=caption, parse_mode=types.ParseMode.HTML, reply_markup=link_kb)
    await states.Film_Menu.person_ready.set()


@dp.message_handler(lambda msg: msg.text in kb.button_back_to_search_film.text, state=states.Film_Menu.film_ready)
async def re_searching_film(message: types.Message):
    await message.answer('Введите название фильма, но сначала хорошо подумайте !')
    await states.Choose_Func.search_film.set()


@dp.message_handler(lambda msg: msg.text in kb.button_back_to_search_person.text, state=states.Film_Menu.person_ready)
async def re_searching_film(message: types.Message):
    await message.answer('Введите имя персоны, но сначала хорошо подумайте !')
    await states.Choose_Func.search_person.set()
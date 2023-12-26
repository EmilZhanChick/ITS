from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import random

# Подключение Базы Данных относительно mainBot.py
import os
import sqlite3;
current_directory = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(current_directory, 'myDB.db')
con = sqlite3.connect(database_path)
cursor = con.cursor()

# Инициализация dotenv (секретные переменные)
from dotenv import load_dotenv
load_dotenv()

# Инициализация бота и диспетчера
import logging
logging.basicConfig(level=logging.INFO)
bot = Bot(token=os.getenv('TOKEN'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Обработчик команды /id
@dp.message_handler(commands=['id'])
async def id__(message: types.Message):
    await message.answer('Твой user_id: ' + str(message.from_user.id))

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def choice_lang(message: types.Message):
    try:                   # Добавление нового User_id в базу данных
        cursor.execute("INSERT INTO users (user_id) VALUES (?)", (message.from_user.id,))
        con.commit()
    except Exception as e:
        None
    button = ['Русский язык', 'Қазақ тілі']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*button)
    await message.answer('Выберете язык/Тілді таңдаңыз:', reply_markup=keyboard)

# Обработчик команды /admin
@dp.message_handler(commands=['admin'])
async def admin_func(message: types.Message):
    for admink in menu.admins_id:
        if admink[0] == str(message.from_user.id):
            admink[1] = 1
            await admin.admin_menu(message)

# Обработчик кнопок админа
@dp.callback_query_handler()
async def callback_handlers(callback: types.callback_query):
    for admink in menu.admins_id:
        if admink[0] == str(callback.from_user.id) and admink[1] == 1:
            await admin._callback(callback)
            break

################################################################## Русский язык #############################################################################
@dp.message_handler(content_types='text')
async def menu_rus(message: types.Message):
    await menu.UpdateCourses()
    await menu.UpdateCourses_KZ()
    
    is_admin = False
    for admink in menu.admins_id:
        if admink[0] == str(message.from_user.id) and admink[1] == 1:
            is_admin = True
            await admin.admin_(message)
            break
    if not is_admin:
        match message.text:
            case 'Русский язык':
                await message.answer('Добро пожаловать в нашего телеграм бота!', reply_markup=menu.main_menu)

            case 'Моя мотивация дня🤙':
                cursor.execute("SELECT * FROM Motivation")
                text = random.choice(cursor.fetchall())
                await message.answer(text[1]) # Выводим случайную мотивацию из БД

            case 'Где мы находимся🌏':
                # Отправляем фотографию пользователю
                photo_path = os.path.join(current_directory, 'photo/adress.jpg')
                with open(photo_path, 'rb') as photo:
                    await bot.send_photo(chat_id=message.chat.id, photo=photo)
                # Выводим текст про адрес из БД
                cursor.execute("SELECT * FROM TextRus WHERE id=1")
                for TextRus in cursor.fetchall(): 
                    Text = TextRus[1]
                await message.reply(Text, reply_markup=menu.keyboard_Address) 

            case 'О нас👥':
                cursor.execute("SELECT * FROM TextRus WHERE id=3")
                for TextRus in cursor.fetchall(): 
                    Text = TextRus[1]
                await message.reply(Text) # Выводим текст о нас из БД

            case 'Наши контакты📱':
                cursor.execute("SELECT * FROM TextRus WHERE id=2")
                for TextRus in cursor.fetchall(): 
                    Text = TextRus[1]
                await message.answer(Text, reply_markup=menu.keyboard_contact)  # Выводим текст про контакты из БД
                
            case 'Подать заявку на курс📝':
                cursor.execute("SELECT * FROM TextRus WHERE id=4")
                for TextRus in cursor.fetchall(): 
                    Text = TextRus[1]
                await message.answer(Text, reply_markup=menu.keyboard_Application) # Выводим текст про заявку из БД

            case 'Наши курсы🖥️':
                await message.answer('У нас имеются активные курсы, на которые принимаются заявки, а также завершенные курсы, на которые в настоящий момент не проводится набор.'
                                        , reply_markup=menu.keyboard_active) # Выводим меню Активные и Завершенные курсы

            case 'Активные курсы':
                await message.answer('Выберите интересующий вас курс, чтобы получить описание.'
                                        , reply_markup=menu.keyboard_courses)  # Выводим меню активыных курсов
            case 'Завершенные курсы':
                await message.answer('Выберите интересующий вас курс, чтобы получить описание.'
                                        , reply_markup=menu.keyboard_courses_ended)  # Выводим меню завершенных курсов

            case 'Назад':
                await message.answer('Вы вернулись в главное меню', reply_markup=menu.main_menu) # возвращаем главное меню

            case 'Перейти на казахский👩‍🏫': 
                await message.answer('Сіз боттың тілін қазақ тіліне өзгерттіңіз.', reply_markup=menu.main_menu_KZ)

    ################################################################## Қазақ тілі #############################################################################
            case 'Қазақ тілі':
                await message.answer('Біздің бот жеделхатымызға қош келдіңіз!', reply_markup=menu.main_menu_KZ)

            case 'Бүгінгі мотивациям🤙':
                cursor.execute("SELECT * FROM Motivation")
                text = random.choice(cursor.fetchall())
                await message.answer(text[2]) # Выводим случайную мотивацию из БД

            case 'Біз қайдамыз🌏':
                # Отправляем фотографию пользователю
                photo_path = os.path.join(current_directory, 'photo/adress.jpg')
                with open(photo_path, 'rb') as photo:
                    await bot.send_photo(chat_id=message.chat.id, photo=photo)

                cursor.execute("SELECT * FROM TextRus WHERE id=1")
                for TextRus in cursor.fetchall(): 
                    Text = TextRus[2]
                await message.reply(Text, reply_markup=menu.keyboard_Address_KZ) # Выводим текст про адрес из БД

            case 'Біз туралы👥':
                cursor.execute("SELECT * FROM TextRus WHERE id=3")
                for TextRus in cursor.fetchall(): 
                    Text = TextRus[2]
                await message.reply(Text) # Выводим текст о нас из БД

            case 'Біздің байланыстар📱':
                cursor.execute("SELECT * FROM TextRus WHERE id=2")
                for TextRus in cursor.fetchall(): 
                    Text = TextRus[2]
                await message.answer(Text, reply_markup=menu.keyboard_contact)  # Выводим текст про контакты из БД
                
            case 'Курсқа өтініш беру📝':
                cursor.execute("SELECT * FROM TextRus WHERE id=4")
                for TextRus in cursor.fetchall(): 
                    Text = TextRus[2]
                await message.answer(Text, reply_markup=menu.keyboard_Application_KZ) # Выводим текст про заявку из БД

            case 'Біздің курстар🖥️':
                await message.answer('Бізде өтінімдер қабылданатын белсенді курстар, сондай-ақ қазіргі уақытта қабылдау жүргізілмейтін аяқталған курстар бар.'
                                        , reply_markup=menu.keyboard_active_KZ) # Выводим меню Активные и Завершенные курсы

            case 'Белсенді курстар':
                await message.answer('Сипаттама алу үшін сізді қызықтыратын курсты таңдаңыз.'
                                        , reply_markup=menu.keyboard_courses_KZ)  # Выводим меню активыных курсов
            case 'Аяқталған курстар':
                await message.answer('Сипаттама алу үшін сізді қызықтыратын курсты таңдаңыз.'
                                        , reply_markup=menu.keyboard_courses_ended_KZ)  # Выводим меню завершенных курсов

            case 'Артқа':
                await message.answer('Сіз Негізгі мәзірге оралдыңыз', reply_markup=menu.main_menu_KZ) # возвращаем главное меню

            case 'Орыс тіліне өтіңіз👩‍🏫': 
                await message.answer('Вы сменили язык бота на русский.', reply_markup=menu.main_menu)

            case _:     
                Link = ''
                Discription = ''
                try:
                    cursor.execute("SELECT * FROM Courses WHERE Course=?", (message.text,))
                    for Course in cursor.fetchall():
                        Discription = Course[2]
                        Link = Course[3]
                    Link_button = types.InlineKeyboardButton('Подробнее о курсе', web_app = types.WebAppInfo(url=Link))
                    keyboard_Link = types.InlineKeyboardMarkup(row_width=1).add(Link_button)
                    await message.answer(Discription, reply_markup=keyboard_Link)
                except Exception as e:
                    try:
                        cursor.execute("SELECT * FROM Courses WHERE CourseKZ=?", (message.text,))
                        for Course in cursor.fetchall():
                            Discription = Course[5]
                            Link = Course[6]
                        Link_button = types.InlineKeyboardButton('Курс туралы толығырақ', web_app = types.WebAppInfo(url=Link))
                        keyboard_Link = types.InlineKeyboardMarkup(row_width=1).add(Link_button)
                        await message.answer(Discription, reply_markup=keyboard_Link)
                    except Exception as e:
                        await message.answer('Простите я не понял вашего запроса. \nКешіріңіз, мен Сіздің өтінішіңізді түсінбедім.')

# Запуск бота
if __name__ == '__main__':
    import admin
    import menu
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
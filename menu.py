from mainBot import *

admin_ids = os.getenv('ADMIN_ID').split(', ')
admins_id = [[admin_id, 0] for admin_id in admin_ids]

Site = types.InlineKeyboardButton('Наш сайт', web_app = types.WebAppInfo(url='https://itschool.tou.edu.kz/'))
Insta = types.InlineKeyboardButton('Instagram', url='https://instagram.com/itschool.tou?utm_medium=copy_link')
TikTok = types.InlineKeyboardButton('TikTok', url='https://www.tiktok.com/@itgrouptou')
YouTube = types.InlineKeyboardButton('YouTube', url='https://www.youtube.com/channel/UCEGZEuaQro5WCc50gDU5JOA/about')
keyboard_contact = types.InlineKeyboardMarkup(row_width=1).add(YouTube, Insta, TikTok, Site)

################################################################## Русский язык #############################################################################
                # Главное меню
button_RU = [
        'Моя мотивация дня🤙', 'Перейти на казахский👩‍🏫', 'Наши курсы🖥️',
        'Где мы находимся🌏', 'О нас👥', 'Наши контакты📱',
        'Подать заявку на курс📝'
        ]
main_menu = types.ReplyKeyboardMarkup(resize_keyboard=False).add(*button_RU)
button_RU = ['Активные курсы', 'Завершенные курсы']
keyboard_active = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*button_RU)
button_RU = types.InlineKeyboardButton('Посмотреть на карте', url='https://2gis.kz/pavlodar/firm/70000001057702006?m=76.966304%2C52.267353%2F16')
keyboard_Address = types.InlineKeyboardMarkup().add(button_RU)
button_RU = types.InlineKeyboardButton('Оставить заявку', web_app = types.WebAppInfo(url='https://itschool.tou.edu.kz/'))
keyboard_Application = types.InlineKeyboardMarkup(row_width=1).add(button_RU)

                # Меню курсов
keyboard_courses_all = types.ReplyKeyboardMarkup(resize_keyboard=False)
keyboard_courses = types.ReplyKeyboardMarkup(resize_keyboard=False)
keyboard_courses_ended = types.ReplyKeyboardMarkup(resize_keyboard=False)
        #   ФУНКЦИЯ ОБНОВЛЕНИЕ БАЗЫ ДАННЫХ КУРСОВ
async def UpdateCourses():
    global keyboard_courses, keyboard_courses_ended, keyboard_courses_all
    back = types.KeyboardButton('Назад')
    buttonsAct = []
    buttonsEnd = []
    cursor.execute("SELECT * FROM Courses")
    for Courses in cursor.fetchall():
        button = types.KeyboardButton(Courses[1])
        if Courses[7] == 1:
            buttonsAct.append(button)
        elif Courses[7] == 0:
            buttonsEnd.append(button)
    keyboard_courses = types.ReplyKeyboardMarkup(resize_keyboard=False)
    keyboard_courses.add(*buttonsAct).add(back)
    
    keyboard_courses_ended = types.ReplyKeyboardMarkup(resize_keyboard=False)
    keyboard_courses_ended.add(*buttonsEnd).add(back)

    keyboard_courses_all = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard_courses_all.add(*buttonsAct).add(*buttonsEnd).add(back)

################################################################## Қазақ тілі #############################################################################
                    # Главное меню KAZ
button_KZ = [
        'Бүгінгі мотивациям🤙', 'Орыс тіліне өтіңіз👩‍🏫', 'Біздің курстар🖥️',
        'Біз қайдамыз🌏', 'Біз туралы👥', 'Біздің байланыстар📱',
        'Курсқа өтініш беру📝'
        ]
main_menu_KZ = types.ReplyKeyboardMarkup(resize_keyboard=False).add(*button_KZ)
button_KZ = ['Белсенді курстар', 'Аяқталған курстар']
keyboard_active_KZ = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*button_KZ)
button_KZ = types.InlineKeyboardButton('Картадан қараңыз', url='https://2gis.kz/pavlodar/firm/70000001057702006?m=76.966304%2C52.267353%2F16')
keyboard_Address_KZ = types.InlineKeyboardMarkup().add(button_KZ)
button_KZ = types.InlineKeyboardButton('Өтініш қалдыру', web_app = types.WebAppInfo(url='https://itschool.tou.edu.kz/'))
keyboard_Application_KZ = types.InlineKeyboardMarkup(row_width=1).add(button_KZ)

                    # Меню курсов KAZ
keyboard_courses_KZ = types.ReplyKeyboardMarkup(resize_keyboard=False)
keyboard_courses_ended_KZ = types.ReplyKeyboardMarkup(resize_keyboard=False)
            #   ФУНКЦИЯ ОБНОВЛЕНИЕ БАЗЫ ДАННЫХ КУРСОВ
async def UpdateCourses_KZ():
    back = types.KeyboardButton('Артқа')
    buttonsAct = []
    buttonsEnd = []
    cursor.execute("SELECT * FROM Courses")
    for Courses in cursor.fetchall():
        button = types.KeyboardButton(Courses[4])
        if Courses[7] == 1:
            buttonsAct.append(button)
        elif Courses[7] == 0:
            buttonsEnd.append(button)
    global keyboard_courses_KZ
    keyboard_courses_KZ = types.ReplyKeyboardMarkup(resize_keyboard=False)
    keyboard_courses_KZ.add(*buttonsAct).add(back)

    global keyboard_courses_ended_KZ
    keyboard_courses_ended_KZ = types.ReplyKeyboardMarkup(resize_keyboard=False)
    keyboard_courses_ended_KZ.add(*buttonsEnd).add(back)
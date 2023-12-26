from mainBot import *
import menu

removal = False # Флаг удаления
activating = False # Флаг Активации
ending = False # Флаг Завершения
addition = False # Флаг Добавления
distribution = False # Флаг Рассылки

# Глобальные переменные
id = 0
name = ''
distribution_text = ''
newCourse = ['']
buttons = ['Курсы', 'Рассылка', 'Выйти с админки']
back = types.KeyboardButton('Назад')  
keyboard_admin_main = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons)

async def admin_menu(message: types.Message): # ФУНКЦИЯ ВЫВОДА ГЛАВНОГО МЕНЮ АДМИНА
    await message.answer('Добро пожаловать в панель администратора', reply_markup=keyboard_admin_main)

                                                # ФУНКЦИЯ ПРОВЕРКИ ВВОДИМОГО ТЕКСТА
async def admin_(message: types.Message):
    global activating, ending, id, addition, removal, newCourse, name, distribution, distribution_text
    match message.text:
        case 'Курсы':                # Выводим меню
            buttons = ['Активировать', 'Добавить', 'Удалить']
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons, back)
            await message.answer('Выбери нужное действие', reply_markup=keyboard)

        case 'Активировать':         # Выводим меню
            buttons = ['Активные курсы', 'Завершенные курсы']
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons, back)
            await message.answer('Выбери нужное действие', reply_markup=keyboard)
        case 'Активные курсы':
                activating = True    # Включаем флаг для дальнейшей проверки и выводим курсы
                await message.answer('Выберите интересующий вас курс'
                                        , reply_markup=menu.keyboard_courses)  
        case 'Завершенные курсы':
                ending = True        # Включаем флаг для дальнейшей проверки и выводим курсы
                await message.answer('Выберите интересующий вас курс'
                                        , reply_markup=menu.keyboard_courses_ended)  

        case 'Добавить': 
            addition = True          # Включаем флаг для дальнейшей проверки и выводим текст
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(back)
            await message.answer("Для добавления курса администратору нужно написать информацию в одной строке, разделяя название, описание и ссылку символом '' _ ''. \n " +
                                "Вот пример: \n<b>Название курса _ Описание курса _ Ссылка на курс _ Название курсаKZ _ Описание курсаKZ _ Ссылка на курсKZ</b> \nссылка обязательно должна быть https://", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)

        case 'Удалить':
            removal = True           # Включаем флаг для дальнейшей проверки и выводим текст
            await message.answer('Выберите курс который хотите удалить', reply_markup=menu.keyboard_courses_all)

        case 'Рассылка':
            distribution = True      # Включаем флаг для дальнейшей проверки и выводим курсы
            await message.answer('Введите текст или ссылку которую хотите разослать всем:')

        case 'Выйти с админки':      # Выходим с админки, выключаем админ панель у админ id
            for admink in menu.admins_id:
                if admink[0] == str(message.from_user.id):
                    admink[1] = 0
            await message.answer('Вы вышли из панели администратора!', reply_markup=menu.main_menu)

        case 'Назад':
                                       # Завершение всех действий и вовращение в админ панель
            removal = activating = ending = addition = distribution = False
            await message.answer('Вы вернулись в меню', reply_markup=keyboard_admin_main)

        case _:                    # ПРОВЕРКА ФЛАГОВ И ВВОДИМОГО ТЕКСТА ДЛЯ ИХ ОБРАБОТКИ ЧЕРЕЗ БАЗУ ДАННЫХ
            try:
                cursor.execute("SELECT * FROM Courses WHERE Course=?", (message.text,))
                for Course in cursor.fetchall():
                    id = Course[0]
                    name = Course[1]
                
                if activating:                     # Подтверждение активации
                    button_ikb = types.InlineKeyboardButton('Завершить курс', callback_data='END')
                    keyboard_ = types.InlineKeyboardMarkup(row_width=1).add(button_ikb)
                    await message.answer('Завершить курс?:\n'+name+'?', reply_markup=keyboard_)
                elif ending:                       # Подтверждение звершения
                    button_ikb = types.InlineKeyboardButton('Начать курс', callback_data='RISE')
                    keyboard_ = types.InlineKeyboardMarkup(row_width=1).add(button_ikb)
                    await message.answer('Активировать курс?:\n'+name+'?', reply_markup=keyboard_)

                elif addition:
                    global newCourse
                    newCourse = message.text.split(' _ ') # Делим текст на массив значений курса
                                                    # Выводим пример готового курса на русском
                    button_ikb = types.InlineKeyboardButton('Подробнее о курсе', web_app = types.WebAppInfo(url=newCourse[2]))
                    keyboard_ = types.InlineKeyboardMarkup(row_width=1).add(button_ikb)
                    await message.answer(newCourse[0] + "\n\n" + newCourse[1] , reply_markup=keyboard_)
                                                    # Выводим пример готового курса на казахском
                    button_ikb = types.InlineKeyboardButton('Подробнее о курсе', web_app = types.WebAppInfo(url=newCourse[5]))
                    keyboard_ = types.InlineKeyboardMarkup(row_width=1).add(button_ikb)
                    await message.answer(newCourse[3] + "\n\n" + newCourse[4] , reply_markup=keyboard_)
                                                    # Выводим подтверждение добавления курса
                    button_ikb = types.InlineKeyboardButton('ДА', callback_data='ADD')
                    button_ikb_2 = types.InlineKeyboardButton('НЕТ', callback_data='ADD_rem')
                    keyboard_ = types.InlineKeyboardMarkup(row_width=1).add(button_ikb).add(button_ikb_2)
                    await message.answer('Всё верно?\n', reply_markup=keyboard_)

                elif removal:                       # Подтверждение удаления
                    button_ikb = types.InlineKeyboardButton('Да, удалить', callback_data='REM')
                    keyboard_ = types.InlineKeyboardMarkup(row_width=1).add(button_ikb)
                    await message.answer('Желаете удалить курс:\n'+name+'?', reply_markup=keyboard_)
                    removal = False

                elif distribution:                  # Подтверждение рассылки
                    distribution_text = message.text
                    button_ikb = types.InlineKeyboardButton('Выполнить рассылку', callback_data='DIST')
                    button_ikb_2 = types.InlineKeyboardButton('Отменить', callback_data='DIST_off')
                    keyboard_ = types.InlineKeyboardMarkup(row_width=1).add(button_ikb).add(button_ikb_2)
                    await message.answer("Подтвердить рассылку?\n\n" + distribution_text, reply_markup=keyboard_)
            except Exception as e:
                print(e)
                print(message.from_user.first_name +": "+ message.text)
                await message.answer("Я не понял вашего запроса.")
                
                                            # ФУНКЦИЯ ОБРАБОТКИ CALLBACK КНОПОК
async def _callback(callback: types.CallbackQuery) -> None:
    match callback.data:
        case 'END':
            await callback.answer('Курс завершен.')
            cursor.execute('UPDATE Courses SET active=0 WHERE id=?', (id,))
            con.commit()
        case 'RISE':
            await callback.answer('Курс активирован!')
            cursor.execute('UPDATE Courses SET active=1 WHERE id=?', (id,))
            con.commit()
        case 'REM':
            await callback.answer('Курс удален!')
            cursor.execute("DELETE FROM Courses WHERE id=?", (id,))
            con.commit()
        case 'ADD':
                                                        # Создаем SQL-запрос и добавляем новый курс в базу данных
            sql_query = "INSERT INTO Courses (Course, Description, link, CourseKZ, DescriptionKZ, linkKZ, active) VALUES (?, ?, ?, ?, ?, ?, ?)"
            cursor.execute(sql_query, (newCourse[0], newCourse[1], newCourse[2], newCourse[3], newCourse[4], newCourse[5], 1))
            con.commit()
            await callback.answer('Курс добавлен!')
            global addition
            addition = False
        case 'ADD_rem':
            await callback.answer('Попробуйте снова')
        case 'DIST':
                                    # Делаем рассылку по всем user_id в базе данных
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            await callback.answer('Выполняется....')
            global distribution_text, distribution
            for user in users:
                await bot.send_message(chat_id=user[0], text=distribution_text)
            distribution = False
        case 'DIST_off':
            await callback.answer('Отмена рассылки')
            distribution = False
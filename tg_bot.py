import telebot, json, random
from timeit import default_timer as timer
from telebot import types
import time

bot = telebot.TeleBot('5717225187:AAETRHVezKSEhSfrU0KzT-KGSk_YNIMhbrQ')
r=0
i=1
k=1
sign = 0

ids = []

#Перевод float во время
def time_result(k):
    hour= k // 3600 #hour
    k -= hour * 3600
    minut = int(k // 60) #minutes
    k -= 60*minut
    # second = round(float(k),2) #seconds
    second = int(k) #second
    return f'{str(minut)} мин, {str(second)} сек'

#При комадне /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Погнали!")
    btn2 = types.KeyboardButton("Расскажи побольше о себе")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id,
                     text=f"Привет, @{message.from_user.first_name}, меня зовут Гиро, и я постараюсь помочь тебе подготовится к экзамену по математике, погнали!?".format(
                         message.from_user), reply_markup=markup)
#########################################

@bot.message_handler(commands=['result'])
def al_result(message):
    def fun(x):
        s = ""
        for j in x.keys():
            s += f"{j}:{x[j]} "
        return s
    m = list(map(fun, ids))
    s = "\n".join(m)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Погнали!")
    markup.add(btn1)
    bot.send_message(message.chat.id, f'{s}', reply_markup=markup)

@bot.message_handler(content_types=["text"])
#Выбор режима
def get_go(message):
    id = message.from_user.id
    if message.text=="Погнали!":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("1")
        btn2 = types.KeyboardButton("2")
        btn3 = types.KeyboardButton("3")
        btn4 = types.KeyboardButton("4")
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id,
                         text=f"Выбери режим: \n"
                              f"1.Тест \n "
                              f"2.Задачи по номеру \n "
                              f"3.Отрешать первую часть ЕГЭ \n "
                              f"4.Задачи на определенную тему"
                              f"".format(
                             message.from_user), reply_markup=markup)
        bot.register_next_step_handler(message, choose);
    elif message.text=='Расскажи побольше о себе':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Погнали!")
        markup.add(btn1)
        bot.send_message(message.chat.id,
                         text=f"Как я уже говорил, меня зовут Гиро, я хочу помочь тебе подготовится к экзамену "
                              f"с помощью отрешивания задач первой части профильного ЕГЭ по математике, "
                              f"я могу предложить 4 интересных режима, которые надеюсь смогут помочь тебе стать "
                              f"увереннее в своем отрешивании 1 части"
                              f"".format(
                             message.from_user), reply_markup=markup)
        bot.register_next_step_handler(message, get_go)

#########################################

def choose(message):

#Первый режим "Тест"

    if message.text == "1":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Старт")
        btn2 = types.KeyboardButton("Вернуться назад")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, text='В этом режиме тебе предстоит на вермя решить 11 задач из ЕГЭ по '
                                               'математике на время, постарайся сделать их правильно и как можно '
                                               'быстрее.\n\n '
                                               'Когда будешь готов, намжи кнопку старт',reply_markup=markup)
        bot.register_next_step_handler(message, ans_ntv)
#########################################

    elif message.text == "2":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("1")
        btn2 = types.KeyboardButton("2")
        btn3 = types.KeyboardButton("3")
        btn4 = types.KeyboardButton("4")
        btn5 = types.KeyboardButton("5")
        btn6 = types.KeyboardButton("6")
        btn7 = types.KeyboardButton("7")
        btn8 = types.KeyboardButton("8")
        btn9 = types.KeyboardButton("9")
        btn10 = types.KeyboardButton("10")
        btn11 = types.KeyboardButton("11")
        btn12 = types.KeyboardButton("Вернуться назад")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11, btn12)
        bot.send_message(message.chat.id, text='В этом режиме ты можешь выбрать номер, из которого хочешь решать '
                                               'задачи, и отрешивать только их.\n\n '
                                               'Выбери тип задания.', reply_markup=markup)
        bot.register_next_step_handler(message, queestion_tip)

    elif message.text == "3":
        pass
        #btn2 = types.KeyboardButton("Вернуться назад")

#Четврёртный режим "Задачи на определенную тему"

    elif message.text == "4":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Алгебра")
        btn2 = types.KeyboardButton("Геометрия")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id,
                         text=f"Из какого раздела ты хочешь решать задачи".format(
                             message.from_user), reply_markup=markup)
        bot.register_next_step_handler(message, alg_topic)

#########################################


#Функция с заданиями для режима 1 "Тест"
@bot.message_handler(content_types=['text'])
def ans_ntv(message):
    global start
    global i
    global sign

    if message.text == "Старт":
        # i+=1
        folder_number = random.randint(1, 3)
        start = timer()
        sign=1

        #из папки с типом задания i беру рандомную папку и из нее картинку
        picture_path = f'folders{str(i)}/{folder_number}/picture.jpg'
        print(picture_path)

        #открываю картинку
        bot.send_photo(message.chat.id, open(picture_path, 'rb'))

        #и в этой же папки читаю txt файл
        with open(f'folders{str(i)}/{folder_number}/answer.txt', 'r') as f:
            answer = f.read()

        bot.send_message(message.chat.id, 'Введите ваш ответ:')
        bot.register_next_step_handler(message, check_answer, answer)

    elif message.text == "Вернуться назад":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("1")
        btn2 = types.KeyboardButton("2")
        btn3 = types.KeyboardButton("3")
        btn4 = types.KeyboardButton("4")
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id,
                         text=f"Выбери режим: \n"
                              f"1.Тест \n "
                              f"2.Задачи по номеру \n "
                              f"3.Отрешать первую часть ЕГЭ \n "
                              f"4.Задачи на определенную тему"
                              f"".format(
                             message.from_user), reply_markup=markup)
        bot.register_next_step_handler(message, choose)

    else:
        bot.send_message(message.chat.id, text='Тут такого варианта нет'.format(message.from_user))
        bot.register_next_step_handler(message, ans_ntv)

#Проверка ответа
def check_answer(message, answer):
    global i
    global r
    global timer
    global sign

    if i <= 10 and message.text == answer and sign==1:
        bot.send_message(message.chat.id, 'Ваш ответ правильный!')
        i += 1
        r += 1
        folder_number = random.randint(1, 3)

        picture_path = f'folders{str(i)}/{folder_number}/picture.jpg'
        print(picture_path)

        bot.send_photo(message.chat.id, open(picture_path, 'rb'))
        with open(f'folders{str(i)}/{folder_number}/answer.txt', 'r') as f:
            answer = f.read()

        bot.send_message(message.chat.id, 'Введите ваш ответ:')
        bot.register_next_step_handler(message, check_answer, answer)

    elif i <= 10 and message.text != answer and sign==1:
        bot.send_message(message.chat.id, 'Ваш ответ неправильный!')
        i += 1

        folder_number = random.randint(1, 3)

        picture_path = f'folders{str(i)}/{folder_number}/picture.jpg'
        print(picture_path)

        bot.send_photo(message.chat.id, open(picture_path, 'rb'))
        with open(f'folders{str(i)}/{folder_number}/answer.txt', 'r') as f:
            answer = f.read()

        bot.send_message(message.chat.id, 'Введите ваш ответ:')
        bot.register_next_step_handler(message, check_answer, answer)

    elif i >= 11:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Погнали!")
        markup.add(btn1)
        end = timer()
        all_time = round(float(end - start), 2)
        print(time_result(all_time))
        rights=" "+str(r)
        time = ' '+str(time_result(all_time))
        bot.send_message(message.chat.id, f"Ты закончил, у тебя {r} правильных ответов из 11.Ты затратил "
                                          f"{time_result(all_time)}\n\n"
                                          f"Хочешь ещё позаниматься?".format(
                             message.from_user), reply_markup=markup)
        ids.append({'Время':time, '  Правильных ответов':rights})
        print(ids)
        bot.register_next_step_handler(message, get_go)
        r = 0
        i = 1
        k = 1
        return

#Функция с заданиями для режима 2 "Задачи по номеру"
def queestion_tip(message):
    global start
    global i
    global r
    # i = 1
    if message.text == "1":
        # i+=1
        folder_number = random.randint(1, 3)
        start = timer()

        #из папки с типом задания i беру рандомную папку и из нее картинку
        picture_path = f'folders{str(i)}/{folder_number}/picture.jpg'
        print(picture_path)

        #открываю картинку
        bot.send_photo(message.chat.id, open(picture_path, 'rb'))

        #и в этой же папки читаю txt файл
        with open(f'folders{str(i)}/{folder_number}/answer.txt', 'r') as f:
            answer = f.read()

        bot.send_message(message.chat.id, 'Введите ваш ответ:')
        bot.register_next_step_handler(message, check_answer_tip, answer)

    elif message.text == "2":
        i+=1
        folder_number = random.randint(1, 3)
        start = timer()

        #из папки с типом задания i беру рандомную папку и из нее картинку
        picture_path = f'folders{str(i)}/{folder_number}/picture.jpg'
        print(picture_path)

        #открываю картинку
        bot.send_photo(message.chat.id, open(picture_path, 'rb'))

        #и в этой же папки читаю txt файл
        with open(f'folders{str(i)}/{folder_number}/answer.txt', 'r') as f:
            answer = f.read()

        bot.send_message(message.chat.id, 'Введите ваш ответ:')
        bot.register_next_step_handler(message, check_answer_tip, answer)

    elif message.text == "3":
        i+=2
        folder_number = random.randint(1, 3)
        start = timer()

        #из папки с типом задания i беру рандомную папку и из нее картинку
        picture_path = f'folders{str(i)}/{folder_number}/picture.jpg'
        print(picture_path)

        #открываю картинку
        bot.send_photo(message.chat.id, open(picture_path, 'rb'))

        #и в этой же папки читаю txt файл
        with open(f'folders{str(i)}/{folder_number}/answer.txt', 'r') as f:
            answer = f.read()

        bot.send_message(message.chat.id, 'Введите ваш ответ:')
        bot.register_next_step_handler(message, check_answer_tip, answer)

    elif message.text == "4":
        i+=3
        folder_number = random.randint(1, 3)
        start = timer()

        #из папки с типом задания i беру рандомную папку и из нее картинку
        picture_path = f'folders{str(i)}/{folder_number}/picture.jpg'
        print(picture_path)

        #открываю картинку
        bot.send_photo(message.chat.id, open(picture_path, 'rb'))

        #и в этой же папки читаю txt файл
        with open(f'folders{str(i)}/{folder_number}/answer.txt', 'r') as f:
            answer = f.read()

        bot.send_message(message.chat.id, 'Введите ваш ответ:')
        bot.register_next_step_handler(message, check_answer_tip, answer)

    elif message.text == "5":
        i+=4
        folder_number = random.randint(1, 3)
        start = timer()

        #из папки с типом задания i беру рандомную папку и из нее картинку
        picture_path = f'folders{str(i)}/{folder_number}/picture.jpg'
        print(picture_path)

        #открываю картинку
        bot.send_photo(message.chat.id, open(picture_path, 'rb'))

        #и в этой же папки читаю txt файл
        with open(f'folders{str(i)}/{folder_number}/answer.txt', 'r') as f:
            answer = f.read()

        bot.send_message(message.chat.id, 'Введите ваш ответ:')
        bot.register_next_step_handler(message, check_answer_tip, answer)

    elif message.text == "6":
        i+=5
        folder_number = random.randint(1, 3)
        start = timer()

        #из папки с типом задания i беру рандомную папку и из нее картинку
        picture_path = f'folders{str(i)}/{folder_number}/picture.jpg'
        print(picture_path)

        #открываю картинку
        bot.send_photo(message.chat.id, open(picture_path, 'rb'))

        #и в этой же папки читаю txt файл
        with open(f'folders{str(i)}/{folder_number}/answer.txt', 'r') as f:
            answer = f.read()

        bot.send_message(message.chat.id, 'Введите ваш ответ:')
        bot.register_next_step_handler(message, check_answer_tip, answer)

    elif message.text == "7":
        i+=6
        folder_number = random.randint(1, 3)
        start = timer()

        #из папки с типом задания i беру рандомную папку и из нее картинку
        picture_path = f'folders{str(i)}/{folder_number}/picture.jpg'
        print(picture_path)

        #открываю картинку
        bot.send_photo(message.chat.id, open(picture_path, 'rb'))

        #и в этой же папки читаю txt файл
        with open(f'folders{str(i)}/{folder_number}/answer.txt', 'r') as f:
            answer = f.read()

        bot.send_message(message.chat.id, 'Введите ваш ответ:')
        bot.register_next_step_handler(message, check_answer_tip, answer)

    elif message.text == "8":
        i+=7
        folder_number = random.randint(1, 3)
        start = timer()

        #из папки с типом задания i беру рандомную папку и из нее картинку
        picture_path = f'folders{str(i)}/{folder_number}/picture.jpg'
        print(picture_path)

        #открываю картинку
        bot.send_photo(message.chat.id, open(picture_path, 'rb'))

        #и в этой же папки читаю txt файл
        with open(f'folders{str(i)}/{folder_number}/answer.txt', 'r') as f:
            answer = f.read()

        bot.send_message(message.chat.id, 'Введите ваш ответ:')
        bot.register_next_step_handler(message, check_answer_tip, answer)

    elif message.text == "9":
        i+=8
        folder_number = random.randint(1, 3)
        start = timer()

        #из папки с типом задания i беру рандомную папку и из нее картинку
        picture_path = f'folders{str(i)}/{folder_number}/picture.jpg'
        print(picture_path)

        #открываю картинку
        bot.send_photo(message.chat.id, open(picture_path, 'rb'))

        #и в этой же папки читаю txt файл
        with open(f'folders{str(i)}/{folder_number}/answer.txt', 'r') as f:
            answer = f.read()

        bot.send_message(message.chat.id, 'Введите ваш ответ:')
        bot.register_next_step_handler(message, check_answer_tip, answer)

    elif message.text == "10":
        i+=9
        folder_number = random.randint(1, 3)
        start = timer()

        #из папки с типом задания i беру рандомную папку и из нее картинку
        picture_path = f'folders{str(i)}/{folder_number}/picture.jpg'
        print(picture_path)

        #открываю картинку
        bot.send_photo(message.chat.id, open(picture_path, 'rb'))

        #и в этой же папки читаю txt файл
        with open(f'folders{str(i)}/{folder_number}/answer.txt', 'r') as f:
            answer = f.read()

        bot.send_message(message.chat.id, 'Введите ваш ответ:')
        bot.register_next_step_handler(message, check_answer_tip, answer)

    elif message.text == "11":
        i+=10
        folder_number = random.randint(1, 3)
        start = timer()

        #из папки с типом задания i беру рандомную папку и из нее картинку
        picture_path = f'folders{str(i)}/{folder_number}/picture.jpg'
        print(picture_path)

        #открываю картинку
        bot.send_photo(message.chat.id, open(picture_path, 'rb'))

        #и в этой же папки читаю txt файл
        with open(f'folders{str(i)}/{folder_number}/answer.txt', 'r') as f:
            answer = f.read()

        bot.send_message(message.chat.id, 'Введите ваш ответ:')
        bot.register_next_step_handler(message, check_answer_tip, answer)

    elif message.text == "Вернуться назад":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("1")
        btn2 = types.KeyboardButton("2")
        btn3 = types.KeyboardButton("3")
        btn4 = types.KeyboardButton("4")
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id,
                         text=f"Выбери режим: \n"
                              f"1.Тест \n "
                              f"2.Задачи по номеру \n "
                              f"3.Отрешать первую часть ЕГЭ \n "
                              f"4.Задачи на определенную тему"
                              f"".format(
                             message.from_user), reply_markup=markup)
        bot.register_next_step_handler(message, choose);

def check_answer_tip(message, answer):
    global i
    global r
    global k
    global timer

    if k <= 10 and message.text == answer and message.text != 'Старт':
        bot.send_message(message.chat.id, 'Ваш ответ правильный!')
        r += 1
        k += 1
        folder_number = random.randint(1, 3)

        picture_path = f'folders{str(i)}/{folder_number}/picture.jpg'
        print(picture_path)

        bot.send_photo(message.chat.id, open(picture_path, 'rb'))
        with open(f'folders{str(i)}/{folder_number}/answer.txt', 'r') as f:
            answer = f.read()

        bot.send_message(message.chat.id, 'Введите ваш ответ:')
        bot.register_next_step_handler(message, check_answer_tip, answer)

    elif k <= 10 and message.text != answer and message.text != 'Старт':
        bot.send_message(message.chat.id, 'Ваш ответ неправильный!')
        k += 1
        folder_number = random.randint(1, 3)

        picture_path = f'folders{str(i)}/{folder_number}/picture.jpg'
        print(picture_path)

        bot.send_photo(message.chat.id, open(picture_path, 'rb'))
        with open(f'folders{str(i)}/{folder_number}/answer.txt', 'r') as f:
            answer = f.read()

        bot.send_message(message.chat.id, 'Введите ваш ответ:')
        bot.register_next_step_handler(message, check_answer_tip, answer)

    elif k >= 11:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Погнали!")
        markup.add(btn1)
        end = timer()
        all_time = round(float(end - start), 2)
        print(time_result(all_time))
        bot.send_message(message.chat.id, f"Ты закончил, у тебя {r} правильных ответов из 11.Ты затратил "
                                          f"{time_result(all_time)}\n\n"
                                          f"Хочешь ещё позаниматься?".format(
                             message.from_user), reply_markup=markup)
        r = 0
        i = 1
        k = 1
        bot.register_next_step_handler(message, get_go)
        return

# Если в 4 режима выбрали Алгебру (самого режима пока нет)

def alg_topic(message):
    if message.text == 'Алгебра':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("1")
        btn2 = types.KeyboardButton("2")
        btn3 = types.KeyboardButton("3")
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id,
                         text=f"Выбери тему:\n\n 1.Начала теории вероятностей\n\n 2.Вероятности сложных событий\n\n "
                              f"3.Простейшие уравнения\n\n 4.Вычисления и преобразования\n\n "
                              f"5.Производная и первообразная\n\n 6.Задачи с прикладным содержанием\n\n "
                              f"7.Текстовые задачи\n\n 8.Графики функций\n\n 9.Наибольшее и наименьшее значение "
                              f"функций ".format(
                             message.from_user), reply_markup=markup)


bot.infinity_polling()

if __name__ == '__main__':
    start()

# def ans_ntv(message):
#     global start
#     global i
#     # i=0
#     id = message.from_user.id
#     if message.text == "Старт":
#         numb_q = random.randint(0, 10)
#         id = message.from_user.id
#         ids.update({id:{'r':0,'numb':numb_q}})
#         qestion_img = str(tip1[numb_q]['qestion'] + ".jpg")
#         img = open(qestion_img, "rb")
#         bot.send_photo(message.chat.id, img)
#         i=1
#         start = timer()
#     elif tip1[ids[id]['numb']]['a']==message.text:
#         bot.send_message(message.chat.id,"Молодец, правильно!")
#         i += 1
#         ids[id]['r']+=1
#         ids[id]['numb']=random.randint(0, 10)
#     else:
#         bot.send_message(message.chat.id, "К сожелению ты ошибся(")
#         i += 1
#         ids[id]['numb'] = random.randint(0, 10)
#     if i <= 11 and message.text != 'Старт':
#         ids[id]['numb'] = random.randint(0, 10)
#         qestion_img = str(tip1[ids[id]["numb"]]['qestion'] + ".jpg")
#         img = open(qestion_img, "rb")
#         bot.send_photo(message.chat.id, img)
#     elif i>11:
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         btn1 = types.KeyboardButton("Погнали!")
#         markup.add(btn1)
#         r=ids[id]["r"]
#         end = timer()
#         all_time = round(float(end - start), 2)
#         bot.send_message(message.chat.id,f"Ты закончил, у тебя {r} правильных ответов из 11.Ты затратил "
#                                              f"{time_result(all_time)}\n\n"
#                                              f"Хочешь ещё позаниматься?".format(
#                              message.from_user), reply_markup=markup)
#         bot.register_next_step_handler(message, get_go)
#         return
#     bot.register_next_step_handler(message, ans_ntv)



#########################################

# def queestion_tip(message):
#     global start
#     global i
#     # i=0
#     id = message.from_user.id
#     if message.text == "Старт":
#         i = 1
#         numb_q = random.randint(0, 10)
#         id = message.from_user.id
#         ids.update({id: {'r': 0, 'numb': numb_q}})
#
#         tip_i = 'tip' + str(i)
#         print(tip_i)
#         qestion_img = str(tip1[numb_q]['qestion'] + ".jpg")
#         # qestion_img = str(str(i) + 'tip' + '/' + tip1[numb_q]['qestion'] + ".jpg")
#         img = open(qestion_img, "rb")
#         bot.send_photo(message.chat.id, img)
#         start = timer()
#     elif tip1[ids[id]['numb']]['a'] == message.text:
#         bot.send_message(message.chat.id, "Молодец, правильно!")
#         i += 1
#         ids[id]['r'] += 1
#         ids[id]['numb'] = random.randint(0, 10)
#     else:
#         bot.send_message(message.chat.id, "К сожелению ты ошибся(")
#         i += 1
#         ids[id]['numb'] = random.randint(0, 10)
#     if i <= 11 and message.text != 'Старт':
#         ids[id]['numb'] = random.randint(0, 10)
#         qestion_img = str(tip1[ids[id]["numb"]]['qestion'] + ".jpg")
#         # qestion_img = str(q[ids[id][numb_q]]['qestion'] + ".jpg")
#         img = open(qestion_img, "rb")
#         bot.send_photo(message.chat.id, img)
#     elif i > 11:
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         btn1 = types.KeyboardButton("Погнали!")
#         markup.add(btn1)
#         r = ids[id]["r"]
#         end = timer()
#         all_time = round(float(end - start), 2)
#         bot.send_message(message.chat.id, f"Ты закончил, у тебя {r} правильных ответов из 11.Ты затратил "
#                                           f"{time_result(all_time)}\n\n"
#                                           f"Хочешь ещё позаниматься?".format(
#             message.from_user), reply_markup=markup)
#         bot.register_next_step_handler(message, get_go)
#         return
#     bot.register_next_step_handler(message, ans_ntv)

# def ans_ntv(message):
#     global start
#     global i
#     global numb_q
#     # i=0
#     id = message.from_user.id
#     if message.text == "Старт":
#         numb_q = random.randint(0, 10)
#         id = message.from_user.id
#         ids.update({id:{'r':0,'numb':numb_q}})
#         qestion_img = str(tip1[numb_q]['qestion'] + ".jpg")
#         img = open(qestion_img, "rb")
#         bot.send_photo(message.chat.id, img)
#         i=1
#         start = timer()
#         bot.register_next_step_handler(message, qestion_for_test);
#
# def qestion_for_test(message):
#     global numb_q
#     ans = int(message.text)
#     if tip1[ids[id]['numb']]['a']==ans:
#         bot.send_message(message.chat.id,"Молодец, правильно!")
#         i += 1
#         ids[id]['r']+=1
#         ids[id]['numb']=random.randint(0, 10)
#
#     elif tip1[ids[id]['numb']]['a']!=ans:
#         bot.send_message(message.chat.id, "К сожелению ты ошибся(")
#         i += 1
#         ids[id]['numb'] = random.randint(0, 10)
#     if i <= 11:
#         ids[id]['numb'] = random.randint(0, 10)
#         qestion_img = str(tip1[ids[id]["numb"]]['qestion'] + ".jpg")
#         # qestion_img = str(q[ids[id][numb_q]]['qestion'] + ".jpg")
#         img = open(qestion_img, "rb")
#         bot.send_photo(message.chat.id, img)
#     else:
#         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#         btn1 = types.KeyboardButton("Погнали!")
#         markup.add(btn1)
#         r=ids[id]["r"]
#         end = timer()
#         all_time = round(float(end - start), 2)
#         bot.send_message(message.chat.id,f"Ты закончил, у тебя {r} правильных ответов из 11.Ты затратил "
#                                          f"{time_result(all_time)}\n\n"
#                                          f"Хочешь ещё позаниматься?".format(
#                          message.from_user), reply_markup=markup)
#         bot.register_next_step_handler(message, get_go)
#         return
#     bot.register_next_step_handler(message, ans_ntv)
#########################################
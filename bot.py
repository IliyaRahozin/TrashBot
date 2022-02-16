import telebot
from telebot import types
from bs4 import BeautifulSoup
import requests
from translitua import translit
from fuzzywuzzy import fuzz

bot = telebot.TeleBot('1776075791:AAFTE2iNu2aMvfM83q37uNK55TiVI64lmmk')


def map(message):
    get_message_bot = message.text.strip().lower()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('❓ Як сортувати сміття')
    btn2 = types.KeyboardButton('❓ Що куди класти')
    btn3 = types.KeyboardButton('🚩 Місця сортування')
    btn4 = types.KeyboardButton('📃 Інформація')
    markup.add(btn1, btn2, btn3, btn4)

    if get_message_bot == "🔙 повернутися":
        bot.send_message(message.chat.id, "Оберіть потрібний пункт меню", parse_mode='html', reply_markup=markup)

    else:
        url = 'https://www.epochtimes.com.ua/maps/recycle/kyiv.php'
        responce = requests.get(url).content
        soup = BeautifulSoup(responce, 'lxml')

        blocks = soup.find_all(class_ = "menu_itemm city not_chosed")
        links = ['kyiv.php']
        for block in blocks:
            links.append(block.get("link"))
        
        trslt=translit(get_message_bot).lower().replace(" ", "-")
        city = links[0]
        for i in range(1, len(links)):
            if fuzz.ratio(trslt, links[i].replace('.php', '')) > fuzz.ratio(trslt, city.replace('.php', '')):
                city = links[i]

        if fuzz.ratio(trslt, city.replace('.php', '')) >= 85:
            final_message = 'Посилання на карту: https://www.epochtimes.com.ua/maps/recycle/' + city
        else:
            final_message = "Даних про введене місто немає на карті 😢"
    
        bot.send_message(message.chat.id, final_message, parse_mode='html', reply_markup=markup)

def garbageSorting(message):
    get_message_bot = message.text.strip().lower()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('❓ Як сортувати сміття')
    btn2 = types.KeyboardButton('❓ Що куди класти')
    btn3 = types.KeyboardButton('🚩 Місця сортування')
    btn4 = types.KeyboardButton('📃 Інформація')
    markup.add(btn1, btn2, btn3, btn4)
         
    if get_message_bot == "📄 папір":
        final_message = """<b>✔ Можна класти:</b>
    - газети, каталоги, журнали, рекламні проспекти;
    - зошити, чистий та використаний папір для нотаток та малювання;
    - конверти, книжки без твердої обкладинки;
    - картонні ящики та коробки, паперові пакети та паперову тару.

<b>❌ Не можна класти:</b>
    - вологий папір та картон;
    - використаний паперовий посуд;
    - картонну тару для напоїв, плівку;
    - фольгу та копіювальний папір.
"""
    
    elif get_message_bot == "🔍 скло":
        final_message = """<b>✔ Можна:</b>
    -Пляшки: від напоїв та пива, вина та шампанського, міцного алкоголю;
    -Банки: скляні банки від соків і закрутки, від дитячого харчування, склянки від ліків.

<b>❌ Не можна:</b>
    -Віконне і меблеве скло;
    -Лампочки;
    -Люстерко;
    -Скляний посуд;
    -Кришталь;
    -Кераміка та фарфор.
"""

    elif get_message_bot == "🥤 пластик":
        final_message = """<b>✔ Можна класти:</b>
Пластикова тара:
    -Пляшка від напоїв, молока і тд.;
    -Пляшка з під олії;
    -Пластикові кришки;
    -Упаковки від яєць з маркуванням "1";
    -Пляшки від гелів для душу, мила і тд.;
    -Пляшки від побутової хімії, миючих засобів;
    -Пакети від молока.
Пакети:
    -Пакети з ручками, пакети-майки;
    -Пакети для фасування.
Пінопласт:
    -Пакування від пінопласту;
    -Вироби з пінопласту.
    Тверді пластикові вироби:
    -Відра, каністри, тази
Тетра-пак:
    -Упаковка від молока, соку.
Консервні банки:
    -Упаковка від консерв;
    -Алюмінієві банки.
Щільна поліетиленова плівка:
    -Плівка від теплиць;
    -Плівка для пакування(наприклад від техніки)

<b>❌ Не можна класти:</b>
    -Лотки від яєць;
    -Одноразовий посуд(всі маркування);
    -Зубні щітки;
    -Білі тари від сметани та йогорту;
    -Прокладки;
    -Тампони;
    -Тюбики від зубної пасти і крему;
    -Памперси;
    -Обгортки від цукерок;
    -Фольга;
    -М’яке пакування від кетчупа і майонеза;
    -Касети для магнітофону;
    -Пакування від чипсів;
    -CD/DVD диски;
    -Фасувальні пакети на яких є їжа і пакети які є занадто брудні.
"""
    
    elif get_message_bot == "🍏 органіка":
        final_message = """<b>✔ Можна класти:</b>
    - м’ясні та рибні відходи, овочі і фрукти, лушпиння, хліб, напівфабрикати, кондитерські вироби та інші харчові відходи;
    - господарський папір, паперові серветки, залишки від чаю і кави;
    - кімнатні рослини та квіти.

<b>❌ Не можна класти:</b>
    - олію, молоко, соуси та інші рідкі харчові продукти;
    - будь-які рідини;
    - великі кістки;
    - плівку, метал, скло, попіл, недопалки, вкритий воском або плівкою папір, а також інші біологічні відходи, що не розкладаються.
"""

    elif get_message_bot == "⚠ небезпечні відходи":
        final_message = """<b>У пункт збору особливо небезпечних відходів слід відвозити:</b>
    - залишки масел та масляні фільтри;
    - рештки клею, фарби, лаку та розчинників;
    - лампи денного світла;
    - медичні відходи;
    - хімікати та пестициди;
    - ртутні термометри та інші відходи, що містять ртуть;
    - батарейки та акумулятори.
"""

    elif get_message_bot == "🔥 спалюється":
        final_message = """<b>Сміття або те що йде на спалювання:</b>
    -Флоу-пак(пакування від цукерок, круп, морозива);
    -Пакування від чипсів;
    -Чеки;
    -Пакування від глазурованих сирків;
    -Зубні щітки;
    -Використані шпалери;
    -Папір, яких має покриття з плівки або металу;
    -Баночки від сметани і йогурту;
    -Фасувальні пакети на яких є їжа і пакети які є занадто брудні.
    -Іграшки, які мають електронні елементи;
    -Тюбики від зубної пасти;
    -Пакування від кетчупу і майонезу;
    -Комбіновані упаковки;
    -Памперси;
    -Недопалки;
    -Серветки.
"""
    
    elif get_message_bot == "🔙 повернутися":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton('❓ Як сортувати сміття')
        btn2 = types.KeyboardButton('❓ Що куди класти')
        btn3 = types.KeyboardButton('🚩 Місця сортування')
        btn4 = types.KeyboardButton('📃 Інформація')
        markup.add(btn1, btn2, btn3, btn4)

        final_message = "Виберіть пункт що вас цікавить:"

    else:
        final_message = "😢 Невідома або невірно введена команда. Оберіть один із пунктів меню 👇🏻"
        
    bot.send_message(message.chat.id, final_message, parse_mode='html', reply_markup=markup)




@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('❓ Як сортувати сміття')
    btn2 = types.KeyboardButton('❓ Що куди класти')
    btn3 = types.KeyboardButton('🚩 Місця сортування')
    btn4 = types.KeyboardButton('📃 Інформація')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, '🤗 Вітаю, ' + str(message.from_user.first_name) + '.' + '\n' +'Чим можу допомогти?', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def mess(message):
    get_message_bot = message.text.strip().lower()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('❓ Як сортувати сміття')
    btn2 = types.KeyboardButton('❓ Що куди класти')
    btn3 = types.KeyboardButton('🚩 Місця сортування')
    btn4 = types.KeyboardButton('📃 Інформація')
    markup.add(btn1, btn2, btn3, btn4)

    if get_message_bot == "❓ як сортувати сміття":
        final_message = """<b>Як сортувати сміття – 6 простих кроків:</b>

1️⃣ Крок  
Придбайте окремі контейнери для кожного виду сировини (детальнішу інформацію можна отримати нажавши кноку "Що куди класти").
    
2️⃣ Крок  
Попередньо підготуйте сировину: промийте її від залишків їжі та висушість (знімайте кришки із фольги з йогуртів чи сметани, а також металеві кришки).
    
3️⃣ Крок 
Зменшіть об’єм пакувального матеріалу (випустіть повітря з пляшок й скрутіть їх, розкладіть коробки та упаковки, спресуйте залізні бляшанки);
    
4️⃣ Крок  
У контейнер «Папір» заборонено викидати: квитки на транспорт, чеки, паперові рушники, серветки, туалетний папір, стаканчики для кави, пергамент).
    
5️⃣ Крок  
У контейнер «Пластик» не можна викидати: обгортки від цукерок, файли, вушні палички, зубні щітки).
    
6️⃣ Крок  
Якщо у Вас є дача чи проживаєте в приватному будинку, то маєте чудову можливість компостувати органічні відходи й перетворити їх у добриво. Для аграрієв існують промислові компостні контейнери."""
        bot.send_message(message.chat.id, final_message, parse_mode='html', reply_markup=markup)

    elif get_message_bot == "❓ що куди класти":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        btn1 = types.KeyboardButton('🥤 Пластик')
        btn2 = types.KeyboardButton('🔍 Скло')
        btn3 = types.KeyboardButton('📄 Папір')
        btn4 = types.KeyboardButton('🍏 Органіка')
        btn5 = types.KeyboardButton('⚠ Небезпечні відходи')
        btn6 = types.KeyboardButton('🔥 Спалюється')
        btn7 = types.KeyboardButton("🔙 Повернутися")
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
        
        final_message = """Для спрощення процесу поділу сміття існує система колірного позначення баків з тим чи іншим вмістом:
🟠 Помаранчевий – пластик
🔵 Синій – папір
🟢 Зелений – скло
🔴 Червоний – електроніка
🟡 Жовтий – метал
⚫ Сірий (чорний) – органічні відходи"""
        bot.send_message(message.chat.id, final_message, reply_markup=markup)
        msg = bot.send_message(message.chat.id, "Оберіть тип сміття, що вас цікавить")
        bot.register_next_step_handler(msg, garbageSorting)

    elif get_message_bot == "🚩 місця сортування":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton("🔙 Повернутися")
        markup.add(btn1)

        msg = bot.send_message(message.chat.id, "Введіть назву міста", reply_markup=markup)
        bot.register_next_step_handler(msg, map)

    elif get_message_bot == "📃 інформація":
        final_message = """‼ Щороку, за офіційними даними, українці викидають <b>11 млн</b> тонн сміття - це десь <b>300 кг</b> на людину.
         
За даними з Мінекології, Мінрегіонбуду і екологів, площа всіх сміттєзвалищ України становить понад <b>10 тис. га</b>, а об'єм сміття - близько <b>1,2 км кубічних</b>.

Ці сміттєві піраміди щороку зростатимут.В Україні захоронюють майже всі відходи, а саме <b>94,4 %</b>. Ще <b>2,7 %</b> спалюють, і лише <b>3,09%</b> переробляють. 

Якщо ж українці будуть сортувати своє сміття, то виросте частка сміття, що перероблюється, тому тема його сортування є досить актуальною, і я допоможу Вам у цій справі."""
        bot.send_message(message.chat.id, final_message, parse_mode='html', reply_markup=markup)
    
    else:
        final_message = "😢 Невідома або невірно введена команда. Оберіть один із пунктів меню 👇🏻 "
        bot.send_message(message.chat.id, final_message, reply_markup=markup) 
       

bot.polling(none_stop = True)
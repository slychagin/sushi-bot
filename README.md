# sushi-bot
### Telegram бот для суши бара.

Простой телеграм бот для суши бара.
Выдает пользователю меню, адрес и режим работы.
Реализована админка, где администратор может добавлять и удалять в базу данных позиции меню.
Также работает инлайн режим для поиска различной информации.
Реализован фильтр нецензурных слов в чате.

### Клиентская часть:
![client](https://github.com/slychagin/sushi-bot/blob/master/demo_gifs/client.gif)

### Администратор:
![admin](https://github.com/slychagin/sushi-bot/blob/master/demo_gifs/admin.gif)

### Что использовано для создания бота:
- Python 3;
- aiogram.

### Для запуска локально:
- `git clone https://github.com/slychagin/sushi-bot.git`;
- установите все зависимости из файла `requirements.txt`;
- подключите бота в Telegram и получите токен;
- в файле `create_bot.py` подставьте свой токен;
- запустите файл `telegram_bot.py`

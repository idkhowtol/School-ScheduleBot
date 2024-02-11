from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN
from database import add_schedule_entry, get_today_schedule, hide_schedule, init_db

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Обработчик команды "start" и "help". Предоставляет информацию о командах бота.
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    # Отправка приветственного сообщения и списка доступных команд.
    await message.reply("Привет! Вот что я могу:\n"
                        "/add_lesson - Добавить урок в расписание (формат: Предмет : Преподаватели : Кабинет)\n"
                        "/schedule - Показать расписание на сегодня\n"
                        "/hide_lesson - Скрыть урок из расписания (формат: Номер урока)")

# Обработчик команды "add_lesson". Добавляет новый урок в расписание.
@dp.message_handler(commands=['add_lesson'])
async def add_schedule_command(message: types.Message):
    try:
        args = message.get_args().split(" : ")
        if len(args) != 3:
            await message.reply("Формат должен быть: Предмет : Преподаватель : Кабинет")
            return

        subject, teachers, classroom = args
        # Вызов функции для добавления урока с проверкой возможности добавления
        result, msg = add_schedule_entry(subject, teachers, classroom)
        await message.reply(msg)  # Отправка сообщения об успешном добавлении или ошибке
    except Exception as e:
        await message.reply(f"Ошибка: {e}")


# Обработчик команды "schedule". Отображает расписание на сегодня.
@dp.message_handler(commands=['schedule'])
async def today_schedule_command(message: types.Message):
    # Получение и отправка списка уроков на сегодня.
    schedule_messages = get_today_schedule()
    if not schedule_messages:
        await message.reply("На сегодня уроков нет.")
    else:
        reply_message = "Расписание на сегодня:\n" + "\n".join(schedule_messages)
        await message.reply(reply_message)

# Обработчик команды "hide_lesson". Скрывает указанный урок из расписания.
@dp.message_handler(commands=['hide_lesson'])
async def hide_schedule_command(message: types.Message):
    # Скрытие урока по порядковому номеру.
    try:
        lesson_number = int(message.get_args())
        result_message = hide_schedule(lesson_number)  
        await message.reply(result_message)
    except ValueError:
        await message.reply("Пожалуйста, укажите номер урока.")
    except Exception as e:
        await message.reply(f"Ошибка: {e}")

# Инициализирует базу данных и запускает бота.
if __name__ == '__main__':
    init_db()
    print("База данных успешно инициализирована.")
    executor.start_polling(dp, skip_updates=True)

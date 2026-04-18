import re
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

TOKEN = "8588283499:AAHPowTEfDq6StuBnzEGLbvn4NtSNrgJvDc"


# клавиатура
keyboard = ReplyKeyboardMarkup(
    [["Расчёт", "Помощь"]],
    resize_keyboard=True
)


def extract_numbers(text):
    nums = re.findall(r"\d+[.,]?\d*", text)
    return [float(n.replace(",", ".")) for n in nums]


def calculate(a1, a2, M, h):
    y = ((h - a2) * M) / (a1 - a2)
    x = M - y
    return round(x, 2), round(y, 2)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Выберите действие:",
        reply_markup=keyboard
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # кнопка ПОМОЩЬ
    if text == "Помощь":
        await update.message.reply_text(
            "Введите 4 числа через пробел:\n"
            "Что Вы хотите смешать и для чего?"
            "жирность молока(обрата), жирность сливок(масла, змж), масса готового продукта, жирность готового продукта\n\n"
            "Пример:\n0,05 26 1000 20"
        )
        return

    # кнопка РАСЧЁТ
    if text == "Расчёт":
        context.user_data["mode"] = "calc"
        await update.message.reply_text(
            "Введите данные пример:\n0,05 3,4 1000 20"
        )
        return

    # если не нажал "Расчёт" — игнор
    if context.user_data.get("mode") != "calc":
        await update.message.reply_text(
            "Нажмите 'Расчёт', чтобы начать"
        )
        return

    # обработка чисел
    nums = extract_numbers(text)

    if len(nums) < 4:
        await update.message.reply_text(
            "Ошибка. Введите 4 числа:\n3.6 26 1000 20"
        )
        return

    a1, a2, M, h = nums[:4]

    try:
        x, y = calculate(a1, a2, M, h)

        await update.message.reply_text(
            f"Чтобы получить {M} кг продукта с жирностью {h}%:\n\n"
            f"{y} кг молока {a1}%\n"
            f"{x} кг сливок {a2}%",
            reply_markup=keyboard
        )

        # сброс режима
        context.user_data["mode"] = None

    except ZeroDivisionError:
        await update.message.reply_text("Ошибка: жирности не должны совпадать")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    print("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
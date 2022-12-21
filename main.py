from aiogram import Bot, Dispatcher, types, executor

import expenses

TOKEN = "5720908741:AAG71Sas1aUUxcSNFfZ0KoqqIH8hrpt24vk"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def start(message: types.Message):
    await message.reply(
        "Sup, here is you command lines to use me\n\n"
        "Add you expenses in format: 70 food\n"
        "Available categories: /categories\n"
        "Today expenses: /today\n"
        "Month expenses: /month\n"
        "Last expenses: /expenses\n")


@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_expense(message: types.Message):
    row_id = int(message.text[4:])
    expenses.delete_expense(row_id)
    answer_message = "Deleted"
    await message.answer(answer_message)


@dp.message_handler(commands=['categories'])
async def list_categories(message: types.Message):
    answer_message = "Categories: \n\n *" + (" \n * ".join(expenses.CATEGORIES))
    await message.answer(answer_message)


@dp.message_handler(commands=['today'])
async def today_stats(message: types.Message):
    answer_message = expenses.get_today_stats()
    await message.answer(answer_message)


@dp.message_handler(commands=['month'])
async def month_stats(message: types.Message):
    answer_message = expenses.get_month_stats()
    await message.answer(answer_message)


@dp.message_handler(commands=['expenses'])
async def list_expenses(message: types.Message):
    last_expenses = expenses.last()
    if not last_expenses:
        await message.answer("You have not spent your money yet")
        return

    last_expenses_rows = [
        f"{expense.amount} eur on {expense.category} - press /del{expense.id} for delete"
        for expense in last_expenses]
    answer_message = "Last expenses:\n\n* " + "\n\n* ".join(last_expenses_rows)
    await message.answer(answer_message)


@dp.message_handler()
async def add_expense(message: types.Message):
    try:
        expense = expenses.add_expense(message.text)
    except Exception as e:
        await message.answer(str(e))
        return
    answer_message = (
        f"Added expense on sum {expense.amount} eur to {expense.category}.\n\n"
        f"{expenses.get_today_stats()}")
    await message.answer(answer_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
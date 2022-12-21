import datetime
from typing import NamedTuple, Optional, List

import pytz

import db

CATEGORIES = ["apartments", "food", "car", "bank deposit", "credit", "snacks"]


class Message(NamedTuple):
    amount: int
    category: str


class Expense(NamedTuple):
    id: Optional[int]
    amount: int
    category: str


def add_expense(raw_message: str)->Expense:
    parsed_message = _parse_message(raw_message)

    today_datetime = _get_current_datetime()
    created = today_datetime.strftime("%Y - %m - %d %H:%M:%S")

    db.insert("expense", {
        "amount": parsed_message.amount,
        "created": created,
        "category": parsed_message.category
    })
    return Expense(id=None, amount=parsed_message.amount, category=parsed_message.category)


def get_today_stats()->str:
    # sourcery skip: assign-if-exp, reintroduce-else, swap-if-expression
    cursor = db.get_cursor()
    cursor.execute("select sum(amount)"
                    "from expense where date(created)=date('now', 'localtime')")
    result = cursor.fetchone()
    if not result[0]:
        return "Today you didn`t spend money"
    else:
        return (f"Spent today:\n"
                f"Total - '{result[0]}' eur")


def get_month_stats()->str:
    now = _get_current_datetime()
    first_day_of_month = f'{now.year:04d}-{now.month:02d}-01'
    cursor = db.get_cursor()
    cursor.execute("select sum(amount)"
                    f"from expense where date(created) >= '{first_day_of_month}'")
    result = cursor.fetchone()
    if not result[0]:
        return "In this month you have not spent money"
    else:
        return (f'Spent money this month:\n'
            f'At all = {result[0]} eur.')


def last():
    cursor = db.get_cursor()
    cursor.execute(
        "SELECT expense.id, expense.amount, expense.category"
        "from expense "
        "order by created desc limit 10"
    )
    rows = cursor.fetchall()
    return [Expense(id=row[0], amount=row[1], category=row[2]) for row in rows]


def delete_expense(row_id: int)->None:
    db.delete("expense", row_id)


def _parse_message(raw_message: str):
    amount, category = raw_message.split(maxsplit=1)
    if category not in CATEGORIES:
        raise Exception(f"Category  '{category}' doesn`t excist")

    return Message(amount=amount, category=category)


def _get_current_datetime():
    tz = pytz.timezone("Europe/Paris")
    return datetime.datetime.now(tz)
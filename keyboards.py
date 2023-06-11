from telethon.tl.types import ReplyKeyboardMarkup, ReplyInlineMarkup, \
    KeyboardButton as Button, KeyboardButtonCallback as InlineButton, \
    KeyboardButtonRow as Row

from config import SEP


def do_button(title: str, data: list):
    return InlineButton(title, bytes(f'{SEP}'.join(data).encode('UTF-8')))


def do_rows(buttons, rows_count: int = 2):
    r = []
    for i in range(0, len(buttons) - len(buttons) % rows_count, rows_count):
        tmp = []
        for k in range(rows_count):
            tmp.append(buttons[i + k])
        r.append(Row(tmp))

    del buttons[: len(buttons) - len(buttons) % rows_count]

    if buttons:
        r.append(Row(buttons))

    return r


async def make_markup(user, menu: str, data=None):
    butt = []
    match menu:
        case 'main':
            butt = [
                do_button('Канал/беседа', [menu, 'mychan']),
                do_button('Настройки', [menu, 'settings'])
            ]

            """
            if user.admin_access_lvl > 0:
                butt += [
                ]
            """

        case 'mychan':
            butt = [do_button(f'Отвязать', [menu, 'detach', data]) if data is not None
                    else do_button('Привязать', [menu, 'attach']),
                    do_button('Назад', [menu, 'back'])]

        case 'settings':
            butt = [
                do_button('Изменить ссылку' if data is not None else 'Добавить ссылку', [menu, 'setDAlink']),
                do_button('Назад', [menu, 'back'])
            ]

    return ReplyInlineMarkup(do_rows(butt))
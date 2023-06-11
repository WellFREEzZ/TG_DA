from typing import Union
from telethon import TelegramClient, events
from telethon.errors import MessageNotModifiedError, MessageIdInvalidError, MessageEditTimeExpiredError
from telethon.tl.types import PeerUser

from config import TG_API_ID, TG_API_HASH, TG_BOT_TOKEN, SEP
from dbAPI import SQLiteAPI

import StaticTexsts
import keyboards

import asyncio

bot = TelegramClient('test', TG_API_ID, TG_API_HASH)
bot_db = SQLiteAPI()


@bot.on(events.NewMessage(pattern='/start'))
async def main_menu(event: Union[events.NewMessage.Event, events.CallbackQuery.Event]):
    if type(event) == events.NewMessage.Event:
        user = bot_db.get_user(event.sender.id)
        if not user:
            bot_db.add_user(event.sender.id, event.sender.username, event.message.id)
            user = bot_db.get_user(event.sender.id)
    else:
        user = bot_db.get_user(event.query.peer.user_id)

    text = StaticTexsts.menu_main.format(da_link='__Не настроена__' if user.da_token is None
    else f'[сслыка](https://www.donationalerts.com/widget/alerts?group_id=1&token={user.da_token})',
                                         chan_link='__Не настроена__' if user.cha_tg_id is None
    else f'[ссылка](https://t.me/{user.cha_tg_id})'
                                         )

    buttons = await keyboards.make_markup(user, 'main')

    try:
        await bot.edit_message(user.tg_id, user.active_msg_id, text, buttons=buttons)
    except (MessageNotModifiedError, MessageEditTimeExpiredError, MessageIdInvalidError):
        await bot.send_message(user.tg_id, text, buttons=buttons)


@bot.on(events.NewMessage(pattern="\b(?!(start|admin)).+"))
async def user_input(event):
    user = bot_db.get_user(event.sender.id)


@bot.on(events.CallbackQuery())
async def query_handler(event):
    if type(event.query.peer) != PeerUser:
        return
    user = bot_db.get_user(event.query.peer.user_id)
    menu, command, *data = (event.data.decode('UTF-8')).split(SEP)

    match command:
        case 'cancel':
            return
        case 'ok':
            return
        case 'back':
            match menu:
                case 'mychan' | 'settings':
                    await main_menu(event)
            return
        case 'home':
            await main_menu(event)
            return

    match menu:
        case 'main':
            match command:
                case 'mychan':
                    pass
                case 'settings':
                    pass

        case 'mychan':
            match command:
                case 'detach':
                    pass
                case 'attach':
                    user.adding_chan = 1
                    bot_db.update_user(user)
                    await bot.edit_message(user.th_id, user.active_msg_id, "Отправьте ссылку на канал (беседу), "
                                                                           "в который "
                                                                           "нужно отправлять уведомления о донатах.")

        case 'settings':
            match command:
                case 'setDAlink':
                    pass


if __name__ == '__main__':
    bot.start(TG_BOT_TOKEN)
    bot.loop.run_forever()

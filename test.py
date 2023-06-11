from config import DA_TOKEN, TG_BOT_TOKEN, MY_ID as WFZ_id
from donationalerts import Alert
from bot import bot
import asyncio


async def postman(token: str):
    alert = Alert(token)

    @alert.event()
    def new_donation(event):
        print(event)
        mess = f'**`{event.username}` отправил `{event.amount_formatted}` {event.currency}!**\n\n'\
                f'{event.message}'
        asyncio.get_event_loop().create_task(bot.send_message(WFZ_id, message=mess))


if __name__ == '__main__':
    main_loop = asyncio.get_event_loop()
    bot.start(bot_token=TG_BOT_TOKEN)
    main_loop.create_task(postman(DA_TOKEN))
    bot.loop.run_forever()

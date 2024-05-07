from data.config import NUM_PHONE, TG_API_ID, TG_API_HASH
from telethon import TelegramClient
from json import dump, load


input('Make sure than you already put your '
    'API ID and API Hash and PHONE NUMBER (with country code "+XX...) in data/config.py\n\n'
    'If is the first login check another device for copy verification code and put here when ask for this\n\n'
    '\n\nPress any key to continue')


SESSION_PATH = './data/user_bot.session'
SCRAPED_USERS_PATH = './data/scraped_users.json'
tg = TelegramClient(SESSION_PATH, TG_API_ID, TG_API_HASH)
tg.start(NUM_PHONE)


with open(SCRAPED_USERS_PATH, 'r', encoding='utf-8') as users_load:
    try:
        user_list = load(users_load)
    except:
        user_list = {}


def user_scraper():
    for group in tg.iter_dialogs():
        if group.is_group:
            user_list[group.id] = {}
            for user in tg.iter_participants(group.id):
                if user.bot:
                    continue
                user_list[group.id][user.id] = {
                    'user_id': user.id,
                    'username': user.username,
                    'name': user.first_name
                    }
    with open(SCRAPED_USERS_PATH, 'w') as users_dump:
        dump(user_list, users_dump, indent=4)
    print('DONE. USERS SAVED!\n\nCheck file in: TGScraper/data/scraped_users.json')


input('Press any key to start scraper')
user_scraper()



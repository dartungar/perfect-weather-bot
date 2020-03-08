import logging
import os
import random
import string
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters, PicklePersistence
import db
import helpers
from helpers import get_nearby_locations_by_iwmo, get_iwmos_by_climate_dict
from places import country_codes
from climate_dicts import months_translate_dict, temperature_translate_dict, precipitation_translate_dict, sunshine_translate_dict
from datetime import datetime


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


BOT_TOKEN = os.environ.get('BOT_TOKEN_WEATHER')

keyboard_en = ReplyKeyboardMarkup([['/go', '/preferences'], ['/language', '/help']], True)
keyboard_ru = ReplyKeyboardMarkup([['/go', '/parametry_pogody'], ['/language', '/help']], True)

month_keyboard_en = ReplyKeyboardMarkup([[f'current ({datetime.now().strftime("%h")})'], ['Jan', 'Feb', 'Mar', 'Apr'], ['May', 'Jun', 'Jul', 'Aug'], ['Sep', 'Oct', 'Nov', 'Dec']], True)
month_keyboard_ru = ReplyKeyboardMarkup([[f'Текущий ({datetime.now().strftime("%h")})'], ['Янв', 'Фев', 'Мар', 'Апр'], ['Май', 'Июн', 'Июл', 'Авг'], ['Сен', 'Окт', 'Ноя', 'Дек']], True)

temperature_keyboard_en = ReplyKeyboardMarkup([['scorching', 'hot'], ['warm', 'temperate'], ['tepid', 'cold'], ['freezing', 'skip']], True)
temperature_keyboard_ru = ReplyKeyboardMarkup([['обжигающе', 'жарко'], ['тепло', 'умеренно'], ['прохладно', 'холодно'], ['морозно', 'всё равно']], True)

precipitation_keyboard_en = ReplyKeyboardMarkup([['constantly', 'often'], ['sometimes', 'rarely'], ['very rarely', 'skip']], True)
precipitation_keyboard_ru = ReplyKeyboardMarkup([['постоянно', 'часто'], ['периодически', 'редко'], ['очень редко', 'всё равно']], True)

sunshine_keyboard_en = ReplyKeyboardMarkup([['very sunny', 'sunny'], ['normal', 'cloudy'], ['very cloudy', 'skip']], True)
sunshine_keyboard_ru = ReplyKeyboardMarkup([['очень солнечно', 'солнечно'], ['нормально', 'облачно'], ['очень облачно', 'всё равно']], True)

save_preferences_keyboard = ReplyKeyboardMarkup([['/save_preferences'], ['/do_not_save']], True)
language_keyboard = ReplyKeyboardMarkup([['🇷🇺 Russian'], ['🇬🇧 English']], True)


CHOOSING_IF_SAVE, CHOOSING_MONTH, CHOOSING_TEMPERATURE, CHOOSING_HUMIDITY, CHOOSING_PRECIPITATION, CHOOSING_SUNSHINE, CHOOSING_LANGUAGE = range(7)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def start(update, context):
    context.user_data['language'] = 'eng'
    reply_text = 'Hello there! Use /preferences to set your favorite weather, /place to find a place with such weather. /language to change (🇷🇺, 🇬🇧)'
    update.message.reply_text(reply_text, reply_markup=keyboard_en)
    return ConversationHandler.END


# def main_menu(update, context):
#     text = update.message.text
#     if text == 'go' or text == 'найти место':
#         get_place(update, context)
#     elif text == 'preferences' or text == 'параметры погоды':
#         preferences(update, context)
#     elif text == 'language' or text == 'язык':
#         show_language_menu(update, context)
#     elif text == 'help' or text == 'помощь':
#         show_help(update, context) 



def go_to_main_menu(update, context):
    reply_text = '.'
    update.message.reply_text(reply_text, reply_markup=keyboard_en)
    return ConversationHandler.END


def get_place(update, context):
    
    try:
        if context.user_data['has_preferences'] == True:
            
            try:
                logger.info('trying to get iwmos by climate...')
                iwmos = get_iwmos_by_climate_dict(month=context.user_data['month'], 
                                                        mean_max_temp=context.user_data['mean_max_temp_mean_range'], 
                                                        humidity='none', # TODO
                                                        precipitation_monthly=context.user_data['precipitation_monthly_range'], 
                                                        percent_sunshine=context.user_data['sunshine_percent_range'])
            except Exception as e:
                logger.error(f'could not get iwmos: {e}')
            logger.info(f'got a list of {len(iwmos)} iwmos, trying to get random...')
            
            if len(iwmos) == 0:
                if context.user_data['language'] == 'eng':
                    reply_text = 'Sorry, could not find a place with your kind of perfect weather!'
                if context.user_data['language'] == 'rus':
                    reply_text = 'Не нашёл места с подходящим климатом :('
                update.message.reply_text(reply_text, reply_markup=keyboard_en)
                return ConversationHandler.END
            
            iwmo = random.choice(iwmos)

            logger.info(f'got random iwmo {iwmo}; trying to get nearby locations...')
            try:
                locations = get_nearby_locations_by_iwmo(iwmo, 30)
            except Exception as e:
                logger.info(f'could not get nearby locations by iwmo: {e}')
            
            logger.info(f'found {len(locations)} locations!')
            
            if len(locations):
                chosen_location = random.choice(locations)
                location_name = chosen_location[3]
                location_country = country_codes.loc[country_codes.Code==chosen_location[1].upper(), ['Name']].iloc[0, 0]
                location_lat = chosen_location[6]
                location_long = chosen_location[7]
            else:
                location_name = iwmo[11]
                location_country = iwmo[12]
                location_lat = iwmo[13]
                location_long = iwmo[14]

            logger.info('building reply text...')
            temp = iwmo[2]
            daytemp = iwmo[3]
            precip = iwmo[6]
            sunshine = iwmo[7]
            nd = 'n/a '

            if temp > -9999 and daytemp == -9999:
                daytemp = f'~{temp + (temp * 0.3)}'

            weather_google_query = 'https://www.google.com/search?q='
            for word in location_name.split():
                weather_google_query += f'{word}%20'
            for word in location_country.split():
                weather_google_query += f'{word}%20'
            weather_google_query += 'weather'

            try:
                if context.user_data['language'] == 'eng':
                    reply_text = reply_text = f'''Check out {location_name}, {location_country}.
Climate in {iwmo[1]}: 
Avg. temperature: {temp if temp > -9999 else nd}C
Avg. daytime temperature: {daytemp if daytemp > -9999 else nd}C
Avg. daily precipitation: {round(precip/30, 1) if precip > -9999 else nd}mm
Avg. hours of sunshine daily: {round(sunshine/30, 1) if sunshine > -9999 else nd}
Google Maps: https://www.google.com/maps/place/{location_lat},{location_long}/@{location_lat},{location_long},6z
Current Weather: {weather_google_query}'''
                if context.user_data['language'] == 'rus':
                    reply_text = f'''Обратите внимание на {location_name}, {location_country}.
Климат в {iwmo[1]}: 
Среднесуточная температура: {temp if temp > -9999 else nd}C
Средний максимум (днём): {daytemp if daytemp > -9999 else nd}C
Средний уровень осадков в день: {round(precip/30, 1) if precip > -9999 else nd}mm
Солнечная погода, часов в день: {round(sunshine/30, 1) if sunshine > -9999 else nd}
Google Maps: https://www.google.com/maps/place/{location_lat},{location_long}/@{location_lat},{location_long},6z
Погода на сегодня: {weather_google_query}'''
                
            except Exception as e:
                logger.error(f'could not build reply string: {e}')
                if context.user_data['language'] == 'eng':
                    reply_text = 'Something went wrong :( Try restarting me with /start'
                if context.user_data['language'] == 'rus':
                    reply_text = 'Непонятная ошибка :( Попробуйте перезапустить меня - /start '

            update.message.reply_text(reply_text, reply_markup=keyboard_en)
            return ConversationHandler.END
    
    except Exception as e:
        logger.error(f'error: {e}')
        if context.user_data['language'] == 'eng':
            reply_text = 'Seems like you have no preferences. Use /preferences to tell me what weather you like.'
        if context.user_data['language'] == 'rus':
            reply_text = 'Расскажите, какая погода вам нужна, с помощью /preferences.'
        
        update.message.reply_text(reply_text, reply_markup=keyboard_en)
        return ConversationHandler.END


def save_preferences(update, context):
    if context.user_data['language'] == 'eng':
        reply_text = 'Memorized your preferences!'
    if context.user_data['language'] == 'rus':
        reply_text = 'Запомнил ваши предпочтения!'
    
    context.user_data['has_preferences'] = True
    logger.info(context.user_data)
    update.message.reply_text(reply_text, reply_markup=keyboard_en)
    return ConversationHandler.END


def reset_preferences(update, context):
    context.user_data['month'] = datetime.now().strftime('%h')
    context.user_data['mean_temp_mean_range'] = 'none'
    context.user_data['mean_max_temp_mean_range'] = 'none'
    context.user_data['humidity_mean_range'] = 'none'
    context.user_data['precipitation_monthly_range'] = 'none'
    context.user_data['sunshine_percent_range'] = 'none'
    if context.user_data['language'] == 'eng':
        reply_text = 'preferences reset!'
    if context.user_data['language'] == 'rus':
        reply_text = 'предпочтения сброшены!'
    
    update.message.reply_text(reply_text, reply_markup=keyboard_en)
    return ConversationHandler.END
    

def preferences(update, context):
    if context.user_data['language'] == 'eng':
        reply_text = 'Choose month:'
        update.message.reply_text(reply_text, reply_markup=month_keyboard_en)
    if context.user_data['language'] == 'rus':
        reply_text = 'Выберите месяц:'
        update.message.reply_text(reply_text, reply_markup=month_keyboard_ru)
    return CHOOSING_MONTH


def get_month_preferences(update, context):
    value = update.message.text
    if 'current' in value or 'Текущий' in value:
        context.user_data['month'] = datetime.now().strftime('%h')
    else:
        context.user_data['month'] = months_translate_dict[value]

    if context.user_data['language'] == 'eng':
        reply_text = 'Now, tell me about your kind of perfect weather. What is day temperature like?'
        update.message.reply_text(reply_text, reply_markup=temperature_keyboard_en)
    if context.user_data['language'] == 'rus':
        reply_text = 'Какой должна быть дневная температура?'
        update.message.reply_text(reply_text, reply_markup=temperature_keyboard_ru)
    
    
    return CHOOSING_TEMPERATURE


def get_temperature_preferences(update, context):
    value = update.message.text
    context.user_data['mean_max_temp_mean_range'] = temperature_translate_dict[value]

    if context.user_data['language'] == 'eng':
        reply_text = 'What about precipitation? Does it rain or snow a lot?'
        update.message.reply_text(reply_text, reply_markup=precipitation_keyboard_en)
    if context.user_data['language'] == 'rus':
        reply_text = 'Дождь - часто?'
        update.message.reply_text(reply_text, reply_markup=precipitation_keyboard_ru)
    
    
    return CHOOSING_PRECIPITATION


def get_precipitation_preferences(update, context):
    value = update.message.text
    context.user_data['precipitation_monthly_range'] = precipitation_translate_dict[value]
    if context.user_data['language'] == 'eng':
        reply_text = 'How sunny do you prefer it?' 
        update.message.reply_text(reply_text, reply_markup=sunshine_keyboard_en)
    if context.user_data['language'] == 'rus':
        reply_text = 'Солнечно или облачно?'
        update.message.reply_text(reply_text, reply_markup=sunshine_keyboard_ru)
    return CHOOSING_SUNSHINE


def get_sunshine_preferences(update, context):
    value = update.message.text
    context.user_data['sunshine_percent_range'] = sunshine_translate_dict[value]
    if context.user_data['language'] == 'eng':
        reply_text = 'OK then. Shall I save your preferences?'
    if context.user_data['language'] == 'rus':
        reply_text = 'Вас понял. Сохраняем предпочтения?'
    
    update.message.reply_text(reply_text, reply_markup=save_preferences_keyboard)
    return CHOOSING_IF_SAVE


def show_help(update, context):
    lang = context.user_data['language']
    if lang == 'eng':
        reply_text = '''Use /preferences to tell me what kind of weather you like.
Then use /go to get random place with such weather.
/language - change language (🇷🇺RUS , 🇬🇧ENG) '''
        update.message.reply_text(reply_text, reply_markup=keyboard_en)
    if lang == 'rus':
        reply_text = '''/preferences - расскажите, какая погода вам нужна.
/go - найду для вас место с нужной погодой.
/language - поменять язык (🇷🇺RUS , 🇬🇧ENG).
Приятного использования!'''  
        update.message.reply_text(reply_text, reply_markup=keyboard_en)     
    
    return ConversationHandler.END


def show_language_menu(update, context):
    reply_text = 'Choose language 👇 Выберите язык: '
    update.message.reply_text(reply_text, reply_markup=language_keyboard)
    return CHOOSING_LANGUAGE


def choose_language(update, context):
    lang = update.message.text
    if 'Russian' in lang:
        context.user_data['language'] = 'rus'
        reply_text = 'Установлен русский язык (кроме главного меню)!'
        update.message.reply_text(reply_text, reply_markup=keyboard_en)
    if 'English' in lang:
        context.user_data['language'] = 'eng'
        reply_text = 'Switched to English!'
        update.message.reply_text(reply_text, reply_markup=keyboard_en)
    
    
    return ConversationHandler.END




### main ###
def main():
    pp = PicklePersistence(filename='weather_bot')
    updater = Updater(BOT_TOKEN, persistence=pp, use_context=True)

    dp = updater.dispatcher

    preferences_handler = ConversationHandler(
        entry_points=[CommandHandler('preferences', preferences), CommandHandler('parametry_pogody', preferences)],

        states={

            CHOOSING_MONTH: [MessageHandler(Filters.text, get_month_preferences)],

            CHOOSING_TEMPERATURE: [MessageHandler(Filters.text, get_temperature_preferences)],

            CHOOSING_PRECIPITATION: [MessageHandler(Filters.text, get_precipitation_preferences)],

            #CHOOSING_HUMIDITY: [MessageHandler(Filters.text, get_humidity_preferences)],

            CHOOSING_SUNSHINE: [MessageHandler(Filters.text, get_sunshine_preferences)],

            CHOOSING_IF_SAVE: [CommandHandler('save_preferences', save_preferences),
                        CommandHandler('do_not_save', reset_preferences)],
        },

        fallbacks=[CommandHandler('back', go_to_main_menu)]
    )
    dp.add_handler(preferences_handler)


    language_handler = ConversationHandler(
        entry_points=[CommandHandler('language', show_language_menu)],

        states={CHOOSING_LANGUAGE: [MessageHandler(Filters.text, choose_language)]},
        fallbacks=[CommandHandler('back', go_to_main_menu)])
    dp.add_handler(language_handler)


    # main_menu_handler = MessageHandler(Filters.text, main_menu)
    # dp.add_handler(main_menu_handler)

    get_go_handler = CommandHandler('go', get_place)
    dp.add_handler(get_go_handler)

    start_handler = CommandHandler('start', start)
    dp.add_handler(start_handler)

    help_handler = CommandHandler('help', show_help)
    dp.add_handler(help_handler)

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
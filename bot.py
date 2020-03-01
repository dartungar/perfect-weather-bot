import logging
import os
import random
import string
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters, PicklePersistence
import db
import helpers
from helpers import get_nearby_locations_by_iwmo
from helpers import get_iwmos_by_climate_dict
from datetime import datetime


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


BOT_TOKEN = os.environ.get('BOT_TOKEN_WEATHER')

keyboard = ReplyKeyboardMarkup([['/start'], ['/preferences', '/place']], True)
temperature_keyboard = ReplyKeyboardMarkup([['scorching', 'hot'], ['warm', 'temperate'], ['tepid', 'cold'], ['freezing', 'skip']], True)
month_keyboard = ReplyKeyboardMarkup([[f'current ({datetime.now().strftime("%h")})'], ['Jan', 'Feb', 'Mar', 'Apr'], ['May', 'Jun', 'Jul', 'Aug'], ['Sep', 'Oct', 'Nov', 'Dec']], True)
precipitation_keyboard = ReplyKeyboardMarkup([['constantly', 'often'], ['sometimes', 'rarely'], ['very rarely', 'skip']], True)
sunshine_keyboard = ReplyKeyboardMarkup([['very sunny', 'sunny'], ['normal', 'cloudy'], ['very cloudy', 'skip']], True)
save_preferences_keyboard = ReplyKeyboardMarkup([['/save_preferences'], ['/do_not_save']], True)



CHOOSING_IF_SAVE, CHOOSING_MONTH, CHOOSING_TEMPERATURE, CHOOSING_HUMIDITY, CHOOSING_PRECIPITATION, CHOOSING_SUNSHINE = range(6)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def start(update, context):
    reply_text = 'hello there! /preferences to set your favorite weather, /place to find a place with such weather.'
    update.message.reply_text(reply_text, reply_markup=keyboard)
    return ConversationHandler.END


def go_to_main_menu(update, context):
    reply_text = '.'
    update.message.reply_text(reply_text, reply_markup=keyboard)
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
                                                        sunshine=context.user_data['sunshine_hours_range'])
            except Exception as e:
                logger.error(f'could not get iwmos: {e}')
            logger.info(f'got a list of {len(iwmos)} iwmos, trying to get random...')
            
            if len(iwmos) == 0:
                update.message.reply_text('Sorry, could not find a place with your kind of perfect weather!', reply_markup=keyboard)
                return ConversationHandler.END
            
            iwmo = random.choice(iwmos)

            logger.info('got random iwmo; trying to get nearby locations...')
            try:
                locations = get_nearby_locations_by_iwmo(iwmo, 30)
            except Exception as e:
                logger.info(f'could not get nearby locations by iwmo: {e}')
            
            logger.info(f'found {len(locations)} locations!')
            chosen_location = random.choice(locations)

            location_name = chosen_location[3]
            location_country = chosen_location[1]
            location_lat = chosen_location[6]
            location_long = chosen_location[7]


            logger.info('building reply text...')
            daytemp = iwmo[3]
            precip = iwmo[6]
            sunshine = iwmo[7]
            nd = 'n/a '
            try:
                reply_text = f'''Check out {string.capwords(location_name.strip())}, {string.capwords(location_country.strip())}.
Climate in {iwmo[1]}: 
Daytime temperature: {daytemp if daytemp > -9999 else nd}C
Average daily precipitation: {round(precip/30, 1) if precip > -9999 else nd}mm
Average hours of sunshine daily: {round(sunshine/30, 1) if sunshine > -9999 else nd}
Google Maps: https://www.google.com/maps/place/{location_lat},{location_long}/@{location_lat},{location_long},6z'''
            except Exception as e:
                logger.error(f'could not build reply string: {e}')

            update.message.reply_text(reply_text, reply_markup=keyboard)
            return ConversationHandler.END
    
    except Exception as e:
        logger.error(f'error: {e}')
        reply_text = 'Seems like you have no preferences. Use /preferences to tell me what weather you like.'
        update.message.reply_text(reply_text, reply_markup=keyboard)
        return ConversationHandler.END


def save_preferences(update, context):
    reply_text = 'saved your preferences!'
    context.user_data['has_preferences'] = True
    logger.info(context.user_data)
    update.message.reply_text(reply_text, reply_markup=keyboard)
    return ConversationHandler.END


def reset_preferences(update, context):
    context.user_data['month'] = datetime.now().strftime('%h')
    context.user_data['mean_temp_mean_range'] = 'none'
    context.user_data['mean_max_temp_mean_range'] = 'none'
    context.user_data['humidity_mean_range'] = 'none'
    context.user_data['precipitation_monthly_range'] = 'none'
    context.user_data['sunshine_hours_range'] = 'none'
    reply_text = 'preferences reset!'
    update.message.reply_text(reply_text, reply_markup=keyboard)
    return ConversationHandler.END
    

def preferences(update, context):
    reply_text = 'Choose month:'
    update.message.reply_text(reply_text, reply_markup=month_keyboard)
    return CHOOSING_MONTH


def get_month_preferences(update, context):
    value = update.message.text
    if 'current' in value:
        context.user_data['month'] = datetime.now().strftime('%h')
    else:
        context.user_data['month'] = value
    reply_text = 'Now, tell me about your kind of perfect weather. What is day temperature like?'
    update.message.reply_text(reply_text, reply_markup=temperature_keyboard)
    return CHOOSING_TEMPERATURE


def get_temperature_preferences(update, context):
    value = update.message.text
    context.user_data['mean_max_temp_mean_range'] = value if value != 'skip' else 'none'
    reply_text = 'Very well. What about precipitation? Does it rain or snow a lot?'
    update.message.reply_text(reply_text, reply_markup=precipitation_keyboard)
    return CHOOSING_PRECIPITATION


def get_precipitation_preferences(update, context):
    value = update.message.text
    context.user_data['precipitation_monthly_range'] = value if value != 'skip' else 'none'
    reply_text = 'Good. And for the sunshine - how sunny do you prefer it?'
    update.message.reply_text(reply_text, reply_markup=sunshine_keyboard)
    return CHOOSING_SUNSHINE


def get_sunshine_preferences(update, context):
    value = update.message.text
    context.user_data['sunshine_hours_range'] = value if value != 'skip' else 'none'
    reply_text = 'OK then. Shall I save your preferences?'
    update.message.reply_text(reply_text, reply_markup=save_preferences_keyboard)
    return CHOOSING_IF_SAVE


def main():
    pp = PicklePersistence(filename='weather_bot')
    updater = Updater(BOT_TOKEN, persistence=pp, use_context=True)

    dp = updater.dispatcher

    preferences_handler = ConversationHandler(
        entry_points=[CommandHandler('preferences', preferences)],

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


    start_handler = CommandHandler('start', start)
    dp.add_handler(start_handler)

    get_place_handler = CommandHandler('place', get_place)
    dp.add_handler(get_place_handler)

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
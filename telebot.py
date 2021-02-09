from telegram.ext import Updater, MessageHandler, Filters
import database
import json

# obtain data from the config file
with open("example.config.json", "r") as config_file:
    data = json.load(config_file)
token = data['token']
chat_id = data['chat_id']
max_text_len = data['max_caption_length']
max_photo_size = data['max_photo_size']

# Create updater from bot token
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher


def store_image(update, context):
    """ Store an image """
    # only allow images
    if not update.message.photo:
        return False

    # Only allow messages from selected chat id
    if not update.message.chat.id == chat_id:
        return False

    # get the caption and check that it is not too long
    text = update.message.caption
    if not text:
        text = ''
    if len(text) > max_text_len:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='Caption too long! Maximum {} characters'.format(max_text_len))
        return False

    # Select photo with reasonable solution
    photo = update.message.photo[0]
    for p in update.message.photo:
        if p.file_size < max_photo_size:
            photo = p

    # get informations from message
    name = update.message.from_user.first_name
    file_id = photo.file_id
    date = update.message.date.strftime("%d-%m-%Y")
    update_id = update.update_id

    # get file and show some information
    file = context.bot.getFile(file_id)
    print('date ', date)
    print('file_id', file_id)
    print('name', name)
    # download file to unique filename
    filename = 'images/' + date + '_' + file_id + '.jpg'
    file.download(filename)
    # add entry to database
    database.insert(name, text, date, filename, file_id, update_id)
    # send a nice response and finish
    context.bot.send_message(chat_id=update.effective_chat.id, text='Thanks, {}!'.format(name))
    return True


# initialize a handler and add it to dispatcher
image_handler = MessageHandler(Filters.photo, store_image)
dispatcher.add_handler(image_handler)
updater.start_polling()

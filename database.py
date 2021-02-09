""" These functions manage the TinyDB which stores all images, their order and additional information """

from tinydb import TinyDB, Query


def insert(name, text, time, filename, file_id, update_id):
    """ Function to insert a new image into the database """
    # open database
    db = TinyDB('database.json')
    # if first entry -> special settings
    if len(db.all()) == 0:
        item_id = 1
        next_id = None
    # if entries already exist
    else:
        # get the latest image
        latest_image = get_latest_image()
        # set the previous id
        next_id = latest_image['item_id']
        # set own id
        item_id = next_id + 1

        # set next id of start image
        entry = Query()
        db.update({'prev_id': item_id}, entry.item_id == latest_image['item_id'])

    # Insert data into database
    db.insert({
        'item_id': item_id,
        'name': name,
        'time': time,
        'filename': filename,
        'update_id': update_id,
        'file_id': file_id,
        'next_id': next_id,
        'text': text,
        'prev_id': None
    })
    print('insertd new image {}'.format(item_id))
    return True


def get_latest_image():
    """ Returns the latest image received """
    db = TinyDB('database.json')
    od = sorted(db.all(), key=lambda k: k['item_id'])
    return od[-1]


def get_image(item_id):
    """ Returns the dict for a given id """
    db = TinyDB('database.json')
    entry = Query()
    return db.search(entry.item_id == item_id)[0]


def get_image_by_file_id(file_id):
    """ Returns the dict for a given file id """
    db = TinyDB('database.json')
    entry = Query()
    return db.search(entry.file_id == file_id)[0]

from database import get_latest_image, get_image, get_image_by_file_id
from fastapi import FastAPI, Response
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# create app
app = FastAPI()

# CORS related stuff to allow CROSS-ORIGINS as the Backend/Frontend is hosted on the same server
# Since we use it only in local network, this should not be a problem!
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
headers = {}


@app.get('/')
def start():
    """ Start page, which returns latest image """
    content = {}
    try:
        content = get_latest_image()
    except IndexError as e:
        pass
    return JSONResponse(content=content, headers=headers)


@app.get('/{item_id}')
def get_item(item_id: int):
    """ Return Metadata about image, given it's id"""
    return JSONResponse(content=get_image(item_id), headers=headers)


@app.get('/image/{file_id}')
def get_image_file(file_id: str):
    """ Returning the actual file as a FileResponse """
    elem = get_image_by_file_id(file_id)
    return FileResponse(elem['filename'], headers=headers)

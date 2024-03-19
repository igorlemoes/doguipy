from nicegui import app, ui

import pages
from pages.stacks import *

app.add_media_files("/static/images", "images")

ui.run(title='DoGuiPy - Docker Gui Python', storage_secret='THIS_NEEDS_TO_BE_CHANGED', favicon='doguipy.ico', port=8088, uvicorn_logging_level='error', uvicorn_reload_excludes='.sqlite-journal', language='pt-BR')
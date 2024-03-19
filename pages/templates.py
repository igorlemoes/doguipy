from dotenv import load_dotenv
from fastapi.responses import RedirectResponse
from nicegui import app, ui

from models.models import User
from utils import funcs

from . import base


@ui.page('/templates')
def typebots_page() -> None:

    if not app.storage.user.get('authenticated', False):
        return RedirectResponse('/login')
    else:
        user = User.get_by_id(app.storage.user.get('id'))

    base.base()

    load_dotenv(override=False)
    
    def open_page(e, nome):
        ui.open('/form/'+nome)

    ui.label('Templates - Stacks').classes('text-2xl').style('color:gray')
        
    container = ui.row().classes('grid w-full grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4')
    with container:
    
        with ui.card().tight().classes('w-full cursor-pointer').on('click', lambda e:open_page(e, 'postgres')):
            ui.image('/static/images/postgres.jpg')
            with ui.card_section():
                ui.label('Postgres')
                
        with ui.card().tight().classes('w-full cursor-pointer').on('click', lambda e:open_page(e, 'builder')):
            ui.image('/static/images/builder.jpg')
            with ui.card_section():
                ui.label('Typebot Builder')
                
        with ui.card().tight().classes('w-full cursor-pointer').on('click', lambda e:open_page(e, 'viewer')):
            ui.image('/static/images/viewer.jpg')
            with ui.card_section():
                ui.label('Typebot Viewer')
                
        with ui.card().tight().classes('w-full cursor-pointer').on('click', lambda e:open_page(e, 'minio')):
            ui.image('/static/images/minio.jpg')
            with ui.card_section():
                ui.label('Minio')
                
        with ui.card().tight().classes('w-full cursor-pointer').on('click', lambda e:open_page(e, 'evolution')):
            ui.image('/static/images/evolution.jpg')
            with ui.card_section():
                ui.label('Evolution-API')
                
        with ui.card().tight().classes('w-full cursor-pointer').on('click', lambda e:open_page(e, 'mongo')):
            ui.image('/static/images/mongo.jpg')
            with ui.card_section():
                ui.label('MongoDB')
                                                       
        with ui.card().tight().classes('w-full cursor-pointer').on('click', lambda e:open_page(e, 'pgadmin')):
            ui.image('/static/images/pgadmin.jpg')
            with ui.card_section():
                ui.label('PgAdmin')

        with ui.card().tight().classes('w-full cursor-pointer').on('click', lambda e:open_page(e, 'mongoexpress')):
            ui.image('/static/images/mongoexpress.jpg')
            with ui.card_section():
                ui.label('MongoExpress')

        with ui.card().tight().classes('w-full cursor-pointer').on('click', lambda e:open_page(e, 'mysql')):
            ui.image('/static/images/mysql.jpg')
            with ui.card_section():
                ui.label('MySQL')
                
        with ui.card().tight().classes('w-full cursor-pointer').on('click', lambda e:open_page(e, 'adminer')):
            ui.image('/static/images/adminer.jpg')
            with ui.card_section():
                ui.label('Adminer')
                
        with ui.card().tight().classes('w-full cursor-pointer').on('click', lambda e:open_page(e, 'wordpress')):
            ui.image('/static/images/wordpress.jpg')
            with ui.card_section():
                ui.label('Wordpress')
                
        with ui.card().tight().classes('w-full cursor-pointer').on('click', lambda e:open_page(e, 'n8n')):
            ui.image('/static/images/n8n.jpg')
            with ui.card_section():
                ui.label('n8n')
        with ui.card().tight().classes('w-full cursor-pointer').on('click', lambda e:open_page(e, 'chatwoot')):
            ui.image('/static/images/chatwoot.jpg')
            with ui.card_section():
                ui.label('chatwoot')

        with ui.card().tight().classes('w-full cursor-pointer').on('click', lambda e:open_page(e, 'redis')):
            ui.image('/static/images/redis.jpg')
            with ui.card_section():
                ui.label('redis')

        with ui.card().tight().classes('w-full cursor-pointer').on('click', lambda e:open_page(e, 'nocobase')):
            ui.image('/static/images/nocobase.jpg')
            with ui.card_section():
                ui.label('nocobase')
                
        with ui.card().tight().classes('w-full cursor-pointer').on('click', lambda e:open_page(e, 'portainer')):
            ui.image('/static/images/portainer.jpg')
            with ui.card_section():
                ui.label('portainer')
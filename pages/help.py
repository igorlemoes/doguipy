from dotenv import load_dotenv
from fastapi.responses import RedirectResponse
from nicegui import app, ui

from models.models import User
from utils import funcs

from . import base


@ui.page('/help')
def typebots_page() -> None:

    if not app.storage.user.get('authenticated', False):
        return RedirectResponse('/login')
    else:
        user = User.get_by_id(app.storage.user.get('id'))

    base.base()

    load_dotenv(override=False)

    ui.label('Suporte - Material de apoio').classes('text-2xl').style('color:gray')
    
    container = ui.row().classes('flex w-full')
    with container:
        
        ui.markdown("""
            ##### Projeto DoGuiPy ![Open Source Love](https://badges.frapsoft.com/os/v3/open-source.svg)
            
            _Olá me chamo Igor Lemões, criador do DoGuiPy._

            _Logo abaixo esta um card que direciona para nosso canal no Youtube onde você poderá encontrar vídeos e tutoriais para a utilização do DoGuiPy._
            
            _Juntamente com o card do canal estou deixando alguns cursos e treinamentos pagos, que ajudam a manter este projeto._
            
            _Faça parte da nossa comunidade._
            
        """).classes('w-full text-gray-500')
            
        
        grid = ui.row().classes('grid w-full grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4')
        with grid:
        
            with ui.card().tight().classes('w-full cursor-pointer').on(type='click', handler=lambda e: ui.open('https://youtube.com/igorlemoesnegocios', True)):
                ui.image('/static/images/canal.jpg')
                with ui.card_section():
                    ui.label('Nosso Canal')
                    
            with ui.card().tight().classes('w-full cursor-pointer').on(type='click', handler=lambda e: ui.open('https://cursodetypebot.com.br', True)):
                ui.image('/static/images/cursodetypebot.jpg')
                with ui.card_section():
                    ui.label('Curso de Typebot - Curso Pago')
                    
            with ui.card().tight().classes('w-full cursor-pointer').on(type='click', handler=lambda e: ui.open('https://cursoden8n.com.br', True)):
                ui.image('/static/images/cursoden8n.jpg')
                with ui.card_section():
                    ui.label('Curso de N8N - Curso Pago')
                    
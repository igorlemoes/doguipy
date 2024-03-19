from fastapi.responses import RedirectResponse
from nicegui import app, ui

from models.models import User
from utils import funcs


@ui.page('/login')
def login_page() -> None:

    user = User.get_or_none(role = 'admin')
    
    if (not user):
        User.create(username='admin', email='admin@admin.com.br', password=funcs.make_password('admin'), use_groups=True)

    def try_login() -> None:  # local function to avoid passing username and password as arguments
        user = User.select().where(User.username == username.value)
        if user and funcs.check_password(password.value, user[0].password):
            user = user[0]
            app.storage.user.update({'id': user.id, 'username': user.username, 'authenticated': True})
            ui.open('/')
        else:
            ui.notify('Wrong username or password', color='negative')

    if app.storage.user.get('authenticated', False):
        return RedirectResponse('/painel')

    with ui.row().classes('flex w-full p-16'):
        with ui.column().classes('flex xl:w-1/5 lg:w-1/4 md:w-2/5 sm:w-3/5 w-full p-5 absolute-center'):
            with ui.row().classes('w-full justify-center'):
                ui.label('DoGuiPy').classes('text-3xl text-indigo-600 font-bold')
            with ui.card().classes('flex w-full p-10 justify-center bg-gray-200'):
                with ui.row().classes('flex w-full justify-center'):
                    username = ui.input('Username').on('keydown.enter', try_login).props('outlined dense bg-color=white').classes('w-full')
                    password = ui.input('Password', password=True, password_toggle_button=True).on('keydown.enter', try_login).props('outlined dense bg-color=white').classes('w-full')
                    ui.button('Entrar', on_click=try_login, color='indigo-600').style('color:white').classes('w-full')
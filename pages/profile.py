from nicegui import app, ui
from fastapi.responses import RedirectResponse
from . import base
from models.models import User
from utils import funcs

@ui.page('/profile')
def profile_page() -> None:

    if not app.storage.user.get('authenticated', False):
        return RedirectResponse('/login')
    
    user = User.get_by_id(app.storage.user.get('id'))

    base.base()

    def update_pass():
        if field_password.value == field_repeat.value:
            user.username = field_username.value
            user.password = funcs.make_password(field_password.value)
            user.save()
            ui.notify('Usuário e senha atualizados com sucesso!', position='bottom-right', type='positive')

    def save():
            user.firstname = field_firstname.value
            user.lastname = field_lastname.value
            user.save()
            ui.notify('Perfil atualizado com sucesso!', position='bottom-right', type='positive')

    @ui.refreshable
    def update_button():
        btn_update.visible = True
        btn_update.enabled = len(field_username.value) < 50 and len(field_username.value) > 3 and len(field_password.value) < 50 and len(field_password.value) > 3 and field_password.value == field_repeat.value
    

    class valid_form():

        validation_rules = {
            'size': {'Tamanho mínimo 4 caracteres': lambda value: len(value) < 50 and len(value) > 3}
        }

        def __init__(self, e) -> None:
            self.field = e.sender
            self.valor = self.field.value
            self.valid = self.field.validation

        def focusout(self, type):
                self.field.validation = self.validation_rules[type]
                self.field.value = ''
                self.field.value = self.valor
                self.field.update()

                update_button()

        def click(self):
            self.field.validation = {}
            btn_update.enabled = False

    with ui.row().classes('w-full justify-center'):
         ui.label('Edite Suas Informações De Perfil').classes('text-2xl').style('color:gray')
    with ui.row().classes('w-full justify-center'):
        with ui.column().classes('w-full lg:w-1/3 p-10 bg-gray-200'):
            field_username  = ui.input('Nome de usuário', value=user.username).props('outlined dense bg-color=white').classes('w-full').on('focusout', lambda e: (valid_form(e).focusout('size'), funcs.slug(e))).on('click', lambda e: valid_form(e).click())
            field_password  = ui.input('Nova Senha', value='', password=True, password_toggle_button=True).props('outlined dense bg-color=white').classes('w-full').on('focusout', lambda e: valid_form(e).focusout('size')).on('click', lambda e: valid_form(e).click())
            field_repeat    = ui.input('Repetir', value='', password=True, password_toggle_button=True).props('outlined dense bg-color=white').classes('w-full').on('focusout', lambda e: valid_form(e).focusout('size')).on('click', lambda e: valid_form(e).click())
            with ui.row().classes('flex w-full justify-end'):
                btn_update = ui.button('Alterar', on_click=update_pass, color='emerald-600').style('color:white')
                update_button()
            ui.separator()
            field_firstname = ui.input('Primeiro Nome', value=user.firstname).props('outlined dense bg-color=white').classes('w-full')
            field_lastname  = ui.input('Último Nome', value=user.lastname).props('outlined dense bg-color=white').classes('w-full')
            with ui.row().classes('flex w-full justify-end'):
                btn_save = ui.button('Salvar', on_click=save, color='emerald-600').style('color:white')
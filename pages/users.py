import os
from dotenv import load_dotenv
from fastapi.responses import RedirectResponse

from models.models import User
from nicegui import app, ui
from utils import funcs

from . import base


@ui.page('/users')
def users_page() -> None:

    if not app.storage.user.get('authenticated', False):
        return RedirectResponse('/login')
    else:
        user = User.get_by_id(app.storage.user.get('id'))

    base.base()

    load_dotenv(override=False)

    def clear_fields():
            field_id.value = ''
            #clear name
            copy_validation = field_username.validation
            field_username.validation = {}
            field_username.value = ''
            field_username.validation = copy_validation
            #clear url
            copy_validation = field_password.validation
            field_password.validation = {}
            field_password.value = ''
            field_password.validation = copy_validation
            #clear url
            copy_validation = field_email.validation
            field_email.validation = {}
            field_email.value = ''
            field_email.validation = copy_validation
            # btn_edit.visible = False
            btn_save.visible = True

    def user_create():

        User.create(username=field_username.value, email=field_email.value, password=funcs.make_password(field_password.value), role=field_role.value.lower())
        clear_fields()
        get_table()

    def user_delete(e):
        user_new = User.get_by_id(e.args['id'])
        user_new.delete_instance()
        clear_fields()
        get_table()
         
        
            
    def get_table():
        container.clear()
        with container:
            rows = list(User.select().dicts())

            columns = [
            {'name': 'username', 'label': 'Nome De Usuário', 'field': 'username', 'sortable': False, 'align': 'left'},
            {'name': 'email', 'label': 'Email', 'field': 'email', 'sortable': False, 'align': 'left'},
            {'name': 'firstname', 'label': 'Nome', 'field': 'firstname', 'sortable': False, 'align': 'left'},
            {'name': 'lastname', 'label': 'Sobrenome', 'field': 'lastname', 'sortable': False, 'align': 'left'},
            {'name': 'actions', 'label': 'Ações'},
            ]
            
            table = ui.table(columns=columns, rows=rows, row_key='id', pagination=5).classes('w-full')
            table.on('func_conn_delete_row', lambda e:user_delete(e))
            table.add_slot('header', r'''
                <q-tr :props="props">
                    <q-th v-for="col in props.cols" :key="col.name" :props="props">
                        {{ col.label }}
                    </q-th>
                </q-tr>
            ''')
            
            table.add_slot('body-cell-actions', r'''
                <q-td auto-width key="actions" :props="props">
                    <q-btn size="sm" text-color="white" color="rose-600"
                        @click="$parent.$emit('func_conn_delete_row', props.row)"
                        :icon="'delete'">
                        <q-tooltip class="bg-black">Excluir Typebot.</q-tooltip>
                    </q-btn>
                </q-td>
            ''')

    @ui.refreshable
    def save_button():
            btn_save.visible = True
            btn_save.enabled = True

    ui.label('Gerenciamento De Usuários').classes('text-2xl').style('color:gray')

    with ui.row().classes('w-full'):
        with ui.column().classes('w-full p-5 bg-gray-200'):
        
            field_id = ui.input().classes('hidden')
            
            with ui.row().classes('flex w-full'):
                field_username  = ui.input(label='Nome de usuário', placeholder='Digite aqui').props('outlined dense bg-color=white').classes('w-full md:w-auto md:grow')
                field_password  = ui.input(label='Senha', placeholder='Digite aqui', password=True, password_toggle_button=True).props('outlined dense bg-color=white').classes('w-full md:w-auto md:grow')
            
            with ui.row().classes('flex w-full'):
                field_email     = ui.input(label='Email', placeholder='Digite aqui').props('outlined dense bg-color=white').classes('w-full md:w-auto md:grow')
                field_role      = ui.select({'admin': 'Admin', 'editor':'Editor', 'cliente':'Cliente'}).props('outlined dense bg-color=white').classes('w-full md:w-auto md:grow')     

            with ui.row().classes('flex w-full justify-end'):
                btn_save = ui.button('Salvar Usuário', on_click=user_create, color='emerald-600').style('color:white')
                save_button()
        
        container = ui.row().classes('w-full')
        
        get_table()
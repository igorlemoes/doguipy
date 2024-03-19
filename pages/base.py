from nicegui import app, ui

from models.models import User


def base():

    ui.query('textarea').style('line-height: 24px')

    user = User.get_by_id(app.storage.user.get('id'))
    
    with ui.header(elevated=True).classes('bg-indigo-600 justify-between'):
        with ui.row().classes('items-end justify-start'):
            ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat text-color=white')
            ui.label("DoGuiPy").classes('text-2xl')
        with ui.row().classes('items-end justify-end'):
            ui.label(user.firstname +' '+ user.lastname if user.lastname else user.firstname if user.firstname else user.username).classes('text-lg')
            with ui.button(icon='manage_accounts', color='indigo-400'):
                with ui.menu().classes('items-end justify-end'):
                    ui.menu_item('Usuário: '+user.username)
                    ui.menu_item('Editar Perfil',on_click=lambda: (ui.open('/profile')))
                    ui.separator()
                    ui.menu_item('Sair',on_click=lambda: (app.storage.user.clear(), ui.open('/login')), auto_close=False).props('flat text-color=white bg-color=rose-600')


    with ui.left_drawer().classes('bg-indigo-400 relative') as left_drawer:
        ui.button('Containers',on_click=lambda: (ui.open('/')), icon='list_alt', color='indigo-600').props('unelevated text-color=white').classes('w-full py-3')
        ui.button('Templates',on_click=lambda: (ui.open('/templates')), icon='view_module', color='indigo-600').props('unelevated text-color=white').classes('w-full py-3')
        ui.button('Configurações',on_click=lambda: (ui.open('/settings')), icon='settings', color='indigo-600').props('unelevated text-color=white').classes('w-full py-3')

        if user.role == 'admin':
            with ui.row().classes('w-full fixed bottom-0 left-0'):
                ui.button('Ajuda',on_click=lambda: (ui.open('/help')), icon='contact_support', color='rose-700').props('unelevated text-color=white').classes('w-full m-4 py-3')
                # ui.button('Usuários',on_click=lambda: (ui.open('/users')), color='indigo-600').props('unelevated text-color=white').classes('w-full m-4 py-3')

    # with ui.page_sticky(position='bottom-left', x_offset=-280, y_offset=20).style('z-index: 9999'):
    #     ui.button(on_click=lambda: (ui.open('/')), icon='contact_support', color='rose-700').props('fab text-color=white')

    with ui.footer(value=True).style('background-color: #333') as footer:
        ui.label('Igor Lemões - DoGuiPy - © Todos os direitos reservados.').classes('flex w-full justify-center')
            
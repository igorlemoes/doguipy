from nicegui import run, ui
from python_on_whales import docker

from ..modal import Modal
from . import (adminer, chatwoot, evolution, minio, mongo, mongoexpress, mysql,
               n8n, nocobase, pgadmin, portainer, postgres, redis, typebot,
               wordpress)


def run_stop(modal, id):
    docker.container.stop(id)
    modal.close()
        
async def stop_container(id):
    modal = Modal('Parando Container...')
    modal.open()
    modal.spinner()
    await run.io_bound(run_stop, modal, id)
    ui.open('/')
    
def run_start(modal, id):
    docker.container.start(id)
    modal.close() 
    
async def start_container(id):
    modal = Modal('Iniciando Container...')
    modal.open()
    modal.spinner()
    await run.io_bound(run_start, modal, id)
    ui.open('/')

def run_remove(modal, id, name):
    docker.container.remove(id, force=True, volumes=True)
    docker.volume.remove(docker.volume.list(filters=dict(name=name)))
    modal.close()

async def remove_container(id, name):
    modal = Modal('Removendo Container...')
    modal.open()
    modal.spinner()
    await run.io_bound(run_remove, modal, id, name)
    ui.open('/')


async def func_deploy(template_deploy=None, default_id=None, default_image=None, default_name=None, default_domain=None, default_port=None, default_envs=None):
    modal = Modal('Subindo container...')
    modal.open()
    modal.spinner()

    if template_deploy == 'evolution':
        await run.io_bound(evolution.deploy_evolution, modal, default_id, default_image, default_name, default_domain, default_port, default_envs)
        ui.open('/')
        
    if template_deploy == 'postgres':
        await run.io_bound(postgres.deploy_postgres, modal, default_id, default_image, default_name, default_domain, default_port, default_envs)
        ui.open('/')

    if template_deploy == 'builder':
        await run.io_bound(typebot.deploy_builder, modal, default_id, default_image, default_name, default_domain, default_port, default_envs)
        ui.open('/')

    if template_deploy == 'viewer':
        await run.io_bound(typebot.deploy_viewer, modal, default_id, default_image, default_name, default_domain, default_port, default_envs)
        ui.open('/')

    if template_deploy == 'minio':
        await run.io_bound(minio.deploy_minio, modal, default_id, default_image, default_name, default_domain, default_port, default_envs)
        ui.open('/')

    if template_deploy == 'pgadmin':
        await run.io_bound(pgadmin.deploy_pgadmin, modal, default_id, default_image, default_name, default_domain, default_port, default_envs)
        ui.open('/')

    if template_deploy == 'mongo':
        await run.io_bound(mongo.deploy_mongo, modal, default_id, default_image, default_name, default_domain, default_port, default_envs)
        ui.open('/')

    if template_deploy == 'mongoexpress':
        await run.io_bound(mongoexpress.deploy_mongoexpress, modal, default_id, default_image, default_name, default_domain, default_port, default_envs)
        ui.open('/')

    if template_deploy == 'mysql':
        await run.io_bound(mysql.deploy_mysql, modal, default_id, default_image, default_name, default_domain, default_port, default_envs)
        ui.open('/')
        
    if template_deploy == 'adminer':
        await run.io_bound(adminer.deploy_adminer, modal, default_id, default_image, default_name, default_domain, default_port, default_envs)
        ui.open('/')
        
    if template_deploy == 'wordpress':
        await run.io_bound(wordpress.deploy_wordpress, modal, default_id, default_image, default_name, default_domain, default_port, default_envs)
        ui.open('/')
        
    if template_deploy == 'n8n':
        await run.io_bound(n8n.deploy_n8n, modal, default_id, default_image, default_name, default_domain, default_port, default_envs)
        ui.open('/')  

    if template_deploy == 'chatwoot':
        await run.io_bound(chatwoot.deploy_chatwoot, modal, default_id, default_image, default_name, default_domain, default_port, default_envs)
        ui.open('/')

    if template_deploy == 'redis':
        await run.io_bound(redis.deploy_redis, modal, default_id, default_image, default_name, default_domain, default_port, default_envs)
        ui.open('/')
    
    if template_deploy == 'nocobase':
        await run.io_bound(nocobase.deploy_nocobase, modal, default_id, default_image, default_name, default_domain, default_port, default_envs)
        ui.open('/') 
        
    if template_deploy == 'portainer':
        await run.io_bound(portainer.deploy_portainer, modal, default_id, default_image, default_name, default_domain, default_port, default_envs)
        ui.open('/')
        
        
def get_fields(template_deploy=None, default_id=None, default_image=None, default_status=None, default_name=None, default_domain=None, default_port=None, default_envs=None):

    ui.query('textarea').style('line-height: 24px')
        
    with ui.column().classes('w-full p-5 bg-gray-200'):
    
        field_id = ui.input(value=default_id).classes('hidden')
        
        with ui.row().classes('flex w-full'):
            field_image = ui.input(label='Imagem/Docker', value=default_image, placeholder='Digite aqui').props('outlined dense bg-color=white').classes('w-full md:w-auto md:grow')

        with ui.row().classes('flex w-full'):
            field_name = ui.input(label='Nome', value=default_name, placeholder='Digite aqui').props('outlined dense bg-color=white').classes('w-full md:w-auto md:grow')
        
        with ui.row().classes('flex w-full'):
            field_domain = ui.input(label='Domínio', value=default_domain, placeholder='Digite aqui').props('outlined dense bg-color=white').classes('w-full md:w-auto md:grow')
            field_port  = ui.input(label='Porta', value=default_port, placeholder='Digite aqui').props('outlined dense bg-color=white').classes('w-full md:w-1/6')
        
        with ui.row().classes('flex w-full'):
            field_enviroments = ui.textarea(label='Variáveis de ambiente', value=str(default_envs), placeholder='Digite aqui').props('outlined dense bg-color=white spellCheck=false').classes('w-full md:w-auto md:grow')
            
        with ui.row().classes('flex w-full justify-between'):
            with ui.row().classes('flex justify-start'):
                if default_status == 'running':
                    ui.button('Parar', on_click=lambda e: stop_container(field_id.value), icon='stop', color='rose-600').style('color:white')
                if default_status == 'exited':
                    ui.button('Iniciar', on_click=lambda e: start_container(field_id.value), icon='play_arrow', color='emerald-600').style('color:white')
            with ui.row().classes('flex justify-end'):
                ui.button('Deploy', icon='file_upload', on_click=lambda e: func_deploy(template_deploy, default_id=field_id.value, default_image=field_image.value, default_name=field_name.value, default_domain=field_domain.value, default_port=field_port.value, default_envs=field_enviroments.value), color='emerald-600').style('color:white')
                
                with ui.dialog() as dialog, ui.card():
                    ui.label('Você realmente deseja excluir completamente os dados deste container ?')
                    with ui.row().classes('flex w-full justify-between'):
                        with ui.row().classes('flex justify-start'):
                            ui.button('Sim', on_click=lambda e: remove_container(default_id, default_name), icon='check_circle', color='red-600').style('color:white')
                        with ui.row().classes('flex justify-end'):
                            ui.button('Não', on_click=dialog.close, icon='not_interested', color='emerald-600').style('color:white')

                ui.button('Excluir', on_click=dialog.open, icon='delete', color='rose-600').style('color:white')

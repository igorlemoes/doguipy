import os
import subprocess

from dotenv import load_dotenv
from fastapi.responses import RedirectResponse
from git import Repo, cmd
from nicegui import app, run, ui
from packaging import version
from python_on_whales import docker

from models.models import User
from up_traefik import container_deploy
from utils import funcs

from . import base
from .modal import Modal


def list_all_tags_for_remote_git_repo(repo_url):

    result = subprocess.run([
        "git", "ls-remote", "--tags", repo_url
    ], stdout=subprocess.PIPE, text=True)

    output_lines = result.stdout.splitlines()
    tags = [
        line.split("refs/tags/")[-1] for line in output_lines
        if "refs/tags/" in line and "^{}" not in line
    ]
    return tags


@ui.page('/settings')
def users_page() -> None:

    repo_url = 'https://github.com/igorlemoes/doguipy'
        
    local_dir = os.path.dirname(os.path.dirname(__file__))

    repo = Repo(local_dir)

    if not app.storage.user.get('authenticated', False):
        return RedirectResponse('/login')
    else:
        user = User.get_by_id(app.storage.user.get('id'))

    base.base()

    load_dotenv(override=False)
    

    async def git_update():
 
        modal = Modal('Atualizando DoGuiPy')
        modal.open()
        modal.spinner()

        await run.io_bound(repo.remotes.origin.pull)
        
        modal.close()
        
        ui.open('/settings')
        
    async def deploy_traefik(field_port_expose):
     
        modal = Modal('Atualizando Traefik')
        modal.open()
        modal.spinner()
        
        await run.io_bound(docker.container.stop, 'traefik')
        
        await run.io_bound(docker.container.remove, 'traefik')

        await run.io_bound(container_deploy, field_port_expose)
        
        modal.close()

        ui.open('/settings')
        

    ui.label('Configurações de sistema').classes('text-2xl').style('color:gray')

    with ui.row().classes('w-full'):
        
        with ui.column().classes('w-full p-5 bg-gray-200'):
            
            with ui.row().classes('flex w-full'):
                
                ui.label('Versão atual do DoGuiPy - ' + str(sorted(repo.tags, key=lambda t: t.commit.committed_datetime)[-1])).classes('text-lg').style('color:gray')
                
                version_local = str(sorted(repo.tags, key=lambda t: t.commit.committed_datetime)[-1])
                
                version_remote = str(list_all_tags_for_remote_git_repo(repo_url=repo_url)[-1])
                
                if version.parse(version_local) < version.parse(version_remote):
                    with ui.row().classes('flex w-full'):
                        ui.label('Versão disponíel do Doguipy - ' + str(list_all_tags_for_remote_git_repo(repo_url=repo_url)[-1])).classes('text').style('color:#E11D47')
                                               
                with ui.row().classes('flex w-full'):        
                    ui.link(text='http://doguipy.'+os.environ.get('DOMAIN_BASE')+':8088', target='http://doguipy.'+os.environ.get('DOMAIN_BASE')+':8088', new_tab=True)
                                                              
                if version.parse(version_local) < version.parse(version_remote):
                    with ui.row().classes('flex w-full justify-end'):
                        ui.button('Atualizar Sistema', icon='refresh', on_click=lambda e: git_update(), color='emerald-600').style('color:white')
                else:
                    with ui.row().classes('flex w-full justify-end'):
                        ui.button('Sistema Atualizado', icon='refresh', color='emerald-600').props('disabled').style('color:white')

        

        with ui.column().classes('w-full p-5 bg-gray-200'):
            
            with ui.row().classes('flex w-full'):
                
                ui.label('Configurações do Traefik').classes('text-lg').style('color:gray')
                    
                
                with ui.row().classes('flex w-full justify-end'):
                    
                    value_port_expose = False
                    
                    try:
                        if docker.container.inspect('traefik').config.exposed_ports.get('8080/tcp') == {}:
                            value_port_expose = True
                    except:
                        pass
                            
                    field_port_expose = ui.switch('Expôr dashboard do Traefik - porta 8080', value=value_port_expose).props('color=emerald-600 outlined dense bg-color=white').classes('w-full md:w-auto md:grow')
                    
                    if value_port_expose:
                        with ui.row().classes('flex w-full'):        
                            ui.link(text='http://'+os.environ.get('DOMAIN_BASE')+':8080/dashboard', target='http://'+os.environ.get('DOMAIN_BASE')+':8080/dashboard', new_tab=True)
                                  
                                                   
                with ui.row().classes('flex w-full justify-end'):
                    ui.button('Deploy', icon='file_upload', on_click=lambda e: deploy_traefik(field_port_expose.value), color='emerald-600').style('color:white')        
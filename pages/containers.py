import os

from dotenv import load_dotenv
from fastapi.responses import RedirectResponse
from nicegui import app, run, ui
from python_on_whales import docker
from slugify import slugify

from models.models import User
from pages.stacks import fields

from . import base
from .modal import Modal


@ui.page('/')
def typebots_page() -> None:

    if not app.storage.user.get('authenticated', False):
        return RedirectResponse('/login')
    else:
        user = User.get_by_id(app.storage.user.get('id'))

    base.base()

    load_dotenv(override=False)
    
    def run_stop(modal, id):
        docker.container.stop(id)
        modal.close()
         
    async def stop_container(e):
        modal = Modal('Parando Container...')
        modal.open()
        modal.spinner()
        await run.io_bound(run_stop, modal, e.args['id'])
        ui.open('/')
     
    def run_start(modal, id):
        docker.container.start(id)
        modal.close() 
        
    async def start_container(e):
        modal = Modal('Iniciando Container...')
        modal.open()
        modal.spinner()
        await run.io_bound(run_start, modal, e.args['id'])
        ui.open('/')

    def show_container(e):
        try:
            inspect = docker.container.inspect(e.selection[0]['id'])
            
            if inspect.config.labels.get('traefik.http.services.'+inspect.name+'_storage.loadbalancer.server.port'):
                port = inspect.config.labels.get('traefik.http.services.'+inspect.name+'_storage.loadbalancer.server.port')
            else:
                if inspect.config.labels.get('traefik.http.services.'+inspect.name+'.loadbalancer.server.port'):
                    port  = inspect.config.labels.get('traefik.http.services.'+inspect.name+'.loadbalancer.server.port')
                else:
                    port  = inspect.config.labels.get('traefik.tcp.services.'+inspect.name+'.loadbalancer.server.port')
            
            container_fields.clear()
            default_envs = ''
            for env in inspect.config.env:
                default_envs += env + '\n'

            with container_fields:
                if 'evolution'in inspect.config.image:
                    fields.get_fields(template_deploy='evolution', default_id=e.selection[0]['id'], default_image=inspect.config.image, default_status=inspect.state.status, default_name=e.selection[0]['name'], default_domain=e.selection[0]['domainname'], default_port=port,  default_envs=default_envs)
                if 'builder'in inspect.config.image:
                    fields.get_fields(template_deploy='builder', default_id=e.selection[0]['id'], default_image=inspect.config.image, default_status=inspect.state.status, default_name=e.selection[0]['name'], default_domain=e.selection[0]['domainname'], default_port=port, default_envs=default_envs)
                if 'viewer'in inspect.config.image:
                    fields.get_fields(template_deploy='viewer', default_id=e.selection[0]['id'], default_image=inspect.config.image, default_status=inspect.state.status, default_name=e.selection[0]['name'], default_domain=e.selection[0]['domainname'], default_port=port, default_envs=default_envs)
                if 'minio'in inspect.config.image:
                    fields.get_fields(template_deploy='minio', default_id=e.selection[0]['id'], default_image=inspect.config.image, default_status=inspect.state.status, default_name=e.selection[0]['name'], default_domain=e.selection[0]['hostname'], default_port=port, default_envs=default_envs)
                if 'postgres'in inspect.config.image:
                    fields.get_fields(template_deploy='postgres', default_id=e.selection[0]['id'], default_image=inspect.config.image, default_status=inspect.state.status, default_name=e.selection[0]['name'], default_domain=e.selection[0]['domainname'], default_port=port, default_envs=default_envs)
                if 'pgadmin'in inspect.config.image:
                    fields.get_fields(template_deploy='pgadmin', default_id=e.selection[0]['id'], default_image=inspect.config.image, default_status=inspect.state.status, default_name=e.selection[0]['name'], default_domain=e.selection[0]['domainname'], default_port=port, default_envs=default_envs)
                if 'mongo:'in inspect.config.image:
                    fields.get_fields(template_deploy='mongo', default_id=e.selection[0]['id'], default_image=inspect.config.image, default_status=inspect.state.status, default_name=e.selection[0]['name'], default_domain=e.selection[0]['domainname'], default_port=port, default_envs=default_envs)
                if 'mongo-express:'in inspect.config.image:
                    fields.get_fields(template_deploy='mongoexpress', default_id=e.selection[0]['id'], default_image=inspect.config.image, default_status=inspect.state.status, default_name=e.selection[0]['name'], default_domain=e.selection[0]['domainname'], default_port=port, default_envs=default_envs)
                if 'mysql:'in inspect.config.image:
                    fields.get_fields(template_deploy='mysql', default_id=e.selection[0]['id'], default_image=inspect.config.image, default_status=inspect.state.status, default_name=e.selection[0]['name'], default_domain=e.selection[0]['domainname'], default_port=port, default_envs=default_envs)
                if 'adminer:'in inspect.config.image:
                    fields.get_fields(template_deploy='adminer', default_id=e.selection[0]['id'], default_image=inspect.config.image, default_status=inspect.state.status, default_name=e.selection[0]['name'], default_domain=e.selection[0]['domainname'], default_port=port, default_envs=default_envs)
                if 'wordpress:'in inspect.config.image:
                    fields.get_fields(template_deploy='wordpress', default_id=e.selection[0]['id'], default_image=inspect.config.image, default_status=inspect.state.status, default_name=e.selection[0]['name'], default_domain=e.selection[0]['domainname'], default_port=port, default_envs=default_envs)
                if 'n8nio/n8n:'in inspect.config.image:
                    fields.get_fields(template_deploy='n8n', default_id=e.selection[0]['id'], default_image=inspect.config.image, default_status=inspect.state.status, default_name=e.selection[0]['name'], default_domain=e.selection[0]['domainname'], default_port=port, default_envs=default_envs)
                if 'chatwoot/chatwoot:'in inspect.config.image:
                    fields.get_fields(template_deploy='chatwoot', default_id=e.selection[0]['id'], default_image=inspect.config.image, default_status=inspect.state.status, default_name=e.selection[0]['name'], default_domain=e.selection[0]['domainname'], default_port=port, default_envs=default_envs)                    
                if 'redis:'in inspect.config.image:
                    fields.get_fields(template_deploy='redis', default_id=e.selection[0]['id'], default_image=inspect.config.image, default_status=inspect.state.status, default_name=e.selection[0]['name'], default_domain=e.selection[0]['domainname'], default_port=port, default_envs=default_envs)                    
                if 'nocobase/nocobase:'in inspect.config.image:
                    fields.get_fields(template_deploy='nocobase', default_id=e.selection[0]['id'], default_image=inspect.config.image, default_status=inspect.state.status, default_name=e.selection[0]['name'], default_domain=e.selection[0]['domainname'], default_port=port, default_envs=default_envs)                    
                if 'portainer/portainer-ce:'in inspect.config.image:
                    fields.get_fields(template_deploy='portainer', default_id=e.selection[0]['id'], default_image=inspect.config.image, default_status=inspect.state.status, default_name=e.selection[0]['name'], default_domain=e.selection[0]['domainname'], default_port=port, default_envs=default_envs)                    
        
        
        except:
            container_fields.clear()
            
    async def get_content(modal):
        container_table.clear()
        with container_table:
            result = []
            categories = await run.io_bound(docker.container.list, all=True)
            for i,t in enumerate(categories):
                inspect = await run.io_bound(docker.container.inspect, t.id)
                
                domainname = ''
                
                if inspect.config.domainname != '':
                    domainname = 'https://'+inspect.config.domainname
                    if 'minio'in inspect.config.image:
                        domainname = 'https://login.'+inspect.config.domainname
                        
                if inspect.config.hostname != '':
                    hostname = 'https://'+inspect.config.hostname
                    
                if t.name != 'doguipy' and t.name != 'traefik':
                
                    result.append(
                            {
                            'id': t.id,
                            'name':t.name,
                            'status': inspect.state.status,
                            'hostname': hostname,
                            'domainname': domainname,
                            }
                        )

            rows = result

            columns = [
            {'name': 'name', 'label': 'Nome', 'field': 'name', 'sortable': False, 'align': 'left'},
            {'name': 'domainname', 'label': 'Link', 'field': 'domainname', 'sortable': False, 'align': 'left'},
            {'name': 'actions', 'label': 'Ações', 'sortable': False, 'align': 'right'},
            ]
            
            table = ui.table(columns=columns, rows=rows, row_key='id', selection='single', pagination=15, on_select=lambda e:show_container(e)).classes('w-full')
            # table = ui.table(columns=columns, rows=rows, row_key='id', selection='single', pagination=5).classes('w-full')
            table.on('func_show_container', lambda e:show_container(e))
            table.on('func_start_container', lambda e:start_container(e))
            table.on('func_stop_container', lambda e:stop_container(e))
            table.add_slot('header', r'''
                <q-tr :props="props">
                    <q-th auto-width ></q-th>
                    <q-th v-for="col in props.cols" :key="col.name" :props="props">
                        {{ col.label }}
                    </q-th>
                </q-tr>
            ''')
            table.add_slot('body-cell-domainname', r'''
                <q-td key="domainname" :props="props">
                    <a :href=props.row.domainname target="_blank">{{props.row.domainname}}</a>
                </q-td>
            ''')
            table.add_slot('body-cell-actions', r'''
                <q-td auto-width key="actions" :props="props">
                           
                    <!------------------- TRECHO COMENTADO ---------------------
                    <q-btn size="sm" text-color="white" color="indigo-600"
                        @click="$parent.$emit('func_show_container', props.row)"
                        :icon="'visibility'">
                        <q-tooltip class="bg-black">Show Inspect</q-tooltip>
                    </q-btn>
                    &nbsp
                    --!>
                           
                    <q-btn v-if="props.row.status == 'exited'" size="sm" text-color="white" color="emerald-600"
                        @click="$parent.$emit('func_start_container', props.row)"
                        :icon="'play_arrow'">
                        <q-tooltip class="bg-black">Iniciar Container</q-tooltip>
                    </q-btn>
                    &nbsp
                    <q-btn v-else size="sm" text-color="white" color="rose-600"
                        @click="$parent.$emit('func_stop_container', props.row)"
                        :icon="'stop'">
                        <q-tooltip class="bg-black">Parar Container</q-tooltip>
                    </q-btn>
                </q-td>
            ''')
            
        modal.close()

    async def get_table():
        modal = Modal('Carregando Containers...')
        modal.open()
        modal.spinner()
        await get_content(modal)


    ui.label('Containers - '+os.environ.get('DOMAIN_BASE')).classes('text-2xl').style('color:gray')

    container_fields = ui.row().classes('w-full')
        
    container_table = ui.row().classes('w-full')
    
    ui.timer(0.0, get_table, active=True, once=True)
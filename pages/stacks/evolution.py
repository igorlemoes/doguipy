import os
from urllib.parse import urlparse

from dotenv import load_dotenv
from fastapi.responses import RedirectResponse
from nicegui import app, ui
from python_on_whales import docker
from slugify import slugify

from models.models import User

from .. import base
from . import fields


def deploy_evolution(modal, default_id=None, default_image=None, default_name=None, default_domain=None, default_port=None, default_envs=None):
        
        if default_id:
            docker.container.stop(default_id)
            
            docker.container.remove(default_id)

        envs = {}
        
        
        try:
            for line in default_envs.strip().split("\n"):
                if line.split("=")[1].lower() == 'false' or line.split("=")[1].lower() == 'true':
                    envs[line.split("=")[0]] = 'false' if line.split("=")[1].lower() == 'false' else 'true'
                else:
                    envs[line.split("=")[0]] = line.split("=")[1]
                    
        except:
            pass


        ####################   Evolution Api   ####################
        var_domain      = urlparse(default_domain).hostname
        var_default     = os.environ.get('DOMAIN_BASE')
        var_image       = default_image
        var_name        = slugify(default_name)
        var_entrypoint  = 'http'
        var_ssl         = True

        if var_entrypoint == 'http':
            if var_domain:
                var_host = "Host(`"+var_domain+"`)"
            else:
                var_host = "Host(`"+var_name+"."+var_default+"`)"
                var_domain = var_name+"."+var_default
                
        else:
            var_host    = "HostSNI(`*`)"
            
        if var_ssl:
            var_entry   = 'websecure'
        else:
            var_entry   = 'web'
            
        var_port        = default_port if default_port else 8080
        var_envs        = envs
        var_volumes     = [
            (var_name+"_instances","/evolution/instances"),
            (var_name+"_store","/evolution/store"),
            ]

        
        created = docker.run(
            detach=True,
            image=var_image,
            name=var_name,
            hostname=var_domain,
            domainname=var_domain,
            restart='always',
            labels={
                "traefik.enable":"true",
                "traefik."+var_entrypoint+".routers."+var_name+".rule":var_host,
                "traefik."+var_entrypoint+".routers."+var_name+".entrypoints":var_entry,
                "traefik."+var_entrypoint+".services."+var_name+".loadbalancer.server.port":var_port,
                "traefik."+var_entrypoint+".routers."+var_name+".tls.certresolver":"le",
                # "traefik."+var_entrypoint+".services."+var_name+".service":var_name,
            },
            networks=['traefik_public'],
            envs=var_envs,
            volumes=var_volumes
        )

        modal.close()


@ui.page('/form/evolution')
def form_evolution() -> None:

    if not app.storage.user.get('authenticated', False):
        return RedirectResponse('/login')
    else:
        user = User.get_by_id(app.storage.user.get('id'))

    base.base()

    load_dotenv(override=False)

    default_image = 'atendai/evolution-api:v1.6.1'
    
    default_envs = """AUTHENTICATION_API_KEY=coloque_uma_secret_key_de_32_car
DATABASE_ENABLED=False
DATABASE_CONNECTION_URI=mongodb://mongo_usuario:mongo_senha@monbodb:27017
DATABASE_CONNECTION_DB_PREFIX_NAME=evolution"""
        
    ui.query('textarea').style('line-height: 24px')

    ui.label('Formulário Evolution-API').classes('text-2xl').style('color:gray')
    
    container_fields = ui.row().classes('w-full')
    
    with container_fields:
        fields.get_fields(template_deploy='evolution', default_image=default_image, default_envs=default_envs)
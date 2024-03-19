import os

from dotenv import load_dotenv
from python_on_whales import docker

load_dotenv(override=False)

try:
    docker.network.create('traefik_public')
except:
    # docker.network.remove('traefik_public')
    pass

def container_deploy():

    img_doguipy = docker.build(
        context_path=".",
        tags="igorlemoes/doguipy"
    )

    try:

        doguipy = docker.run(
            detach=True,
            image=img_doguipy,
            name="doguipy",
            domainname="doguipy."+os.environ.get('DOMAIN_BASE'),
            restart='always',
            labels={
                "traefik.enable":"true",
                "traefik.http.routers.doguipy.rule":"Host(`doguipy."+os.environ.get('DOMAIN_BASE')+"`)",
                "traefik.http.routers.doguipy.entrypoints":"websecure",
                "traefik.http.services.doguipy.loadbalancer.server.port":8088,
                "traefik.http.routers.doguipy.tls.certresolver":"le",
                "traefik.http.routers.doguipy.service":"doguipy",
            },
            publish=[("8088","8088")],
            networks=['traefik_public'],
            volumes=[
                ("/var/run/docker.sock","/var/run/docker.sock:ro"),
                (os.path.abspath(os.path.dirname(__file__)),"/doguipy"),
                ]
        )

    except:
        pass

if __name__ == '__main__':
    container_deploy()
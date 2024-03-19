import os

from dotenv import load_dotenv
from python_on_whales import docker

load_dotenv(override=False)

try:
    docker.network.create('traefik_public')
except:
    # docker.network.remove('traefik_public')
    pass

def container_deploy(publish_port = None):
        
    ports = [("80","80"), ("443","443")]
    
    if publish_port:
    
        ports = [("80","80"), ("443","443"),("8080","8080")]
        

    var_commands_traefik = [
        "--providers.docker=true",
        "--entrypoints.web.address=:80",
        "--entrypoints.websecure.address=:443",
        "--providers.docker.exposedbydefault=false",
        # - --providers.docker.swarmMode=true
        # # Defina a mesma rede que você criou para o traefik
        "--providers.docker.network=traefik_public",
        "--providers.docker.endpoint=unix:///var/run/docker.sock",
        # # Config para SSL Lets Encrypt
        # # altere para seu e-mail
        "--certificatesresolvers.le.acme.httpchallenge.entrypoint=web",
        "--certificatesresolvers.le.acme.email="+os.environ.get('EMAIL_SSL'),
        "--certificatesresolvers.le.acme.storage=/letsencrypt/acme.json",
        "--certificatesresolvers.le.acme.tlschallenge=true",
        # # Global HTTP -> HTTPS
        "--entrypoints.web.http.redirections.entryPoint.to=websecure",
        "--entrypoints.web.http.redirections.entryPoint.scheme=https",
        "--api.insecure=true",
        "--log.level=DEBUG",
    ]

    var_volumes_traefik = [
        ("traefik_certificates","/letsencrypt"),
        ("/var/run/docker.sock","/var/run/docker.sock:ro"),
        ]

    try:

        traefik = docker.run(
            detach=True,
            image='traefik:latest',
            name='traefik',
            command=var_commands_traefik,
            restart='always',
            publish=ports,
            volumes=var_volumes_traefik,
            networks=['traefik_public'],
        )

    except:
        pass
    
if __name__ == '__main__':
    container_deploy()

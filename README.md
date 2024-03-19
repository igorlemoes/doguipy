# DoGuiPy
Painel que utiliza Python com uma UI Nicegui para gerenciar ferramentas e containers do Docker.

## Projeto DoGuiPy ![Open Source Love](https://badges.frapsoft.com/os/v3/open-source.svg)

Este é um projeto de código aberto, que tem como objetivo facilitar a utilização do Docker em projetos de pequeno e médio porte.

Utilizando o DoGuiPy você será capaz de instalar alguns containers do docker que estão pré configurados no DoGuiPy para trabalhar juntamente com o Traefik, o que facilita a ligação do proxy reverso com o domínio que você deseja utilizar em cada aplicação.

## Instalação

Nosso instalador foi testado em servidores com Ubuntu 20.04 e 22.04.

Acesse seu servidor via ssh e clone o repositóio.

```git clone https://github.com/igorlemoes/doguipy.git```

Entre na pasta do DoGuiPy.

```cd doguipy```

Conceda permissão de execução ao script.

```chmod +x install_server.sh```

Execute o instalador.

```./install_server.sh```

O processo de instalação vai lhe pedir algumas confirmações, para a atualização e instalação do Docker.

Por fim forneça o endereço (um domínio para o sistema e um e-mail para a geração dos certificados SSL).

Para acessar o painel do DoGuiPy abra o navegador e entre com https://seu.domínio.com:8088

## Desenvolvedor

_Me chamo Igor Lemões e este é meu primeiro projeto open source, espero ajudar a comunidade que juntamente comigo trabalha em soluções de automação e necessita de uma ferramenta como esta para facilitar o trabalho de instalação de sistemas em servidores linux através do Docker._

Para colaborar financeiramente com este projeto, faça parte da nossa comunidade e ou entre para alguma de nossas turmas de alunos.

(https://igorlemoes.com.br)

## Licença

DoGuiPy está sob os termos da [licença MIT](LICENSE).

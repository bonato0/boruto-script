<h1 align="center"> Boruto </h1>
<h1 align="center"> Bonato Optimized Root User Template Oriented </h1>

BORUTO visa facilitar a criação de ambientes do rocketchat utilizando a API da linode para criar as VMs e o Ansible para instalar, configurar e colocar no ar o site do RocketChat.

## Índice 
* [Pré-Requisitos](#pré-requisitos)
* [Variáveis](#variáveis)
* [Utilizando o Script](#utilizando)
* [Atualizando](#atualizando)
* [Finalizando](#finalizando)



## Pré-Requisitos
Para o correto funcionamento é necessário um sistema operacionais Linux. Caso utilize outro SO será necessária criar uma VM com linux.
Para utilizar é necessário clonar o repositório no diretório /usr/local/, as configurações do ansible foram setadas para este diretório.
Para instalar os pré-requisitos, utilize o seguinte comando:
```sh
./install.sh
```

## Variáveis
Para definir as variáveis da instalação o script utiliza de argumentos em linha de comando:
* --name ou -n: Define o nome da máquina virtual na linode (Sempre utilizar o padrão rocketChat-nomedavm)
* --dns: Define o site que será utilizado para criar o certificado https e por onde irão acessar o site (Necessário criar pelo site registro.br)
* --version ou -v: Define qual versão do RocketChat será utilizada (Sempre utilizar RocketChat acima da versão 5.0.0, as versões disponíveis est https://hub.docker.com/_/rocket-chat
* --vm: Cria a máquina virtual na linode e retorna o IP para ser utilizado na criação do DNS
* --install: Faz a instalação dos pré-requisitos necessários e prepara a máquina para o RocketChat (Para uma instalação completa, utilizar em conjunto com * --update ou utilize somente --all)
* --update: Atualiza o RocketChat para a versão definida caso o mesmo já tenha sido instalada
* --all: Faz a instalação completa (Conjunto das opções --install e --update)

## Utilizando

O Script é dividido em duas partes, sendo a primeira a criação da VM onde o RocketChat será instalado e a segunda parte a instalação e inicialização do RocketChat.

* Primeira Parte - Criando a VM
  Para criar a VM para o RocketChat é necessário utilizar o comando dentro do diretório /usr/local/boruto
```sh
python3 boruto.py --name rocketchat-nomedavm --vm
```
  Esse comando irá criar a VM utilizando o nome definido e retornar o IP da vm criada. Com o IP da Vm é necessário ir no site registro.br para criar o DNS.

* Segunda Parte - Configurando e Instalando o RocketChat
  Para configurar e instalar o RocketChat é necessário utilizar o comando dentro do diretório /usr/local/boruto
```sh
python3 boruto.py --dns {dns} --version versão_RC --name rocketchat-nomedavm --all
```
  Esse comando irá configurar as variáveis de instalação, sendo elas:
  * DNS: link que será utilizado para acesso e para criar o certificado HTTPS
  * Version: Versão do RocketChat que será utilizada
  * Name: Nome da VM, será utilizado para buscar o IP no arquivo de IPs
  * All: Realiza a instalação completa do RocketChat e deixa ele pronto para uso

## Atualizando
Para realizar a atualização do RocketChat você precisará ter criado a VM ou acrescentar, manualmente, o nome e ip no arquivo de IPs .ip.txt
A atualização é realizada utilizando o seguinte comando:
```sh
python3 boruto.py --version versão_RC --name rocketchat-nomedavm --update
```

## Finalizando
Após o processo de instalação e/ou atualização do RocketChat o site irá apresentar o erro 502 enquanto é iniciado, esse processo leva em média 3 minutos e após o termino dele já será possível acessar o site e configurar/usar o RocketChat

import argparse
import os
import linode_api4

# Cria os argumentos utilizado na linha de comando para definir as variáveis
parser = argparse.ArgumentParser()
parser.add_argument("--name", "-n", action='store', dest='var_name', help="Nome da VM")
parser.add_argument("--dns", action='store', dest='var_dns', help="DNS utilizado no rocketchat")
parser.add_argument("--version", "-v", action='store', dest='var_version', help="Versão do RocketChat")
parser.add_argument('--vm', nargs='?',dest='vm', const='True', type=str, default='False', help='Cria VM para instalação do RocketChat')
parser.add_argument('--install', nargs='?',dest='install', const='True', type=str, default='False', help='Instala RocketChat')
parser.add_argument('--update', nargs='?', dest='update', const='True', type=str, default='False', help='Atualiza RocketChat')
parser.add_argument("--all", action='store_true', dest='all', help="Instala e atualiza o RocketChat")
args = parser.parse_args()

# Caso o argumento --all for utilizado, habilita update e o install
if args.all:
    args.install = 'True'
    args.update = 'True'

vm_name = args.var_name
vm_dns = args.var_dns
vm_version = args.var_version

# Se o argumento --vm foi utilizado, irá ser criado uma instância pela API da Linode
if args.vm == 'True':
    client = linode_api4.LinodeClient('API_Cloud')

    # Configurações da máquina (configurações padrão para RocketChat)
    vm = client.linode.instance_create(
        image = "linode/debian11",
        label = vm_name,
        region = "us-east",
        ltype = "g6-standard-1",
        root_pass = "API_Cloud",
    )

    # Traz ip da instância criada
    ip_address = vm.ipv4[0]
    
    # Salva IP em um arquivo local para caso seja utilizado novamente
    with open('/usr/local/boruto/ip.txt', 'a') as f:
        f.write('\n'+vm_name+':'+ip_address)

    # Printa no terminal o IP da instância criada
    print('IP: ', ip_address)
    exit()

# Busca IP da VM pelo nome dela no arquivo de IPs
with open('ip.txt', 'r') as f:
    linhas = f.readlines()

    for linha in linhas:
        if vm_name in linha:
            ip_address = linha.split(':') [1]

            break

# Altera variáveis do arquivo Hosts do Ansible
with open('/usr/local/boruto/templates/hosts.yml', 'r') as f:
    data = f.read()

new_data = data.replace('ip_var', ip_address)

with open('/usr/local/boruto/inventory/hosts.yml', 'w') as f:
    f.write(new_data)

# Altera variáveis do arquivo de template do Ansible
with open('/usr/local/boruto/templates/rc.yml', 'r') as f:
    data = f.read()

new_data = data.replace('ip_var', ip_address).replace('dns_var', vm_dns).replace('version_var', vm_version).replace('install_var', args.install).replace('update_var', args.update)

with open('/usr/local/boruto/inventory/host_vars/rc.yml', 'w') as f:
    f.write(new_data)

# Inicia o Ansible para a configuração da máquina
os.system("ansible-playbook -i /usr/local/boruto/inventory/hosts.yml /usr/local/boruto/playbook.yml")

# mata58-cluster-beowulf

## Instalação
Tendo python 3.7 instalado, execute o seguinte comando para instalar as dependências:
```
python -m pip install -r requirements.txt
```

## Configuração das Máquinas
Para configurar as máquinas, é necessário acessar o arquivo config.json e determinar todas as máquinas que serão utilizadas no cluster. O arquivo config.json deve seguir o seguinte formato:
```json
{
  "nodes": [
    {
      "username": "so",
      "password": "01",
        "ip": "192.168.0.47",
        "name": "node1"
    },
    {
      "username": "so",
      "password": "01",
      "ip": "192.168.0.48",
      "name": "node2"
    }
  ]
}
```

Determine o nome de usuário e senha que será utilizado para acessar as máquinas. O campo "ip" deve ser o endereço ip da máquina. O campo "name" deve ser o hostname da máquina. O nome da máquina deve ser único para cada máquina.

Cada máquina deve ter acesso ssh habilitado. Para habilitar o acesso ssh, execute o seguinte comando:
```
sudo apt-get install openssh-server
```

Após isso, deve-se determinar uma relação entre as máquinas. Para isso, deve-se criar um arquivo chamado "hosts" na pasta /etc/ e determinar o hostname de cada máquina. O arquivo deve seguir o seguinte formato:
```
127.0.0.1 localhost
127.0.1.1 node1.ufba hostname1
192.168.0.48 node2.ufba hostname2

# The following lines are desirable for IPv6 capable hosts
::1 ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
```

Em que cada hostname deve ser único, e deve ser o mesmo nome determinado no arquivo config.json.

## Execução
Para executar o programa, execute o seguinte comando:
```
python main.py comando
```

Onde comando é o comando que será executado em todas as máquinas. Por exemplo, para executar o comando "ls", execute o seguinte comando:
```
python main.py ls
```

Para mais informações, execute o seguinte comando:
```
python main.py --help
```

Para informação sobre o comando, execute o seguinte comando:
```
python main.py comando --help
```
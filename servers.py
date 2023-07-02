from dataclasses import dataclass

import paramiko
import json


@dataclass
class Node:
    username: str
    ip: str
    password: str
    hostname: str
    __ssh: paramiko.SSHClient = None

    @property
    def ssh(self):
        if self.__ssh is None:
            self.__ssh = paramiko.SSHClient()
            self.__ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.__ssh.connect(self.ip, username=self.username, password=self.password)
        return self.__ssh


class Nodes:
    def __init__(self):
        self.nodes = get_nodes()

    def get_node(self, name):
        for node in self.nodes:
            if node.hostname == name:
                return node
        return None


def get_nodes():
    nodes = []
    with open('config.json', 'r') as file:
        config = json.load(file)
        for node in config['nodes']:
            nodes.append(
                Node(username=node['username'], password=node['password'], ip=node['ip'], hostname=node['name'])
            )
    return nodes

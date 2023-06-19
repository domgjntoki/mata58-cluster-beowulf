from dataclasses import dataclass

import paramiko


@dataclass
class Node:
    username: str
    ip: str
    password: str
    name: str


NODES = [
    Node(username='so', password='01', ip='192.168.0.47', name='node1'),
    Node(username='so', password='01', ip='192.168.0.48', name='node2'),
]


def get_nodes_ssh():
    nodes_ssh = []
    for node in NODES:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(node.ip, username=node.username, password=node.password)
        nodes_ssh.append(ssh)
    return nodes_ssh

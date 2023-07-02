# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from typing import Optional, Annotated
import re
import typer

from servers import Nodes

nodes = Nodes()
app = typer.Typer()


def print_message(stdout, stderr):
    stdout, stderr = stdout.read().decode('utf-8'), stderr.read().decode('utf-8')
    if stdout:
        print(stdout)
    elif stderr:
        print(stderr)


@app.command(help='Lista todos os arquivos de um diretório')
def ls(path: Annotated[Optional[str], typer.Argument(help='caminho/pro/diretório')] = None):
    if path is None:
        print('\n'.join([node.hostname for node in nodes.nodes]))
        return

    split_path = re.split(r'/|\\', path)
    node_name = split_path[0]
    path_rest = '/'.join(split_path[1:])

    for node in nodes.nodes:
        if node.hostname == node_name:
            stdin, stdout, stderr = node.ssh.exec_command('ls ' + path_rest)
            print_message(stdout, stderr)
            return

    print('ls: não foi possível acessar \'{}\': Arquivo ou diretório inexistente'.format(path))


@app.command(help='Copia um arquivo')
def cp(source: Annotated[str, typer.Argument(help='caminho/pro/arquivo')],
       dest: Annotated[str, typer.Argument(help='outro/caminho/pro/arquivo')]):
    split_path1, split_path2 = re.split(r'/|\\', source), re.split(r'/|\\', dest)
    node_name1, node_name2 = split_path1[0], split_path2[0]
    path_rest1, path_rest2 = '/'.join(split_path1[1:]), '/'.join(split_path2[1:])

    node1, node2 = nodes.get_node(node_name1), nodes.get_node(node_name2)

    if node1 is None or node2 is None:
        print('cp: não foi possível acessar \'{}\': Arquivo ou diretório inexistente'.format(source))
        return

    if node_name1 != node_name2:
        stdin, stdout, stderr = node1.ssh.exec_command(f'scp {path_rest1} {node2.hostname}:{path_rest2}')
    else:
        stdin, stdout, stderr = node1.ssh.exec_command(f'cp {path_rest1} {path_rest2}')
    print_message(stdout, stderr)


@app.command(help='Move um arquivo para outro lugar')
def mv(source: Annotated[str, typer.Argument(help='caminho/pro/arquivo')],
       dest: Annotated[str, typer.Argument(help='outro/caminho/pro/arquivo')]):
    split_path1, split_path2 = re.split(r'/|\\', source), re.split(r'/|\\', dest)
    node_name1, node_name2 = split_path1[0], split_path2[0]
    path_rest1, path_rest2 = '/'.join(split_path1[1:]), '/'.join(split_path2[1:])

    node1, node2 = nodes.get_node(node_name1), nodes.get_node(node_name2)

    if node1 is None or node2 is None:
        print('cp: não foi possível acessar \'{}\': Arquivo ou diretório inexistente'.format(source))
        return

    if node_name1 != node_name2:
        stdin, stdout, stderr = node1.ssh.exec_command(f'scp {path_rest1} {node2.hostname}:{path_rest2}')
        print_message(stdout, stderr)
        stdin, stdout, stderr = node1.ssh.exec_command(f'rm {path_rest1}')
    else:
        stdin, stdout, stderr = node1.ssh.exec_command(f'mv {path_rest1} {path_rest2}')
    print_message(stdout, stderr)


@app.command(help='Deleta um arquivo/diretório')
def rm(path: str):
    split_path = re.split(r'/|\\', path)
    node_name = split_path[0]
    path_rest = '/'.join(split_path[1:])
    node = nodes.get_node(node_name)
    print('node_name: ', node_name, ', path_rest: ', path_rest)

    if node_name == '' or node is None:
        print('rm: não foi possível remover \'{}\': Arquivo ou diretório inexistente'.format(path))
        return

    if path_rest == '':
        print('rm: não foi possível remover \'{}\': Diretório protegido'.format(path))
        return

    stdin, stdout, stderr = node.ssh.exec_command('rm -r ' + path_rest)
    print_message(stdout, stderr)


@app.command(help='Cria um diretório')
def mkdir(path: str):
    split_path = re.split(r'/|\\', path)
    node_name = split_path[0]
    path_rest = '/'.join(split_path[1:])
    node = nodes.get_node(node_name)
    if node is None:
        print('mkdir: não foi possível criar o diretório \'{}\': Arquivo ou diretório inexistente'.format(path))
        return

    stdin, stdout, stderr = node.ssh.exec_command('mkdir ' + path_rest)
    print_message(stdout, stderr)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

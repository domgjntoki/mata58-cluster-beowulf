# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from typing import Optional
import re
import typer

from servers import get_nodes_ssh

nodes = get_nodes_ssh()
app = typer.Typer()


@app.command(help='Lista todos os arquivos de um diretório',
             options_metavar='[caminho/pro/diretório]',

             )
def ls(path: Optional[str] = typer.Argument(None)):
    if path is None:
        print("node1\nnode2")
        return

    split_path = re.split(r'/|\\', path)
    node = split_path[0]
    path_rest = '/'.join(split_path[1:])
    if path.split('/')[0] == 'node1':
        stdin, stdout, stderr = nodes[0].exec_command('ls ' + path_rest)
        print(stderr.read().decode('utf-8'))
        return
    elif path.split('/')[0] == 'node2':
        stdin, stdout, stderr = nodes[1].exec_command('ls ' + path_rest)
        print(stdout.read().decode('utf-8'))
        return

    print('ls: não foi possível acessar \'{}\': Arquivo ou diretório inexistente'.format(path))


@app.command(help='Copia um arquivo para um diretório')
def cp(source: str, dest: str):
    print(f"Copying {source} to {dest}")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

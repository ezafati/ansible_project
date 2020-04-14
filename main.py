from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from utils import ResultCallback
from ansible import context

INVENTORY_PATH = ''


def get_host(fqdn, inventorie_path):
    """get the ansible hostname giving the fqdn (hostname)"""
    loader = DataLoader()
    inventory = InventoryManager(loader=loader, sources=inventorie_path)
    hosts_list = inventory._inventory.hosts
    for host in hosts_list:
        if hosts_list[host].vars['ansible_ssh_host'] == fqdn:
            return host


def launch_play(user, play_src, inventory_path):
    """launch the task giving in play source in the
    remote host indicated in the inventory"""
    context.CLIARGS = ImmutableDict(connection='ssh', remote_user=user, forks=10, become=True,
                                    become_method='sudo', become_user='root', check=False, diff=False)
    loader = DataLoader()
    inventory = InventoryManager(loader=loader, sources=inventory_path)
    variable_manager = VariableManager(loader=loader, inventory=inventory)
    play = Play().load(play_src, variable_manager=variable_manager, loader=loader)
    results_callback = ResultCallback()
    tqm = TaskQueueManager(
        inventory=inventory,
        variable_manager=variable_manager,
        loader=loader,
        passwords=dict(),
        stdout_callback=results_callback,
    )
    tqm.run(play)


if __name__ == '__main__':
    hostname = ''
    args1 = ''
    host = get_host(fqdn=hostname, inventorie_path=INVENTORY_PATH)
    play_source = dict(
        name="Ansible Play",
        hosts=host,
        gather_facts='yes',
        tasks=[
            dict(action=dict(module='script', args='example.py --args1 {0}'.format(args1)),
                 args=dict(excutable='python'),register='python_out'),
            dict(action=dict(module='debug', args=dict(msg='{{python_out.stdout}}')))
        ]
    )

    launch_play(user='myuser', play_src=play_source, inventory_path=INVENTORY_PATH) # execute the python script at the
    # remote host

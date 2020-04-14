from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from utils import ResultCallback

from ansible import context


def get_host(hostname, inventorie_path):
    loader = DataLoader()
    inventory = InventoryManager(loader=loader, sources=inventorie_path)
    hosts_list = inventory._inventory.hosts
    for host in hosts_list:
        if hosts_list[host].vars['ansible_ssh_host'] == hostname:
            return host


def launch_play(user, play_src, inventory_path):
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


play_source = dict(
    name="Ansible Play",
    hosts='localhost',
    gather_facts='no',
    tasks=[
        dict(action=dict(module='shell', args='ls'), register='shell_out'),
        dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}')))
    ]
)

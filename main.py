from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from utils import ResultCallback

from ansible import context

context.CLIARGS = ImmutableDict(connection='ssh', remote_user='ezafati', forks=10,  become=True,
                                become_method='sudo', become_user='root', check=False, diff=False)

loader = DataLoader()
inventory = InventoryManager(loader=loader, sources='localhost,')
variable_manager = VariableManager(loader=loader, inventory=inventory)

play_source = dict(
    name="Ansible Play",
    hosts='localhost',
    gather_facts='no',
    tasks=[
        dict(action=dict(module='shell', args='ls'), register='shell_out'),
        dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}')))
    ]
)

play = Play().load(play_source, variable_manager=variable_manager, loader=loader)
results_callback = ResultCallback()

tqm = TaskQueueManager(
    inventory=inventory,
    variable_manager=variable_manager,
    loader=loader,
    passwords=dict(),
    stdout_callback=results_callback,
    # Use our custom callback instead of the ``default`` callback plugin, which prints to stdout
)
result = tqm.run(play)

#print(result)
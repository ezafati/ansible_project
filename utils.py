from ansible.plugins.callback import CallbackBase
import json


class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """
    def __init__(self, result=None):
        super(ResultCallback, self).__init__()
        self.result = result

    def v2_runner_on_ok(self, result, **kwargs):
        """Print a json representation of the result

        This method could store the result in an instance attribute for retrieval later
        """
        host = result._host
        print(result._result.get('stdout'))
        print(json.dumps({host.name: result._result}, indent=4))

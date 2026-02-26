from azure.cli.core.commands.parameters import resource_group_name_type

def load_arguments(self, _):
    with self.argument_context("avd-health-check") as c:
        c.argument("resource_group_name", arg_type=resource_group_name_type)
        c.argument("hostpool_name", options_list=["--hostpool-name", "-p"])

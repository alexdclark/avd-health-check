from azure.cli.core import AzCommandsLoader
import azext_avd_health_check._help  # pylint: disable=unused-import


class AVDHealthCheckCommandsLoader(AzCommandsLoader):
    def __init__(self, cli_ctx=None):
        super().__init__(cli_ctx=cli_ctx)

    def load_command_table(self, args):
        from azext_avd_health_check.commands import load_command_table
        load_command_table(self, args)
        return self.command_table

    def load_arguments(self, command):
        from azext_avd_health_check._params import load_arguments
        load_arguments(self, command)


COMMAND_LOADER_CLS = AVDHealthCheckCommandsLoader

from azure.cli.core.commands import CliCommandType


def load_command_table(self, _):
    custom = CliCommandType(operations_tmpl="azext_avd_health_check.custom#{}")
    with self.command_group("avd-health-check", custom_command_type=custom) as g:
        g.custom_command("list", "list_power_states")
        g.custom_command("hello", "greeting")
        g.custom_command("online", "list_online_hosts")
        g.custom_command("offline", "list_offline_hosts")

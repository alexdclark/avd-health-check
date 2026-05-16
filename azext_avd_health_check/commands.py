from azure.cli.core.commands import CliCommandType
from azext_avd_health_check._transformers import (
    transform_host_action_list_output,
    transform_host_list_output,
)

def load_command_table(self, _):
    custom = CliCommandType(operations_tmpl="azext_avd_health_check.custom#{}")
    #Test Command to verify extension is working - to be removed later
    # with self.command_group("avd-health-check", custom_command_type=custom) as g:
    #     g.custom_command("hello", "greeting")

    #Adding Command Subgroup for host related commands
    with self.command_group("avd-health-check host", custom_command_type=custom) as g:
        g.custom_command("list", "list_power_states", table_transformer=transform_host_list_output)
        g.custom_command("start-all", "power_on_all_hosts", table_transformer=transform_host_action_list_output)
        g.custom_command("stop-all", "power_off_all_hosts", table_transformer=transform_host_action_list_output)
    
    with self.command_group("avd-health-check host list", custom_command_type=custom) as g:
        g.custom_command("online", "list_online_hosts", table_transformer=transform_host_list_output)
        g.custom_command("offline", "list_offline_hosts", table_transformer=transform_host_list_output)

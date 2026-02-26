from azure.cli.core.commands import CliCommandType

def load_command_table(self, _):
    custom = CliCommandType(operations_tmpl="azext_avd_health_check.custom#{}")
    with self.command_group("avd-health-check", custom_command_type=custom) as g:
        g.custom_command("hello", "greeting")

    #Adding Command Subgroup for host related commands
    with self.command_group("avd-health-check host", custom_command_type=custom) as g:
        g.custom_command("list", "list_power_states")
        g.custom_command("online", "list_online_hosts")
        g.custom_command("offline", "list_offline_hosts")
    
    #Adding some Lab Commands for testing purposes - to be removed later (Testing Azure Connectivity, Permissions, etc.)
    with self.command_group("avd-health-check lab", custom_command_type=custom) as g:
        g.custom_command("whoami", "lab_whoami")
       # g.custom_command("locations", "lab_locations")
        g.custom_command("resource-groups", "lab_resource_groups")

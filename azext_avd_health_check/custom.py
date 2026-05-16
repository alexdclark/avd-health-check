import json
from azure.cli.core.commands.client_factory import get_subscription_id
from azure.cli.core.util import send_raw_request


def _get_json(cmd, url):
    resp = send_raw_request(cmd.cli_ctx, "GET", url)
    return json.loads(resp.text)

#This function get VMS Power State
def _get_vm_power_state(cmd, resource_id):
    if not resource_id:
        return None

    url = (
        f"https://management.azure.com{resource_id}"
        "/instanceView?api-version=2024-07-01"
    )
    
    #Make the call to ARM with Resource ID
    try:
        instance_view = _get_json(cmd, url)
    except Exception:  # pylint: disable=broad-except
        return None

    #Pull Power State from response
    for status in instance_view.get("statuses", []):
        code = status.get("code", "")
        if code.startswith("PowerState/"):
            return status.get("displayStatus") or code.replace("PowerState/", "")

    return None


    #This function formats the session host information into a more user-friendly structure, including the power state of the underlying VM.
def _format_session_host(cmd, host):
    properties = host.get("properties", {})
    session_host_name = host.get("name", "")
    host_name = session_host_name.split("/")[-1]
    resource_id = properties.get("resourceId")

    return {
        "name": host_name,
        "resourceId": resource_id,
        "status": properties.get("status"),
        "powerState": _get_vm_power_state(cmd, resource_id),
        "sessions": properties.get("sessions"),
        "allowNewSession": properties.get("allowNewSession"),
        "assignedUser": properties.get("assignedUser"),
    }

#This function is used by list functions to get session host info and power state for all hosts in a host pool, which is then filtered by online/offline status as needed.
def _list_hosts(cmd, resource_group_name, hostpool_name):
    sub_id = get_subscription_id(cmd.cli_ctx)
    url = (
        f"https://management.azure.com/subscriptions/{sub_id}"
        f"/resourceGroups/{resource_group_name}"
        "/providers/Microsoft.DesktopVirtualization"
        f"/hostPools/{hostpool_name}/sessionHosts?api-version=2024-04-03"
    )
    avds = _get_json(cmd, url)

    return [_format_session_host(cmd, host) for host in avds.get("value", [])]


def _clean_host_output(host):
    return {
        "name": host.get("name"),
        "status": host.get("status"),
        "powerState": host.get("powerState"),
        "sessions": host.get("sessions"),
        "allowNewSession": host.get("allowNewSession"),
        "assignedUser": host.get("assignedUser"),
    }


#List Power State for all hosts
def list_power_states(cmd, resource_group_name, hostpool_name):
    hosts = _list_hosts(cmd, resource_group_name, hostpool_name)
    return [_clean_host_output(host) for host in hosts]

#List only online hosts by filtering on status
def list_online_hosts(cmd, resource_group_name, hostpool_name):
    hosts = _list_hosts(cmd, resource_group_name, hostpool_name)
    return [
        _clean_host_output(host)
        for host in hosts
        if host.get("status") == "Available"
    ]

#List only offline hosts by filtering on status
def list_offline_hosts(cmd, resource_group_name, hostpool_name):
    hosts = _list_hosts(cmd, resource_group_name, hostpool_name)
    return [
        _clean_host_output(host)
        for host in hosts
        if host.get("status") != "Available"
    ]


def _vm_action_url(resource_id, action, api_version="2025-11-01"):
    return (
        f"https://management.azure.com{resource_id}"
        f"/{action}?api-version={api_version}"
    )


def _run_vm_action(cmd, host, action, requested_state):
    resource_id = host.get("resourceId")
    if not resource_id:
        return {
            "name": host.get("name"),
            "action": action,
            "requestedState": requested_state,
            "result": "Skipped",
            "httpStatus": None,
            "powerState": host.get("powerState"),
            "message": "No VM resource ID found for this session host.",
        }

    resp = send_raw_request(cmd.cli_ctx, "POST", _vm_action_url(resource_id, action))
    http_status = getattr(resp, "status_code", None)

    return {
        "name": host.get("name"),
        "action": action,
        "requestedState": requested_state,
        "result": "Accepted" if http_status in (200, 202) else "Submitted",
        "httpStatus": http_status,
        "powerState": host.get("powerState"),
        "message": f"VM {action} request submitted.",
    }

#TODO: Implement power on/off functions using the same pattern - call ARM for each host's VM and perform the action, then return results.
def power_on_all_hosts(cmd, resource_group_name, hostpool_name):
    avds = [
        host
        for host in _list_hosts(cmd, resource_group_name, hostpool_name)
        if host.get("powerState") != "VM running"
    ]

    return [
        _run_vm_action(cmd, off_avd, "start", "VM running")
        for off_avd in avds
    ]

#TODO: Implement power on/off functions using the same pattern - call ARM for each host's VM and perform the action, then return results.
def power_off_all_hosts(cmd, resource_group_name, hostpool_name):
    avds = [
        host
        for host in _list_hosts(cmd, resource_group_name, hostpool_name)
        if host.get("powerState") == "VM running"
    ]

    return [
        _run_vm_action(cmd, on_avd, "deallocate", "VM deallocated")
        for on_avd in avds
    ]

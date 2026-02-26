import json
from azure.cli.core.commands.client_factory import get_subscription_id
from azure.cli.core.util import send_raw_request

def list_power_states(resource_group_name, hostpool_name):
    return {
        "resourceGroup": resource_group_name,
        "hostpoolName": hostpool_name,
        "message": "Hello World :) "
    }

def greeting():
    return {
        "message": f"Hello there angel from my nightmare"
    }

def list_online_hosts(resource_group_name, hostpool_name):
    return {
        "resourceGroup": resource_group_name,
        "hostpoolName": hostpool_name,
        "message": "These are your online hosts: [host1, host2, host3]"
    }

def list_offline_hosts(resource_group_name, hostpool_name):
    return {
        "resourceGroup": resource_group_name,
        "hostpoolName": hostpool_name,
        "message": "These are your offline hosts: [host4, host5]"
    }

def lab_whoami(cmd):
    sub_id = get_subscription_id(cmd.cli_ctx)
    url = f"https://management.azure.com/subscriptions/{sub_id}?api-version=2022-12-01"
    resp = send_raw_request(cmd.cli_ctx, "GET", url)
    sub = json.loads(resp.text)
    
    return {
        "subscriptionID": sub.get("subscriptionId"),
        "displayName": sub.get("displayName"),
        "tenantId": sub.get("tenantId"),
        "state": sub.get("state"),
    }

def lab_resource_groups(cmd):
    sub_id = get_subscription_id(cmd.cli_ctx)
    url = f"https://management.azure.com/subscriptions/{sub_id}/resourcegroups?api-version=2022-09-01"
    resp = send_raw_request(cmd.cli_ctx, "GET", url)
    rgps = json.loads(resp.text)

    return {
        "resourceGroups": [rgp.get("name") for rgp in rgps.get("value", [])]
    }

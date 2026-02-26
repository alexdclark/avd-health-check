def list_power_states(resource_group, hostpool_name):
    return {
        "resourceGroup": resource_group,
        "hostpoolName": hostpool_name,
        "message": "Hello World :) "
    }

def greeting():
    return {
        "message": f"Hello there angel from my nightmare"
    }

def list_online_hosts(resource_group, hostpool_name):
    return {
        "resourceGroup": resource_group,
        "hostpoolName": hostpool_name,
        "message": "These are your online hosts: [host1, host2, host3]"
    }

def list_offline_hosts(resource_group, hostpool_name):
    return {
        "resourceGroup": resource_group,
        "hostpoolName": hostpool_name,
        "message": "These are your offline hosts: [host4, host5]"
    }
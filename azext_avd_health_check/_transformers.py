def transform_host_output(host):
    return {
        "Name": host.get("name"),
        "Status": host.get("status"),
        "PowerState": host.get("powerState"),
        "Sessions": host.get("sessions"),
        "AllowNewSession": host.get("allowNewSession"),
        "AssignedUser": host.get("assignedUser"),
    }


def transform_host_list_output(hosts):
    return [transform_host_output(host) for host in hosts]


def transform_host_action_output(action):
    return {
        "Name": action.get("name"),
        "Action": action.get("action"),
        "Result": action.get("result"),
        "HttpStatus": action.get("httpStatus"),
        "CurrentPowerState": action.get("powerState"),
        "RequestedState": action.get("requestedState"),
        "Message": action.get("message"),
    }


def transform_host_action_list_output(actions):
    return [transform_host_action_output(action) for action in actions]

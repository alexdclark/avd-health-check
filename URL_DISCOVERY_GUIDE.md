# Azure ARM URL Discovery Guide

Use this guide when building new Azure CLI extension commands and you need to figure out the correct REST URL.

## 1. Start from a built-in `az` command

If Azure CLI already has a command that does something similar, run it with debug and inspect the request URL:

```bash
az group list --debug 2>&1 | grep -i "Request URL"
```

This is often the fastest way to find a working endpoint shape.

## 2. Learn the ARM URL pattern

Most management-plane calls use this base:

```text
https://management.azure.com
```

Then add scope and resource path:

```text
/subscriptions/{subId}/resourceGroups/{rg}/providers/{namespace}/{type}/{name}?api-version=...
```

Common examples:

- Resource groups:
  - `/subscriptions/{subId}/resourcegroups?api-version=2021-04-01`
- Subscription locations:
  - `/subscriptions/{subId}/locations?api-version=2022-12-01`

## 3. Discover valid API versions for a provider

When you are unsure which `api-version` to use, query provider metadata:

```bash
az rest --method get \
  --url "https://management.azure.com/subscriptions/<subId>/providers/Microsoft.DesktopVirtualization?api-version=2021-04-01"
```

Inspect:

- `resourceTypes[].resourceType`
- `resourceTypes[].apiVersions`

Pick an API version listed for the resource type you are calling.

## 4. Validate with `az rest` before coding

Before writing Python code, test your URL directly:

```bash
az rest --method get --url "<full-url>" -o json
```

If this works, reuse the same URL logic in your extension function with `send_raw_request`.

## 5. Move it into extension code

Typical pattern inside `custom.py`:

```python
from azure.cli.core.commands.client_factory import get_subscription_id
from azure.cli.core.util import send_raw_request


def my_command(cmd):
    sub_id = get_subscription_id(cmd.cli_ctx)
    url = f"https://management.azure.com/subscriptions/{sub_id}/resourcegroups?api-version=2021-04-01"
    resp = send_raw_request(cmd.cli_ctx, "GET", url)
    return resp.json()
```

## 6. Troubleshooting checklist

- `404`: wrong path or wrong resource scope.
- `401/403`: not logged in or missing RBAC permissions.
- `NoRegisteredProviderFound`: register provider namespace first.
- `InvalidApiVersionParameter`: wrong API version for that resource type.

Useful commands:

```bash
az login
az account show -o table
az provider show --namespace Microsoft.DesktopVirtualization -o json
```

# avd-health-check

Azure CLI extension for checking AVD hostpool power-state data.

This project is set up for local extension development, so you can edit Python files, rebuild, and test with `az` quickly.

## What this extension currently does

Current command group:

- `az avd-health-check host list`
- `az avd-health-check host online`
- `az avd-health-check host offline`
- `az avd-health-check hello`

Test Functions
- az avd-health-check lab resource-groups
- az avd-health-check lab whoami

At the moment these commands return stub/demo data from `custom.py` while you build out real Azure API calls.

## Project structure

```text
.
├── azext_avd_health_check/
│   ├── __init__.py          # Extension loader (COMMAND_LOADER_CLS)
│   ├── commands.py          # Command registrations
│   ├── custom.py            # Python functions behind each command
│   ├── _help.py             # CLI help text
│   └── azext_metadata.json  # Extension metadata
├── rebuild_extension.sh     # Rebuild + reinstall helper script
├── setup.py                 # Python packaging metadata
└── dist/                    # Built wheel files
```

## Prerequisites

- Azure CLI installed (`az --version`)
- Python 3 (`python3 --version`)

## Quick start

1. Clone/open the repo.
2. Run the rebuild script:

```bash
./rebuild_extension.sh
```

3. Verify the extension:

```bash
az extension show -n avd-health-check
az avd-health-check -h
```

## Run commands

Examples:

```bash
az avd-health-check list -g MyResourceGroup -p MyHostPool
az avd-health-check online -g MyResourceGroup -p MyHostPool
az avd-health-check offline -g MyResourceGroup -p MyHostPool

az avd-health-check hello
```

## Development workflow

After any code change:

1. Edit files in `azext_avd_health_check/`
2. Rebuild and reinstall:

```bash
./rebuild_extension.sh
```

3. Test commands with `az`.

## How commands are wired

- `commands.py` maps CLI command names to function names.
- `custom.py` contains the actual Python functions.

Example mapping pattern:

```python
g.custom_command("list", "list_power_states")
```

This means:

- CLI command: `az avd-health-check list`
- Python function called: `list_power_states(...)`

## Next steps

- Replace stub return values in `custom.py` with real AVD + VM power-state API calls.
- Add more command help entries in `_help.py` for `hello`, `online`, and `offline`.

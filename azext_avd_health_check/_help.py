from knack.help_files import helps

helps["avd-health-check"] = """
type: group
short-summary: AVD hostpool health checks.
"""

helps["avd-health-check list"] = """
type: command
short-summary: List AVD session host power state info.
examples:
  - name: Basic usage
    text: az avd-health-check list -g MyResourceGroup --hostpool-name MyHostPool
"""
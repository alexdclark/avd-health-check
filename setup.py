from setuptools import setup, find_packages

setup(
    name="avd-health-check",
    version="0.1.0",
    description="Azure CLI extension for AVD hostpool power checks",
    packages=find_packages(),
    include_package_data=True,
    package_data={"azext_avd_health_check": ["azext_metadata.json"]},
)
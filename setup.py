from setuptools import setup

setup(
    name="user_agent",
    version="0.1.11",
    packages=["user_agent", "user_agent.data"],
    install_requires=["six", "pytz"],
    entry_points={
        "console_scripts": {
            "ua=user_agent.cli:script_ua",
        }
    },
)

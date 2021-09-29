# ade-external-api-cli

## Installation

Install tool using the following command

```pip install .```

Usage requires configuring external api credentials for the tool. Configuration can be done using configuration command

```ade config add --tenant {tenant} --installation {installation} --environment {environment} --apikey-id {apikey_id} --apikey-secret {apikey_secret}```

The tool requires at least a design environment to be configured. Some commands require runtime environments to be configured as well.

## Usage

To get more information about all the commands available, use ```--help``` parameter with all commands and subcommands. It will give more information about the command and display all available parameters and subcommands.

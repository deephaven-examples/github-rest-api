# Deephaven + GitHub for user issue monitoring

This repository hosts an application that can be used to track and report issues submitted to a GitHub repository by external users. The tracking part of the app uses the GitHub REST API, while the reporting part uses Python's Slack API.

## Contents

- `README.md`: This file, which contains information needed to get started and use the application.
- `data`: A folder containing notebooks and an application mode script to install the required packages.
  - The required packages are [requests](https://pypi.org/project/requests/) and [slack_sdk](https://pypi.org/project/slack-sdk/).
- `docker-compose.yml`: The docker-compose YAML file that defines the Docker container setup. It is very similar to Deephaven's [base Python file](https://github.com/deephaven/deephaven-core/blob/main/containers/python/base/docker-compose.yml), with the addition of an application mode specification, and file to set the necessary environment variables for the scripts to run.
- `env-vars.env`: A file containing three lines. Each line pulls an environment variable from the host to be used in the application. More information on these is given below.

## Prerequisites

### Deephaven

Deephaven has prerequisites of its own. This application is built and deployed via Docker, so see our guide [Quick start for Docker](https://deephaven.io/core/docs/tutorials/quickstart/) for how to quickly get Deephaven up and running via Docker.

### GitHub

This application pulls information from the [GitHub REST API](https://docs.github.com/en/rest?apiVersion=2022-11-28). The API is free to use, and does not explicitly require a GitHub account with a personal access token to use. However, it is highly recommended to have those set up, as you can make up to 5,000 requests/hour to the API with them.

For more information on creating a personal access token to use for this project, see [Creating a personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token). For scopes, this application only requires the `repo` and `read:org` scopes.

### Slack

This application also contains a script to write data obtained from the GitHub API to [Slack](https://slack.com/). In order to write data to a Slack workspace, there are a few requirements.

- Have a Slack account that is a member of at least one workspace.
- [Create a Slack app](https://api.slack.com/apps/) connected to a workspace.
  - This Slack app will need the `Bots` and `Permissions` features enabled.
    - In the `Permissions` page, add a `Bot User OAuth Token` and give the app the `channels:read` and `chat:write` scopes.

The final step to set up the Slack bot is to add the bot to a channel of your choosing. In order to add the bot, type `/invite <BOT_NAME>` in the channel you wish to add it to.

### Environment variables

There are *three* environment variables that must be set properly in order for this app to work:

- `GH_PAT`: This is your GitHub personal access token.
- `GH_NAME`: This is your GitHub username.
- `SLACK_TOKEN`: This is your Slack Bot User OAuth Token.

## Usage

To run this application, run the following commands from your terminal:

```shell
docker compose pull
docker compose up
```

Once that's done, head to `http://localhost:10000/ide` in your browser of choice to bring up the Deephaven console.

There are two scripts that come with this application; they can be found in the `File Explorer` tab in the top-right pane. They are intended to be run in the order they are given below.

1. `GH_External_Issues.py`

    Before running this script, be sure to set the `my_org` and `my_repo` variables on lines 8 and 9 to the GitHub organization and repository names you are interested in. Any organization and repository you have access to will work. That includes all public repositories and any private repositories you've been granted access to.

2. `Slack_Report.py`

    Before running this script, be sure to set the `my_channel_name` variable to the name of the channel in Slack (including the leading `#`) you previously added your bot to.

## Support

If you have any questions, comments, concerns, or issues when running this application, feel free to file a ticket in this repository, or reach out to us on [Slack](https://deephaven.io/slack).

from deephaven import numpy as dhnp
from slack_sdk import WebClient
import numpy as np
import os

### CHANGE THIS VALUE TO THE NAME OF THE SLACK CHANNEL TO WRITE TO ###
my_channel_name = "#"

def write_external_issues_to_slack(slack_token, org, repo, channel_name, issue_table):
    client = WebClient()

    slack_token = os.environ["SLACK_TOKEN"]

    first_message = f"There are {issue_table.size} issues in <https://github.com/{org}/{repo}|{org}/{repo}> submitted by external users."
    client.chat_postMessage(token=slack_token, channel=channel_name, text=first_message)

    issue_numbers = np.squeeze(dhnp.to_numpy(issue_table.select(["Number"])))
    chat_text = [""] * issue_table.size
    for issue_idx, issue_number in enumerate(issue_numbers):
        issue_url = f"https://github.com/{org}/{repo}/issues/{issue_number}"
        chat_text[issue_idx] = f"<{issue_url}|{issue_number}>"
    client.chat_postMessage(token=slack_token, channel=channel_name, text=", ".join(chat_text))

write_external_issues_to_slack(my_slack_token, my_org, my_repo, my_channel_name, repo_issues_by_nonmembers)

from deephaven import DynamicTableWriter
from deephaven import dtypes as dht
from deephaven import time as dhtu

import os, requests, threading

### CHANGE THESE VARIABLES TO WHAT YOU WANT TO PULL ###
my_org = ""
my_repo = ""

issue_col_defs = {"Filer": dht.string, "Number": dht.int32, "DateFiled": dht.DateTime, "MostRecentUpdate": dht.DateTime, "Title": dht.string, "Assignee": dht.string, "IsOpen": dht.bool_}
issue_table_writer = DynamicTableWriter(issue_col_defs)
repo_issues = issue_table_writer.table

def write_gh_issues_to_table(org, repo):
    header = (os.environ["GH_NAME"], os.environ["GH_TOKEN"])

    pagenum = 1

    while True:
        url = f"https://api.github.com/repos/{org}/{repo}/issues?state=open&page={pagenum}&per_page=100"
        issues = requests.get(url, auth=header).json()

        if not(len(issues)):
            return

        for issue in issues:
            if "pull_request" in issue.keys():
                continue
            number = int(issue["url"].split("/")[-1])
            timestamp = dhtu.to_datetime(issue["created_at"])
            update_time = dhtu.to_datetime(issue["updated_at"])
            title = issue["title"]
            filer = issue["user"]["login"]
            try:
                assignee = issue["assignee"]["login"]
            except TypeError:
                assignee = ""
            is_open = not issue["closed_at"]

            issue_table_writer.write_row(filer, number, timestamp, update_time, title, assignee, is_open)
        
        pagenum += 1

member_col_defs = {"Username": dht.string}
member_table_writer = DynamicTableWriter(member_col_defs)
org_members = member_table_writer.table

def write_gh_org_members_to_table(org):
    header = (os.environ["GH_NAME"], os.environ["GH_TOKEN"])

    url = f"https://api.github.com/orgs/{org}/members?per_page=100"
    members = requests.get(url, auth=header).json()

    for member in members:
        member_table_writer.write_row(member["login"])

def get_gh_issues(org, repo):
    thread = threading.Thread(target=write_gh_issues_to_table, args=(org, repo, ))
    thread.start()

def get_gh_org_members(org):
    thread = threading.Thread(target=write_gh_org_members_to_table, args=(org, ))
    thread.start()

get_gh_issues(my_org, my_repo)
get_gh_org_members(my_org)

repo_issues_by_nonmembers = repo_issues.natural_join(org_members, on=["Filer=Username"]).where(["isNull(Username)"]).drop_columns(["Username"]).sort_descending(["DateFiled"])
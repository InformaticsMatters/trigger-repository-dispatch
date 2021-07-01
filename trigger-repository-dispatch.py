#!/usr/bin/env python

# Trigger a new GitHub build via a repository dispatch event.
#
# Add variables using '--vars' where VARS is a comma-separated list of
# variable names and values, e.g. "A=B,C=D". The variables will be added
# to the event's client payload.
#
# Usage:
#   trigger-repository-dispatch.py
#       [--vars VARS]
#       GITHUB_EVENT
#       GITHUB_REPO
#       GITHUB_TOKEN
#
# Example:
#   trigger-repository-dispatch.py \
#       dm-api informaticsmatters/blob 000 --vars A=1,B=2

import argparse
import os
import requests

GITHUB_API_URL = 'https://api.github.com/repos/'

# Build a command-line parser
# and parse the command-line...
PARSER = argparse.ArgumentParser(description='Trigger a GitHub Respository Dispatch')
PARSER.add_argument('event', type=str)
PARSER.add_argument('repo', type=str)
PARSER.add_argument('token', type=str)
PARSER.add_argument('--vars', type=str)
ARGS = PARSER.parse_args()

# Are GitLab pipeline and tag values present?
CI_PIPELINE_ID = os.environ.get('CI_PIPELINE_ID')
CI_COMMIT_TAG = os.environ.get('CI_COMMIT_TAG')

# Any variables to process?
# True if the length of '--vars' is greater than 2
# i.e. we have "A=1". "-" is passed in by some scripts to imply none.
# If there are arguments, split the comma-separated list into a simple list
VAR_LIST = []
if ARGS.vars and len(ARGS.vars) > 2:
    VAR_LIST = ARGS.vars.split(',')
VARS = {}
for VAR in VAR_LIST:
    var = VAR.split('=')
    assert len(var) == 2
    VARS[var[0]] = var[1]

# The payload to pass to the GitLab API.
# We'll add any parameters added by the user
# and a GitLab pipeline ID and tag if found.
print(ARGS)
DATA = {'event_type': ARGS.event}
CLIENT_PAYLOAD = {}
# If present
# adds the CI_PIPELINE_ID and any CI_COMMIT_TAG to the client_payload.
if CI_PIPELINE_ID:
    CLIENT_PAYLOAD['CI_PIPELINE_ID'] = CI_PIPELINE_ID
if CI_COMMIT_TAG:
    CLIENT_PAYLOAD['CI_COMMIT_TAG'] = CI_COMMIT_TAG
# Add any variables
for VAR in VARS:
    CLIENT_PAYLOAD[VAR] = VARS[VAR]
# Any client payload?
if CLIENT_PAYLOAD:
    DATA['client_payload'] = CLIENT_PAYLOAD

HEADERS = {'Accept': 'Accept: application/vnd.github.v3+json',
           'Authorization': 'token {}'.format(ARGS.token)}
URL = 'https://api.github.com/repos/{}/dispatches'.format(ARGS.repo)

# Trigger...
print(URL)
print(DATA)
response = requests.post(URL, headers=HEADERS, json=DATA, timeout=4.0)
print(response)
print(response.text)

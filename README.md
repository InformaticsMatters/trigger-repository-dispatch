# trigger-repository-dispatch

![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/informaticsmatters/trigger-repository-dispatch)

[![CodeFactor](https://www.codefactor.io/repository/github/informaticsmatters/trigger-repository-dispatch/badge)](https://www.codefactor.io/repository/github/informaticsmatters/trigger-repository-dispatch)

A Python module to simplify creating GitHub repository dispatch events and
payloads. Used by some of our GitLab repos to trigger builds in GitHub.

To use in GitLab CI:

```yaml
variables:
  # The origin of the trigger code
  TRIGGER_ORIGIN: https://raw.githubusercontent.com/informaticsmatters/trigger-repository-dispatch/2021.1

trigger:
  stage: trigger
  image: python:3.9.5-slim
  tags:
  script:
  - apt-get -y update
  - apt-get -y install curl
  - curl --location --retry 3 ${TRIGGER_ORIGIN}/requirements.txt --output trigger-repository-dispatch-requirements.txt
  - curl --location --retry 3 ${TRIGGER_ORIGIN}/trigger-repository-dispatch.py --output trigger-repository-dispatch.py
  - pip install -r trigger-repository-dispatch-requirements.txt
  - chmod +x trigger-repository-dispatch.py
  - ./trigger-repository-dispatch.py EVENT REPO $TOKEN
```

---

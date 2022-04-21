# trigger-repository-dispatch

![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/informaticsmatters/trigger-repository-dispatch)

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

## Running the trigger locally
Although designed for us in a CI process you can use the trigger for development.
You just need to configure the environment, to simulate what you'd find in the
CI process.

First, it's Python so clone this repository, create an environment, and install
the trigger's requirements: -

    cd trigger-repository-dispatch
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

Now simulate the GitLab environment variables. You will need to define: -

- `CLIENT_REPO` (the GitHub repo you want to trigger, i.e. "informaticsmatters/repo-a")
- `CLIENT_TOKEN` (a GitHub [personal access token] with access to the "repo" being triggered)
- `CI_PIPELINE_ID` (A simulated GitLab pipeline ID, any string like "521115318")
- `CI_COMMIT_TAG` (The tag of the origin repo you want to simulate, i.e."1.0.0")

For example: -

    export CLIENT_REPO=informaticsmatters/repo-a
    export CLIENT_TOKEN=000000000
    export CI_PIPELINE_ID=521115318
    export CI_COMMIT_TAG=1.0.0

With these environment variables set you just need to run the trigger...

    ./trigger-repository-dispatch.py dm-api ${CLIENT_REPO} ${CLIENT_TOKEN}

---

[personal access token]: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token

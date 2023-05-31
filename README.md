# auto-profile
Auto update of personal website, github profile and compile latex cv

On `user-data.yml` file update the pipeline will be triggered. The pipeline will:
- Update personal github page [github.com/k4black](https://github.com/k4black)
- [TBA] Update personal website [k4black.github.io](https://k4black.github.io)
- [TBA] Compile latex cv and upload it to both website and profile


## Setup

For the github actions you need to set `PAT` (Personal Access Token) with `repo` and `user` scope in this repo secrets ([docs](https://docs.github.com/en/enterprise-server@3.4/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token))

For the local development use venv:
```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Scripts  

### Github profile 
```shell
python github-profile/generate_readme.py --data=user-data.yml --output=./build/README.md
```

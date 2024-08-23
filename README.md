# auto-profile
[![Update all profiles on push](https://github.com/k4black/auto-profile/actions/workflows/update-data.yml/badge.svg)](https://github.com/k4black/auto-profile/actions/workflows/update-data.yml)

Auto update of personal website, LinkedIn, GitHub profile and compile LaTeX CV.

---

## Motivation

When it comes to maintaining an up-to-date CV, it often requires making changes to various websites, 
profiles, PDF file and placing it accordingly. However, ensuring consistent information across all 
platforms can be a pain. The aim of this repository is to establish a single, centralized source of 
information (in a YAML file) that can be used for auto generating and filling all other platforms.


## How it works

On `user-data.yml` file update the pipeline will be triggered. The pipeline will:
- Update personal github page [github.com/k4black](https://github.com/k4black)
- [TBA] Update personal website [k4black.github.io](https://k4black.github.io)
- [TBA] Update linkedin profile
- Compile latex cv and upload it to website, profile, and LinkedIn

For generating the `md` and `tex` files the `jinja2` is used.


## Repository Setup

#### Production

For the github actions you need to set `PAT` (Personal Access Token) with `repo` and `user` scope in this repo secrets ([docs](https://docs.github.com/en/enterprise-server@3.4/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token))

#### Local development

For the local development use venv:
```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
and some `latex` should be installed, for ubuntu:
```shell
sudo apt-get install texlive-latex-base
```

The following commands can be used to generate the files locally:
* Github profile 
    ```shell
    python github-profile/generate_readme.py --data=user-data.yml --output=./build/README.md
    ```
    
* Latex CV generation - first generate the `tex` file and then compile it
    ```shell
    python latex-cv/generate_tex.py --data=user-data.yml --output=./build/latex-cv/cv.tex
    pdflatex build/latex-cv/cv.tex
    ```

from pathlib import Path

import typer as typer
import requests
import yaml
from github import Github


REPO_ROOT = Path(__file__).parent.parent


def main(
        data: Path = REPO_ROOT / 'user-data.yml',
        api_token: str = typer.Option(..., envvar='PAT'),
) -> None:
    """Update github profile bio with links and short description Github"""
    with open(data, 'r') as f:
        data = yaml.safe_load(f)

    api = Github(api_token)

    user = api.get_user()

    user.edit(
        # name=data['bio']['name'],
        bio=data['summary']['short'],
        location=data['bio']['location'],
        # email=data['bio']['email'],
        blog=data['bio']['website'],
        # company=data.get('company', ''),
        hireable=data.get('hireable', False),
    )
    # TODO: add social profiles with PyGithub when available, now requests
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
    }
    social_profiles_url = 'https://api.github.com/user/social_accounts'
    # get list of account
    response = requests.get(
        social_profiles_url,
        headers=headers,
    )
    assert response.status_code == 200,(response.status_code, response.text)
    # delete all accounts
    response = requests.delete(
        social_profiles_url,
        headers=headers,
        json={'account_urls': [i['url'] for i in response.json()]},
    )
    assert response.status_code == 204 or response.status_code == 304, (response.status_code, response.text)
    # add social accounts
    response = requests.post(
        social_profiles_url,
        headers=headers,
        json={'account_urls': [data['bio']['linkedin'], data['bio']['website']]},
    )
    assert response.status_code == 201 or response.status_code == 304, (response.status_code, response.text)


if __name__ == '__main__':
    typer.run(main)

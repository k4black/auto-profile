import urllib.parse
from pathlib import Path

import typer as typer
import yaml


REPO_ROOT = Path(__file__).parent.parent


def _preprocess_shield_name(
        name: str
) -> str:
    return urllib.parse.quote(name)


def _get_shield(
        name: str,
        logo: str = '',
        color: str = 'blue',
        logo_color: str = 'white',
        url: str = None,
) -> str:
    shield = f'![{name} badge](https://img.shields.io/static/v1?label=&message={_preprocess_shield_name(name)}&style=flat&logo={logo}&color={color}&logoColor={logo_color})'
    if url is not None:
        shield = f'[{shield}]({url})'
    return shield


def _get_skills_tagline(
        tags: list[dict[str, str | int]]
) -> str:
    # TODO: add logo support
    colors_dict = {
        0: 'ffffff',
        1: 'e6f5ff',
        2: 'b3e0ff',
        3: '80ccff',
    }
    return ' '.join(
        _get_shield(name=tag['name'], logo='', color=colors_dict[tag.get('level', 0)], logo_color='white')
        for tag in tags
    )


def get_readme(
        name: str,
        description: str,
        github_username: str,
        location: str,
        github: str,
        linkedin: str,
        website: str,
        skills: list[dict[str,list]],
        projects: list[dict[str,str]],
        *,
        include_stats: bool = True,
) -> str:
    readme = ''

    readme += f'# Hi, I\'m {name} 👋\n\n'

    # Badges and Contacts
    readme += _get_shield(name='Linkedin', logo='linkedin', color='0A66C2', logo_color='white', url=linkedin) + '\n'
    readme += _get_shield(name='Github', logo='github', color='181717', logo_color='white', url=github) + '\n'
    readme += _get_shield(name='Website', logo='googlechrome', color='FF9900', logo_color='white', url=website) + '\n'
    readme += _get_shield(name=location, logo='googlemaps', color='34A853', logo_color='white', url=None) + '\n'
    readme += '---\n\n'

    # Description
    readme += f'{description}\n'
    readme += '---\n\n'

    # Languages and Tools
    readme += '### 🛠️ Tools and Languages\n'
    readme += '|  | Skills |\n'
    readme += '| --- | --- |\n'
    for group in skills:
        readme += f'| {group["group"]} | {_get_skills_tagline(group["tags"])} |\n'
    readme += '\n'
    readme += '---\n\n'

    # Projects
    readme += '### 📦 Projects\n'
    readme += '#### Personal\n'
    readme += '| Project | Description | Stack |\n'
    readme += '| --- | --- | --- |\n'
    for project in filter(lambda p: p['type'] == 'personal', projects):
        readme += f'| [{project["title"]}]({project["url"]}) | {project["description"]} | {" ".join(_get_shield(tag, color="b3e0ff") for tag in project["tags"])} |\n'
    readme += '#### Educational\n'
    readme += '| Project | Description | Stack |\n'
    readme += '| --- | --- | --- |\n'
    for project in filter(lambda p: p['type'] == 'edu', projects):
        readme += f'| [{project["title"]}]({project["url"]}) | {project["description"]} | {" ".join(_get_shield(tag, color="b3e0ff") for tag in project["tags"])} |\n'
    readme += '\n'
    readme += '---\n\n'


    # Stats
    if include_stats:
        # TODO: Update stats theme to adaptive, see https://github.com/anuraghazra/github-readme-stats#themes
        readme += '### ⚡ Github Stats\n\n'
        readme += f'![Github stats](https://github-readme-stats.vercel.app/api?username={github_username}&show_icons=true&count_private=true&hide_rank=true&line_height=24&hide=issues&custom_title=GitHub%20Stats)\n'
        readme += f'![Top Lang](https://github-readme-stats.vercel.app/api/top-langs/?username={github_username}&layout=compact&count_private=true&hide=Jupyter%20Notebook)\n'

    return readme


def main(
        data: Path = REPO_ROOT / 'user-data.yml',
        output: Path = REPO_ROOT / 'build' / 'GITHUB_PROFILE_README.md',
) -> None:
    """Generate Github Profile README from user data YAML file"""
    with open(data, 'r') as f:
        data = yaml.safe_load(f)

    readme = get_readme(
        name=data['bio']['informal'],
        description=data['summary']['github_profile'],
        github_username=data['bio']['github'].split('/')[-1],
        location=data['bio']['location'],
        github=data['bio']['github'],
        linkedin=data['bio']['linkedin'],
        website=data['bio']['website'],
        skills=data['skills'],
        projects=data['projects'],
        include_stats=data['settings'].get('include_stats', True),
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, 'w') as f:
        f.write(readme)


if __name__ == '__main__':
    typer.run(main)

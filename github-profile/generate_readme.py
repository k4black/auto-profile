import urllib.parse
from pathlib import Path

from jinja2 import Template
import typer as typer
import yaml


FILE_FOLDER = Path(__file__).parent
REPO_ROOT = FILE_FOLDER.parent


def main(
        data: Path = REPO_ROOT / 'user-data.yml',
        output: Path = REPO_ROOT / 'build' / 'github-profile' / 'GITHUB_PROFILE_README.md',
        template: Path = FILE_FOLDER / 'readme_template.jinja.md',
) -> None:
    """Generate Github Profile README from user data YAML file"""
    # load yaml data
    with open(data, 'r') as f:
        data = yaml.safe_load(f)

    # load jinja2 template
    with open(template, 'r') as f:
        jinja2_template = Template(f.read())

    # load functions in template to process data
    # jinja2_template.globals.update(
    #     _get_shield=_get_shield,
    #     _get_skills_tagline=_get_skills_tagline,
    # )

    # fill template and write to output
    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, 'w') as f:
        f.write(jinja2_template.render(
            name=data['bio']['informal'],
            summary=data['summary']['github_profile'],
            skills_list=data['skills'],
            projects_list=data['projects'],
            github_username=data['bio']['github'].split('/')[-1],
            include_stats=data['settings'].get('include_stats', True),
        ))


if __name__ == '__main__':
    typer.run(main)

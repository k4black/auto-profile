import urllib.parse
from pathlib import Path

from jinja2 import Template
import typer as typer
import yaml


FILE_FOLDER = Path(__file__).parent
REPO_ROOT = FILE_FOLDER.parent


def _process_text_to_latex(text: str) -> str:
    """Process text to be used in latex"""
    symbols_to_replace = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '\n': r'\\',
    }
    text = text.strip()
    for symbol, replacement in symbols_to_replace.items():
        text = text.replace(symbol, replacement)
    return text


def main(
        data: Path = REPO_ROOT / 'user-data.yml',
        output: Path = REPO_ROOT / 'build' / 'latex-cv' / 'cv.tex',
        template: Path = FILE_FOLDER / 'cv_template.jinja.tex',
) -> None:
    """Generate CV tex file from user data YAML file"""
    # load yaml data
    with open(data, 'r') as f:
        data = yaml.safe_load(f)

    # load jinja2 template
    with open(template, 'r') as f:
        # custom delimiters to avoid conflict with latex
        jinja2_template = Template(
            f.read(),
            block_start_string='(#', block_end_string='#)',
            variable_start_string='((', variable_end_string='))',
            comment_start_string='((#', comment_end_string='#))',
        )

    # load functions in template to process data
    jinja2_template.globals.update(
        _process_text_to_latex=_process_text_to_latex,
    )

    # fill template and write to output
    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, 'w') as f:
        f.write(jinja2_template.render(
            bio=data['bio'],
            short_summary=data['summary']['short'],
            summary=data['summary']['long'],
            experience_list=data['experience'],
            education_list=data['education'],
            certificates_list=data['certificates'],
            skills_list=data['skills'],
            publication_list=data['publications'],
            projects_list=data['projects'],
            achievements_list=data['achievements'],
            personal_summary=data['personal']['summary'],
            personal_tags_list=data['personal']['tags'],
            github_username=data['bio']['github'].split('/')[-1],
            project_name=data['settings']['name'],
            project_url=data['settings']['url'],
        ))


if __name__ == '__main__':
    typer.run(main)

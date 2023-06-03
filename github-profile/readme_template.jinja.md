# Hi, I'm {{name}} 👋

{{summary}}

{%- macro render_shield(name,logo,color,logo_color,url) %}
    {%- if url -%}
[![{{name}} badge](https://img.shields.io/static/v1?label=&message={{name | replace(" ", "%20")}}&style=flat&logo={{logo}}&color={{color}}&logoColor={{logo_color}})]({{url}})
    {%- else -%}
![{{name}} badge](https://img.shields.io/static/v1?label=&message={{name| replace(" ", "%20")}}&style=flat&logo={{logo}}&color={{color}}&logoColor={{logo_color}})
    {%- endif -%}
{%- endmacro %}

{%- macro get_color_by_level(level) %}
    {%- set colors = ["ffffff", "e6f5ff", "b3e0ff", "80ccff"] %}
    {{- colors[level] }}
{%- endmacro %}

---


### 🛠️ Tools and Languages
{#TODO: add logo support#}
|  | Skills |
| --- | --- |
{%- for skill in skills_list %}
| {{ skill.group }} | {% for tag in skill.tags %} {{ render_shield(tag.name,"",get_color_by_level(tag.get("level", 0)),"") }} {% endfor %} |
{%- endfor %}

---


### 📦 Projects
{%- macro render_projects(projects,type) %}
   {%- for project in projects -%}
      {%- if project.type == type %}
| [{{ project.name }}]({{ project.url }}) {% if project.year %}*({{ project.year }})*{% endif %} | {{ project.description }} | {% for tag in project.tags %} {{ render_shield(tag,"","f3f3ff","") }} {% endfor %} |
      {%- endif %}
   {%- endfor -%}
{%- endmacro %}

| Project | Description | Stack |
| --- | --- | --- |
| **Personal:** | | |
{{- render_projects(projects_list,"personal") }}
| **Open Source:** | | |
{{- render_projects(projects_list,"open-source") }}
| **Educational:** | | |
{{- render_projects(projects_list,"educational") }}

---

{%  if include_stats %}
### ⚡ Github Stats
{# TODO: Update stats theme to adaptive, see https://github.com/anuraghazra/github-readme-stats#themes#}
![Github stats](https://github-readme-stats.vercel.app/api?username={{github_username}}&show_icons=true&count_private=true&line_height=24&hide=issues&custom_title=Contribution%20Stats)
![Top Lang](https://github-readme-stats.vercel.app/api/top-langs/?username={{github_username}}&layout=compact&count_private=true&hide=Jupyter%20Notebook)
{% endif %}

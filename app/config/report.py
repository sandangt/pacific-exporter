from pathlib import Path

from jinja2 import Environment, FileSystemLoader, Template

from app.constant import REPORT_TEMPLATE


def get_report_template() -> Template:
    template_path = Path(REPORT_TEMPLATE)
    env = Environment(loader=FileSystemLoader(Path('resources', 'templates')))
    return env.get_template(template_path.name)

from jinja2 import Environment, PackageLoader
from pathlib import Path
import re

SERVICE_NAME = 'GitHub Resume'
SERVICE_SITE = 'http://www.pabloemidio.com.br'
RPC_SERVICE_NAME = re.sub(r'\W', '', SERVICE_NAME)

_TEMPLATES_DIR = 'github_resume/templates/'
TEMPLATE_PATH = str(Path().absolute().joinpath(_TEMPLATES_DIR))

JINJA_ENV = Environment(
    loader=PackageLoader('github_resume')
)

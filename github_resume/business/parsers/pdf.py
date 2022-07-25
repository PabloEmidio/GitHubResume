import base64
from uuid import uuid4

import pdfkit

from github_resume.business.consume.response import ServiceResponse
from github_resume.business.consume import ConsumeAPI
from github_resume.business.parsers.const import OPTIONS, CSS_FILE
from github_resume.const import JINJA_ENV


class PDFParse:
    def __init__(self):
        self.filename = f'out-{uuid4()}.pdf'
        self.consume = ConsumeAPI()

    @staticmethod
    def render_template(service_response: ServiceResponse):
        template = JINJA_ENV.get_template('template.html')
        return template.render(out=service_response)

    def generate_document(self, profile_name: str) -> dict:
        service_response = self.consume.consume_api(profile_name)
        template = self.render_template(service_response)
        pdf_file: bytes = pdfkit.from_string(
            template, options=OPTIONS, css=CSS_FILE
        )
        return {'pdf': base64.b64encode(pdf_file), 'encode_type': 'b64'}

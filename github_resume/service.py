from nameko.rpc import rpc
from werkzeug.exceptions import BadRequest

from github_resume.business.parsers.pdf import PDFParse
from github_resume.const import RPC_SERVICE_NAME


class GitHubResumeProfile:
    name = RPC_SERVICE_NAME

    @rpc
    def generate_pdf(self, data: dict) -> dict:
        if 'profile_name' not in data:
            raise BadRequest('`profile_name` not found in data')
        profile_name = data['profile_name']
        return PDFParse().generate_document(profile_name)

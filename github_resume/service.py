from nameko.rpc import rpc

from github_resume.business.parsers.pdf import PDFParse
from github_resume.const import RPC_SERVICE_NAME


class GitHubResumeProfile:
    name = RPC_SERVICE_NAME

    @rpc
    def generate_pdf(self, profile_name: str) -> dict:
        return PDFParse().generate_document(profile_name)

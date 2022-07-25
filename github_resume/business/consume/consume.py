from copy import deepcopy
from json import JSONDecodeError
import requests

from werkzeug.exceptions import NotFound, BadGateway

from github_resume.business.consume.const import USER, REPOSITORIES
from github_resume.business.consume.utils import normalize_response_datetime
from github_resume.business.consume.response import ServiceResponse
from github_resume.const import SERVICE_NAME, SERVICE_SITE


class ConsumeAPI:
    def __init__(self):
        ...

    @staticmethod
    def _get_user(username):
        response = requests.request(USER.method, USER.url.format(username))

        if response.status_code == 404:
            raise NotFound(f'User "{username}" not found on GitHub API')
        elif response.status_code >= 500:
            raise BadGateway('GitHub API returned a server error.')
        elif response.status_code != 200:
            raise BadGateway(
                'A not valid response was received from GitHub API'
            )

        try:
            user_data = response.json()
        except JSONDecodeError:
            user_data = {}
        return {
            'name': user_data.get('name', ''),
            'username': user_data.get('login', ''),
            'profile_url': user_data.get('html_url', ''),
            'profile_image_url': user_data.get('avatar_url', ''),
            'bio': user_data.get('bio', ''),
            'public_repos': user_data.get('public_repos', 0),
            'followers': user_data.get('followers', 0),
            'blog': user_data.get('blog', ''),
        }

    @staticmethod
    def __select_best_repositories(repositories: list) -> list:
        owner_repositories = list(
            filter(lambda re: re['fork'] is False, repositories)
        )
        if len(owner_repositories) > 20:
            best_repositories = sorted(
                owner_repositories,
                key=lambda rep: rep['forks_count'],
                reverse=True
            )[:20]
        else:
            best_repositories = deepcopy(owner_repositories)
        return normalize_response_datetime(sorted(
            best_repositories,
            key=lambda rep: rep['stargazers_count'],
            reverse=True
        )[:5])

    def _get_repositories(self, username: str):
        response = requests.request(
            REPOSITORIES.method, REPOSITORIES.url.format(username)
        )

        if response.status_code == 404:
            raise NotFound(
                f'Repositories of "{username}" not found on GitHub API'
            )
        elif response.status_code >= 500:
            raise BadGateway('GitHub API returned a server error.')
        elif response.status_code != 200:
            raise BadGateway(
                'A not valid response was received from GitHub API'
            )

        try:
            rep_data = response.json()
        except JSONDecodeError:
            rep_data = []
        repositories = self.__select_best_repositories(rep_data)
        return [
            {
                'name': rep.get('name'),
                'repository_link': rep.get('html_url'),
                'main_language': rep.get('language'),
                'description': rep.get('description'),
                'stars': rep.get('stargazers_count'),
                'created_at': rep.get('created_at'),
                'last_push': rep.get('pushed_at')

            }
            for rep in repositories
        ]

    def consume_api(self, username: str) -> ServiceResponse:
        user_data = self._get_user(username)
        rep_data = self._get_repositories(username)

        service_response = ServiceResponse()
        service_response.set_response({
            'generator': {
                'name': SERVICE_NAME,
                'url': SERVICE_SITE,
            },
            'profile': user_data,
            'repositories': rep_data,
        })

        return service_response

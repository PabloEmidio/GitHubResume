from collections import namedtuple


UseEndpoint = namedtuple('UseEndpoint', ('url', 'method'))

_GITHUB_API_BASE_URL = 'https://api.github.com'
_GITHUB_API_USER_ENDPOINT = _GITHUB_API_BASE_URL + '/users/{}'
_GITHUB_API_USER_REPOS_ENDPOINT = _GITHUB_API_BASE_URL + '/users/{}/repos'

USER = UseEndpoint(_GITHUB_API_USER_ENDPOINT, 'GET')
REPOSITORIES = UseEndpoint(_GITHUB_API_USER_REPOS_ENDPOINT, 'GET')

DATE_FIELDS = [
    'created_at',
    'updated_at',
    'pushed_at',
]

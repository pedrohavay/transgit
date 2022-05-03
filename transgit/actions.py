import json
import requests
from colorama import Fore
from urllib.parse import urlparse
from requests.auth import HTTPBasicAuth

from transgit.exceptions import TransGitError
from transgit.utils import colored

API_URL = "https://api.github.com"
API_HEADERS = {"Accept": "application/vnd.github.v3+json"}


def prepare_url(url):
    if not url.startswith('http'):
        url = "http://" + url
    return url


def prepare_clone_url(url, token, username="oauth2"):
    url = urlparse(url)

    return f'{url.scheme}://{username}:{token}@{url.netloc}{url.path}'


def get_repos(url, token, group=None):
    url = urlparse(prepare_url(url))
    url = f'{url.scheme}://{url.netloc}'

    if group is None:
        url += "/api/v4/projects"
    else:
        url += f"/api/v4/groups/{group.lower()}/projects"

    try:
        repos = requests.get(
            url,
            params={"private_token": token, "per_page": 999},
            verify=False
        ).json()
    except:
        raise TransGitError('It was not possible to obtain the repositories.')

    print(colored(f"[i] Found {len(repos)} repositories.", Fore.GREEN))

    for repo in repos:
        yield {
            'clone_target': prepare_clone_url(repo['http_url_to_repo'], token),
            **repo
        }


def prepare_repo_github(repo, username, token, org=None):
    owner = username if org is None else org

    url = f'{API_URL}/repos/{owner.lower()}/{repo["path"].lower()}'

    res = requests.get(
        url,
        auth=HTTPBasicAuth(username, token),
        verify=False,
        headers=API_HEADERS
    )

    if res.status_code == 404:
        if org is None:
            create_url = f'{API_URL}/user/repos'
        else:
            create_url = f'{API_URL}/orgs/{org}/repos'

        try:
            cres = requests.post(
                create_url,
                data=json.dumps({
                    "name": repo['name'],
                    "description": repo['description'].strip(),
                    "private": True,
                    "visibility": "private",
                    "auto_init": False
                }),
                headers={
                    'Authorization': f'token {token}',
                    **API_HEADERS
                }
            )

            if cres.status_code == 200 or cres.status_code == 201:
                return prepare_clone_url(cres.json()['clone_url'], token)
            else:
                raise Exception(cres.text)
        except Exception as error:
            raise TransGitError(
                f"Error creating the repository in Github: {error}")
    else:
        return prepare_clone_url(res.json()['clone_url'], token)


def archive_project(project_id, url, token):
    url = urlparse(prepare_url(url))
    url = f'{url.scheme}://{url.netloc}'

    url += f'/api/v4/projects/{project_id}/archive'

    try:
        requests.post(
            url,
            params={"private_token": token},
            verify=False
        ).json()
    except:
        raise TransGitError('It was not possible to archive the repository.')

    print(colored(f"[i] Repository successfully archived.", Fore.GREEN))

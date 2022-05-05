import os
import urllib3
import subprocess
from git import Repo
import click as click
from colorama import init, Fore

from transgit.constants import LOGO
from transgit.utils import colored
from transgit.actions import get_repos, prepare_repo_github, archive_project

init(autoreset=True)
urllib3.disable_warnings()


@click.command(help="Export your Gitlab repositories to Github!")
@click.option('-u', '--url', type=str, help='GitLab URL.', required=True)
@click.option('-t', '--token', type=str, help='GitLab Token.', required=True)
@click.option('-gu', '--guser', type=str, help='Github Username.', required=True)
@click.option('-p', '--personal-token', type=str, help='GitHub Personal Token.', required=True)
@click.option('--group', type=str, help='Select a specific GitLab group.')
@click.option('--clone-folder', type=str, help='Clone folder output. Default: ./dumps')
@click.option('--org', type=str, help='Select a Github organization.')
@click.option('--archive', is_flag=True, help='Archive project after exported. Default: false')
@click.option('--filter-repo', type=str, help='Commit Callback using git-filter-repo.')
def transgit(url, token, guser, personal_token, group=None, clone_folder=None, org=None, archive=False, filter_repo=None):
    print(colored(f'[*] Getting repositories from GitLab...', Fore.BLUE))

    # Get repositories from GitLab
    repos = get_repos(url, token, group)

    # Set clone folder
    clone_folder = os.path.join(
        os.getcwd(), "dumps") if clone_folder is None else clone_folder

    if not os.path.exists(clone_folder):
        # Create clone folder
        os.mkdir(clone_folder)

    # Iterate in each repository
    for repo in repos:
        print(colored(f'\n[*] Cloning "{repo["name"]}"...', Fore.YELLOW))

        # Format repo output folder
        repo_folder = os.path.join(clone_folder, repo['path'])

        # Clone repository to clone folder
        Repo.clone_from(repo['clone_target'], repo_folder)

        print(colored(f'[*] Preparing repository on GitHub...', Fore.YELLOW))

        # Check repository in GitHub
        new_origin = prepare_repo_github(repo, guser, personal_token, org)

        # Git config file
        config_file = os.path.join(repo_folder, '.git/config')
        content_config = None

        # Get git config file content
        with open(config_file, 'r') as fd:
            content_config = fd.read()

        # Replace remote origin URL to GitHub
        content_config = content_config.replace(
            repo['clone_target'], new_origin)

        if filter_repo is not None:
            print(colored(f'[*] Filtering the repository...', Fore.YELLOW))

            subprocess.check_call(
                ['git', 'filter-repo', '--commit-callback', filter_repo], cwd=repo_folder)

        # Get git config file content
        with open(config_file, 'w+') as fd:
            fd.write(content_config)

        # Open repo with Git
        git_repo = Repo(repo_folder)

        print(colored(f'[*] Pushing to GitHub...', Fore.YELLOW))

        # Push to new origin on Github
        git_repo.remotes.origin.push(all=True)

        print(colored(f'[+] Repository successfully exported.', Fore.GREEN))

        # Check if archive project
        if archive:
            archive_project(repo['id'], url, token)


def main():
    print(colored(LOGO, Fore.RED))
    transgit()

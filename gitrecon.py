import argparse
import json
import os

import requests
from rich import print
from rich.console import Console

from modules import gitlab_recon, github_recon

console = Console()

parser = argparse.ArgumentParser()

parser.add_argument('username')
parser.add_argument('-s', dest='sites', choices=['github', 'gitlab'],
                    help="sites selection", required=True)
parser.add_argument('-a', '--avatar', dest='avatar', action='store_true',
                    help="download avatar pic")
parser.add_argument('-o', '--output', dest='output', action='store_true',
                    help="save output")
args = parser.parse_args()


def gitlab_user_recon(username):
    gitlab_user_id = gitlab_recon.obtain_user_id(username)
    gitlab_user_info = gitlab_recon.obtain_profile_info(gitlab_user_id)
    gitlab_user_status = gitlab_recon.obtain_status(gitlab_user_id)
    gitlab_user_keys = gitlab_recon.obtain_keys(gitlab_user_id)
    gitlab_user_gpg_keys = gitlab_recon.obtain_gpg_keys(gitlab_user_id)
    gitlab_recon.extract_project_leaks(gitlab_user_id)
    gitlab_recon.validate_leaked_emails(gitlab_recon.emails_list, gitlab_user_info)
    return gitlab_user_info, gitlab_user_status, gitlab_user_keys, gitlab_user_gpg_keys


def github_user_recon(username):
    github_user_info = github_recon.obtain_profile_info(username)
    github_recon.extract_orgs(username)
    github_user_keys = github_recon.obtain_keys(username)
    github_recon.extract_events_leaks(username)
    github_recon.validate_leaked_emails(github_recon.emails_list, github_user_info)
    return github_user_info, github_user_keys


def print_github_results(user_data, keys):
    print()
    console.rule('[bold blue]' + user_data['login'] + ' Github report')

    print('[bold red] [+] Username: [/bold red]' + str(user_data['login']))
    print('[bold red] [+] Name: [/bold red]' + str(user_data['name']))
    print('[bold red] [+] User id: [/bold red]' + str(user_data['id']))
    print('[bold red] [+] Avatar url: [/bold red]' + user_data['avatar_url'])
    if user_data['email']:
        print('[bold red] [+] Email: [/bold red]' + user_data['email'])
    if user_data['location']:
        print('[bold red] [+] Location: [/bold red]' + user_data['location'])
    if user_data['bio']:
        print('[bold red] [+] Bio: [/bold red]' + user_data['bio'])
    if user_data['company']:
        print('[bold red] [+] Company: [/bold red]' + user_data['company'])
    for org in github_recon.orgs_list:
        print('[bold red] [+] Org: [/bold red]' + org)
    if user_data['blog']:
        print('[bold red] [+] Blog: [/bold red]' + user_data['blog'])
    if user_data['gravatar_id']:
        print('[bold red] [+] Gravatar id: [/bold red]' + user_data['gravatar_id'])
    if user_data['twitter_username']:
        print('[bold red] [+] Twitter username: [/bold red]' + user_data['twitter_username'])
    print('[bold red] [+] Followers: [/bold red]' + str(user_data['followers']))
    print('[bold red] [+] Following: [/bold red]' + str(user_data['following']))
    print('[bold red] [+] Created at: [/bold red]' + str(user_data['created_at']))
    print('[bold red] [+] Updated at: [/bold red]' + str(user_data['updated_at']))
    for email in github_recon.valid_emails:
        print('[bold red] [+] Leaked email: [/bold red]' + email)

    if keys:
        console.rule('[bold blue]' + user_data['login'] + ' keys')
        for key in keys:
            print('[bold red] [+] Id: [/bold red]' + str(key['id']))
            print('[bold red] [+] Key: [/bold red]' + str(key['key']))

    console.rule()


def print_gitlab_results(user_data, status, keys):
    print()
    console.rule('[bold blue]' + user_data['username'] + ' Gitlab report')

    print('[bold red] [+] Username: [/bold red]' + str(user_data['username']))
    print('[bold red] [+] Name: [/bold red]' + str(user_data['name']))
    print('[bold red] [+] User id: [/bold red]' + str(user_data['id']))
    print('[bold red] [+] State: [/bold red]' + user_data['state'])
    if status['message']:
        print('[bold red] [+] Status message: [/bold red]' + status['message'])
    print('[bold red] [+] Avatar url: [/bold red]' + user_data['avatar_url'])
    if user_data['public_email']:
        print('[bold red] [+] Email: [/bold red]' + user_data['public_email'])
    if user_data['location']:
        print('[bold red] [+] Location: [/bold red]' + user_data['location'])
    if user_data['bio']:
        print('[bold red] [+] Bio: [/bold red]' + user_data['bio'])
    if user_data['organization']:
        print('[bold red] [+] Organization: [/bold red]' + user_data['organization'])
    if user_data['job_title']:
        print('[bold red] [+] Job title: [/bold red]' + user_data['job_title'])
    if user_data['work_information']:
        print('[bold red] [+] Work information: [/bold red]' + user_data['work_information'])
    if user_data['web_url']:
        print('[bold red] [+] Web: [/bold red]' + user_data['web_url'])
    if user_data['skype']:
        print('[bold red] [+] Skype: [/bold red]' + user_data['skype'])
    if user_data['linkedin']:
        print('[bold red] [+] Linkedin: [/bold red]' + user_data['linkedin'])
    if user_data['twitter']:
        print('[bold red] [+] Twitter: [/bold red]' + user_data['twitter'])
    try:
        print('[bold red] [+] Followers: [/bold red]' + str(user_data['followers']))
        print('[bold red] [+] Following: [/bold red]' + str(user_data['following']))
        print('[bold red] [+] Created at: [/bold red]' + str(user_data['created_at']))
    except:
        pass
    for email in gitlab_recon.valid_emails:
        print('[bold red] [+] Leaked email: [/bold red]' + email)

    if keys:
        console.rule('[bold blue]' + user_data['username'] + ' keys')
        for key in keys:
            print('[bold red] [+] Tittle: [/bold red]' + str(key['title']))
            print('[bold red] [+] Created at: [/bold red]' + str(key['created_at']))
            print('[bold red] [+] Expires at: [/bold red]' + str(key['expires_at']))
            print('[bold red] [+] Key: [/bold red]' + str(key['key']))
            console.print('------------------------------', justify='center')

    console.rule()


def create_github_json_output(user_data, keys):
    json_output = {}
    json_output['username'] = user_data['login']
    json_output['name'] = user_data['name']
    json_output['id'] = user_data['id']
    json_output['avatar_url'] = user_data['avatar_url']
    json_output['orgs'] = []
    if user_data['email']:
        json_output['email'] = user_data['email']
    if user_data['location']:
        json_output['location'] = user_data['location']
    if user_data['bio']:
        json_output['bio'] = user_data['bio']
    if user_data['company']:
        json_output['company'] = user_data['company']
    for org in github_recon.orgs_list:
        json_output['orgs'].append(org)
    if user_data['blog']:
        json_output['blog'] = user_data['blog']
    if user_data['gravatar_id']:
        json_output['gravatar_id'] = user_data['gravatar_id']
    if user_data['twitter_username']:
        json_output['twitter_username'] = user_data['twitter_username']
    json_output['followers'] = user_data['followers']
    json_output['following'] = user_data['following']
    json_output['created_at'] = user_data['created_at']
    json_output['updated_at'] = user_data['updated_at']
    json_output['leaked_emails'] = []
    for email in github_recon.valid_emails:
        json_output['leaked_emails'].append(email)
    json_output['keys'] = []
    if keys:
        for key in keys:
            data = {'id': str(key['id']), 'key': str(key['key'])}
            json_output['keys'].append(data)
    return json_output


def create_gitlab_json_output(user_data, status, keys):
    json_output = {}
    json_output['username'] = user_data['username']
    json_output['name'] = user_data['name']
    json_output['id'] = user_data['id']
    json_output['state'] = user_data['state']
    json_output['avatar_url'] = user_data['avatar_url']
    if status['message']:
        json_output['description'] = status['message']
    if user_data['public_email']:
        json_output['public_email'] = user_data['public_email']
    if user_data['location']:
        json_output['location'] = user_data['location']
    if user_data['bio']:
        json_output['bio'] = user_data['bio']
    if user_data['organization']:
        json_output['organization'] = user_data['organization']
    if user_data['job_title']:
        json_output['job_title'] = user_data['job_title']
    if user_data['work_information']:
        json_output['work_information'] = user_data['work_information']
    if user_data['web_url']:
        json_output['web_url'] = user_data['web_url']
    if user_data['skype']:
        json_output['skype'] = user_data['skype']
    if user_data['linkedin']:
        json_output['linkedin'] = user_data['linkedin']
    if user_data['twitter']:
        json_output['twitter'] = user_data['twitter']
    try:
        json_output['followers'] = user_data['followers']
        json_output['following'] = user_data['following']
        json_output['created_at'] = user_data['created_at']
    except:
        pass
    json_output['leaked_emails'] = []
    for email in gitlab_recon.valid_emails:
        json_output['leaked_emails'].append(email)
    json_output['keys'] = []
    if keys:
        for key in keys:
            data = {'title': str(key['title']), 'created_at': str(key['created_at']),
                    'expires_at': str(key['expires_at']), 'key': str(key['key'])}
            json_output['keys'].append(data)

    return json_output


def save_output(json_output):
    path = 'results/' + args.username
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except:
            print()
            print('[bold red] [!] Error creating output folder[/bold red]')
            print()

    if args.sites == 'github':
        with open(path + '/' + args.username + '_github.json', 'w') as f:
            json.dump(json_output, f)
            print('[bold cyan] [+] Output saved: [/bold cyan]' + path + '/' + args.username + '_github.json')

    if args.sites == 'gitlab':
        with open(path + '/' + args.username + '_gitlab.json', 'w') as f:
            json.dump(json_output, f)
            print('[bold cyan] [+] Output saved: [/bold cyan]' + path + '/' + args.username + '_gitlab.json')

    console.rule()


def download_github_avatar(url):
    path = 'results/' + args.username
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except:
            print()
            print('[bold red] [!] Error creating output folder[/bold red]')
            print()
    r = requests.get(url)
    if args.sites == 'github':
        with open(path + '/' + args.username + '_github_avatar.jpg', "wb") as f:
            f.write(r.content)
        print('[bold cyan] [+] Avatar downloaded: [/bold cyan]' + path + '/' + args.username + '_github.jpg')

    if args.sites == 'gitlab':
        with open(path + '/' + args.username + '_gitlab_avatar.jpg', "wb") as f:
            f.write(r.content)
        print('[bold cyan] [+] Avatar downloaded: [/bold cyan]' + path + '/' + args.username + '_gitlab.jpg')

    console.rule()


if args.sites == 'github':
    user_info, keys = github_user_recon(args.username)
    print_github_results(user_info, keys)
    if args.output:
        json_data = create_github_json_output(user_info, keys)
        save_output(json_data)
    if args.avatar:
        download_github_avatar(user_info['avatar_url'])

if args.sites == 'gitlab':
    user_info, user_status, user_keys, user_gpg_keys = gitlab_user_recon(args.username)
    print_gitlab_results(user_info, user_status, user_keys)
    if args.output:
        json_data = create_gitlab_json_output(user_info, user_status, user_keys)
        save_output(json_data)
    if args.avatar:
        download_github_avatar(user_info['avatar_url'])

import argparse
import json
import os

import requests
from rich import print
from rich.console import Console

parser = argparse.ArgumentParser()

parser.add_argument('username')
"""parser.add_argument('-s', dest='sites', choices=['github', 'gitlab', 'bitbucket'],
                    help="sites selection", required=True)"""
parser.add_argument('-a', '--avatar', dest='avatar', action='store_true',
                    help="download avatar pic")
parser.add_argument('-o', '--output', dest='output', action='store_true',
                    help="save output")

args = parser.parse_args()

console = Console()

token = ''
headers = {
    'Authorization': 'token ' + token
}

emails_list = {}
orgs_list = []


def check_api_status():
    if token:
        r = requests.get('https://api.github.com/rate_limit', headers=headers)
    else:
        r = requests.get('https://api.github.com/rate_limit')
    api_limit = r.json()['resources']['core']['remaining']
    return api_limit


def obtain_user_info(user):
    if token:
        response = requests.get('https://api.github.com/users/' + user, headers=headers)
    else:
        response = requests.get('https://api.github.com/users/' + user)
    return response.json()


def obtain_user_events_info(user):
    if token:
        response = requests.get('https://api.github.com/users/' + user + '/events?per_page=100', headers=headers)
    else:
        response = requests.get('https://api.github.com/users/' + user + '/events?per_page=100')
    return response.json()


def obtain_user_orgs_info(user):
    if token:
        response = requests.get('https://api.github.com/users/' + user + '/orgs', headers=headers)
    else:
        response = requests.get('https://api.github.com/users/' + user + '/orgs')
    return response.json()


def extract_user_events_info(user):
    events = obtain_user_events_info(user)
    for data in events:
        try:
            for info in data['payload']['commits']:
                info = {info['author']['email']: info['author']['name']}
                emails_list.update(info)
        except:
            pass


def extract_user_orgs_info(user):
    orgs = obtain_user_orgs_info(user)
    for org in orgs:
        orgs_list.append(org['login'])


def main(user):
    api_limit = check_api_status()

    if api_limit == 0:
        print()
        print('[bold red] [!] API rate limit exceeded[/bold red]')
        print()

    else:
        global emails_list
        global orgs_list

        output = {}

        user_info = obtain_user_info(user)
        extract_user_events_info(user)
        extract_user_orgs_info(user)

        print()
        console.rule('[bold blue]' + user_info['login'] + ' report')
        print('[bold red] [+] Username: [/bold red]' + user_info['login'])
        print('[bold red] [+] Name: [/bold red]' + user_info['name'])
        print('[bold red] [+] User id: [/bold red]' + str(user_info['id']))
        print('[bold red] [+] Avatar url: [/bold red]' + user_info['avatar_url'])
        if args.output:
            output['username'] = user_info['login']
            output['name'] = user_info['name']
            output['id'] = user_info['id']
            output['avatar_url'] = user_info['avatar_url']
        if user_info['email']:
            print('[bold red] [+] Email: [/bold red]' + user_info['email'])
            if args.output:
                output['email'] = user_info['email']
        if user_info['location']:
            print('[bold red] [+] Location: [/bold red]' + user_info['location'])
            if args.output:
                output['location'] = user_info['location']
        if user_info['bio']:
            print('[bold red] [+] Bio: [/bold red]' + user_info['bio'])
            if args.output:
                output['bio'] = user_info['bio']
        if user_info['company']:
            print('[bold red] [+] Company: [/bold red]' + user_info['company'])
            if args.output:
                output['company'] = user_info['company']
        output['orgs'] = []
        for org in orgs_list:
            print('[bold red] [+] Org: [/bold red]' + org)
            if args.output:
                output['orgs'].append(org)
        if user_info['blog']:
            print('[bold red] [+] Blog: [/bold red]' + user_info['blog'])
            if args.output:
                output['blog'] = user_info['blog']
        if user_info['gravatar_id']:
            print('[bold red] [+] Gravatar id: [/bold red]' + user_info['gravatar_id'])
            if args.output:
                output['gravatar_id'] = user_info['gravatar_id']
        if user_info['twitter_username']:
            print('[bold red] [+] Twitter username: [/bold red]' + user_info['twitter_username'])
            if args.output:
                output['twitter_username'] = user_info['twitter_username']
        print('[bold red] [+] Followers: [/bold red]' + str(user_info['followers']))
        print('[bold red] [+] Following: [/bold red]' + str(user_info['following']))
        print('[bold red] [+] Created at: [/bold red]' + str(user_info['created_at']))
        print('[bold red] [+] Updated at: [/bold red]' + str(user_info['updated_at']))
        if args.output:
            output['followers'] = user_info['followers']
            output['following'] = user_info['following']
            output['created_at'] = user_info['created_at']
            output['updated_at'] = user_info['updated_at']

        output['leaked_emails'] = []
        for email in emails_list:
            if emails_list[email] == user_info['name']:
                print('[bold red] [+] Leaked email: [/bold red]' + email)
                if args.output:
                    output['leaked_emails'].append(email)

        console.rule()

        if args.output:
            path = 'results/' + args.username
            try:
                os.mkdir(path)
            except:
                print()
                print('[bold red] [!] Error creating output folder[/bold red]')
                print()
            with open(path + '/' + args.username + '.json', 'w') as f:
                json.dump(output, f)
            print('[bold cyan] [+] Output saved: [/bold cyan]' + path + '/' + args.username + '.json')
            console.rule()
        if args.avatar:
            r = requests.get(user_info['avatar_url'])
            with open(path + '/' + args.username + '.jpg', "wb") as f:
                f.write(r.content)
            print('[bold cyan] [+] Avatar downloaded: [/bold cyan]' + path + '/' + args.username + '.jpg')
            console.rule()

        print()


if __name__ == '__main__':
    main(args.username)

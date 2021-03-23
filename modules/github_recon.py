import requests

github_token = ''
github_headers = {
    'Authorization': 'token ' + github_token
}

emails_list = {}
valid_emails = []
orgs_list = []


def obtain_profile_info(user):
    if github_token:
        response = requests.get('https://api.github.com/users/' + user, headers=github_headers)
    else:
        response = requests.get('https://api.github.com/users/' + user)
    if response.status_code == 404:
        print()
        print(' [!] Username not found')
        exit()
    return response.json()


def obtain_orgs(user):
    if github_token:
        response = requests.get('https://api.github.com/users/' + user + '/orgs', headers=github_headers)
    else:
        response = requests.get('https://api.github.com/users/' + user + '/orgs')
    return response.json()


def obtain_keys(user):
    if github_token:
        response = requests.get('https://api.github.com/users/' + user + '/keys', headers=github_headers)
    else:
        response = requests.get('https://api.github.com/users/' + user + '/keys')
    return response.json()


def extract_orgs(user):
    orgs = obtain_orgs(user)
    for org in orgs:
        orgs_list.append(org['login'])


def obtain_events(user):
    if github_token:
        response = requests.get('https://api.github.com/users/' + user + '/events?per_page=100', headers=github_headers)
    else:
        response = requests.get('https://api.github.com/users/' + user + '/events?per_page=100')
    return response.json()


def extract_events_leaks(user):
    events = obtain_events(user)
    for data in events:
        try:
            for info in data['payload']['commits']:
                info = {info['author']['email']: info['author']['name']}
                emails_list.update(info)
        except:
            pass


def validate_leaked_emails(emails, user_info):
    for email in emails_list:
        if emails[email] == user_info['name']:
            valid_emails.append(email)

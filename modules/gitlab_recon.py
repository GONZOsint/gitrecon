import requests

gitlab_token = ''
gitlab_headers = {
    'PRIVATE-TOKEN': gitlab_token
}

emails_list = {}
valid_emails = []


def obtain_user_id(user):
    try:
        response = requests.get('https://gitlab.com/api/v4/users?username=' + user)
        gitlab_user_id = response.json()[0]['id']
        return gitlab_user_id
    except:
        print()
        print(' [!] Username not found')
        exit()


def obtain_profile_info(user_id):
    response = requests.get('https://gitlab.com/api/v4/users/' + str(user_id))
    return response.json()


def obtain_status(user_id):
    response = requests.get('https://gitlab.com/api/v4/users/' + str(user_id) + '/status')
    return response.json()


def obtain_keys(user_id):
    response = requests.get('https://gitlab.com/api/v4/users/' + str(user_id) + '/keys')
    return response.json()


def obtain_gpg_keys(user_id):
    response = requests.get('https://gitlab.com/api/v4/users/' + str(user_id) + '/gpg_keys')
    return response.json()


def obtain_projects(user_id):
    response = requests.get('https://gitlab.com/api/v4/users/' + str(user_id) + '/projects')
    return response.json()


def obtain_project_info(project_id):
    response = requests.get('https://gitlab.com/api/v4/projects/' + str(project_id) + '/repository/commits/')
    return response.json()


def extract_project_leaks(user_id):
    projects = obtain_projects(user_id)
    for project in projects:
        commits = obtain_project_info(project['id'])
        for commit in commits:
            info = {commit['author_email']: commit['author_name']}
            emails_list.update(info)


def validate_leaked_emails(emails, user_info):
    for email in emails:
        if user_info['name'] in emails_list[email]:
            valid_emails.append(email)

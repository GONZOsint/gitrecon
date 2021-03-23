# gitrecon


OSINT tool to get information from a Github or Gitlab profile and find user's email addresses leaked on commits.

## 📚 How does this work?
GitHub uses the email address associated with a GitHub account to link commits and other activity to a GitHub profile. When a user makes commits to public repos their email address is usually published in the commit and becomes publicly accessible, if you know where to look.

GitHub provide some [instructions](https://help.github.com/articles/setting-your-email-in-git/) on how to prevent this from happening, but it seems that most GitHub users either don't know or don't care that their email address may be exposed.

Finding a GitHub user's email address is often as simple as looking at their [recent events](https://developer.github.com/v3/activity/events/) via the GitHub API.

> Idea and text from [Nick Drewe](https://twitter.com/nickdrewe). 

> Source: https://thedatapack.com/tools/find-github-user-email/

---

## ✔️ Prerequisites
- [Python 3](https://www.python.org/download/releases/3.0/)

---

## 🛠️ Installation
```bash
git clone https://github.com/GONZOsint/gitrecon.git
cd gitrecon/
python3 -m pip install -r requirements.txt
```
It is possible to use a [Github access token](https://github.com/settings/tokens) by editing line 3 of the modules/github_recon.py file. This will prevent a possible API ban.

It is possible to use a [Gitlab access token](https://gitlab.com/-/profile/personal_access_tokens) by editing line 3 of the modules/gitlab_recon.py file. This will prevent a possible API ban.
```
token = '<Access token here>'
```

---

## 🔎 Usage
```
usage: gitrecon.py [-h] -s {github,gitlab} [-a] [-o] username

positional arguments:
  username

optional arguments:
  -h, --help          show this help message and exit
  -s {github,gitlab}  sites selection
  -a, --avatar        download avatar pic
  -o, --output        save output
```
![image](https://imgur.com/YERiJRM.png)

---

## Features
### Github
- #### Profile info
  - Username
  - Name
  - User ID
  - Avatar url
  - Email
  - Location
  - Bio
  - Company
  - Blog
  - Gravatar ID
  - Twitter username
  - Followers
  - Following
  - Created at
  - Updated at
- #### Extract Orgs
- #### Extract SSH keys
- #### Search for leaked emails on commits
### Gitlab
- #### Profile info
  - Username
  - Name
  - User ID
  - State
  - Status
  - Avatar url
  - Email
  - Location
  - Bio
  - Organization
  - Job title
  - Work information
  - Web
  - Skype
  - Linkedin
  - Twitter
  - Followers
  - Following
  - Created at
- #### Extract SSH keys
- #### Search for leaked emails on commits

---

## 🔒 Prevention
### Configurations on Github:

Settings url: https://github.com/settings/emails

- ✔️ Keep my email addresses private

- ✔️ Block command line pushes that expose my email

### Configurations on Gitlab:

Settings url: https://gitlab.com/-/profile

- ✔️ Public email: do not show on profile

- ✔️ Commit email: use a private email

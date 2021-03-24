# gitrecon


OSINT tool to get information from a Github or Gitlab profile and find user's email addresses leaked on commits.

## 📚 How does this work?
GitHub uses the email address associated with a GitHub account to link commits and other activity to a GitHub profile. When a user makes commits to public repos their email address is usually published in the commit and becomes publicly accessible, if you know where to look.

GitHub provide some [instructions](https://help.github.com/articles/setting-your-email-in-git/) on how to prevent this from happening, but it seems that most GitHub users either don't know or don't care that their email address may be exposed.

Finding a GitHub user's email address is often as simple as looking at their [recent events](https://developer.github.com/v3/activity/events/) via the GitHub API.

> Idea and text from [Nick Drewe](https://twitter.com/nickdrewe). 

> Source: https://thedatapack.com/tools/find-github-user-email/


### ❗ Disclaimer

As [@pielco11](https://github.com/pielco11/) [warned](https://twitter.com/noneprivacy/status/1373164632756604934), emails and other data can be spoofed in commits.

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
It is possible to use a [Github access token](https://github.com/settings/tokens) by editing line 3 of the ```modules/github_recon.py``` file. This will prevent a possible API ban.

It is possible to use a [Gitlab access token](https://gitlab.com/-/profile/personal_access_tokens) by editing line 3 of the ```modules/gitlab_recon.py``` file. This will prevent a possible API ban.
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
Results are saved in ```results/<username>/``` path.


---

## ⚔️ Features
- #### Gitlab and Github leaked emails on commits
- #### Gitlab and Github SSH keys
Github SSH keys | Gitlab SSH keys
------------ | -------------
ID | ❌
❌ | Tittle
❌ | Created at
❌ | Expires at
Key | Key

- #### Gitlab and Github profile info
Github profile info | Gitlab profile info
------------ | -------------
Username | Username
Name | Name
User ID | User ID
❌ | State
❌ | Status
Avatar url | Avatar url
Email | Email
Location | Location
Bio | Bio
Company | Organization
Organizations  |  ❌
❌ | Job title
❌ | Work information
Blog | Web
Gravatar ID | ❌
Twitter | Twitter
❌ | Skype
❌ | Linkedin
Followers | Followers
Following | Following
Created at | Created at
Updated at | ❌

---

## 🔒 Prevention
### Configurations on Github:

- Settings url: https://github.com/settings/emails

  - ✔️ Keep my email addresses private

  - ✔️ Block command line pushes that expose my email

### Configurations on Gitlab:

- Settings url: https://gitlab.com/-/profile

  - ✔️ Public email: do not show on profile

  - ✔️ Commit email: use a private email

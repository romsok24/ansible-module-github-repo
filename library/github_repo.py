#!/usr/bin/python
from ansible.module_utils.basic import *
import requests

DOCUMENTATION = '''
---
module: github_repo
short_description: Manage repositories on Github
'''

EXAMPLES = '''
- name: Create a github Repo
    github_repo:
        github_access_token: "..."
        repo_name: "ansible-repo-1"
        description: "This repo was created by ansible"
        private: yes
        has_issues: no
        has_wiki: no
        has_downloads: no
    register: result
# All properties:
        "github_access_token": 
        "name": 
        "organization": 
        "description": 
        "homepage": 
        "private": 
        "has_issues": 
        "has_projects": 
        "has_wiki": 
        "has_downloads": 
        "is_template": 
        "team_id":  
        "state":  ['present', 'absent']
        "account_level": ['personal','organization']
        "auto_init": 
        "owner":  

- name: Delete that repo
    github_repo:
        github_access_token: "..."
        name: "ansible-repo-1"
        state: absent
    register: result
'''


api_url = "https://api.github.**********.com"


def github_repo_present(data):
    api_key = data['github_access_token']
    del data['state']
    del data['github_access_token']

    headers = {"Authorization": "access_token={}" . format(api_key)}
    if data['account_level'] == "organization":
        url = "{}{}{}{}{}" . format(api_url, '/orgs/', data['organization'], '/repos?access_token=', api_key)
    if data['account_level'] == "personal":
        url = "{}{}{}" . format(api_url, '/user/repos?access_token=', api_key)
    result = requests.post(url, json.dumps(data), headers=headers)
    
    if result.status_code == 201:
        if data['collaborators'] !="":
            url = "{}/repos/{}/{}/collaborators/{}?access_token={}" . format(api_url, data['organization'], data['name'],data['collaborators'], api_key)
            result_coll = requests.put(url, headers=headers)
    if data['no_pr_tomerge'] > 0:
        url = "{}/repos/{}/{}/branches/master/protection?access_token={}" . format(api_url, data['organization'], data['name'], api_key)
        body = {
                "required_status_checks": {
                    "strict": True,
                    "contexts": ['continuous-integration/travis-ci']
                },
                "enforce_admins": True,
                "required_pull_request_reviews": {
                    "dismissal_restrictions": {"users": [''],
                    "teams": ['']
                    },
                    "dismiss_stale_reviews": True,
                    "require_code_owner_reviews": True,
                    "required_approving_review_count": data['no_pr_tomerge']
                },
                "restrictions": {
                    "users": [''],
                    "teams": [''],
                    "apps": ['']
                },
                "required_linear_history": True,
                "allow_force_pushes": True,
                "allow_deletions": True
                }
        headers = {"Accept": "application/vnd.github.luke-cage-preview+json"}
        result_coll = requests.put(url, json.dumps(body), headers=headers)


    if result.status_code == 201:
        return False, True, result.json()
    if result.status_code == 422:
        return False, False, result.json()
    meta = {"status": result.status_code, "response": result.json()}
    return True, False, meta


def github_repo_absent(data=None):
    headers = {
      "Authorization": "access_token={}" . format(data['github_access_token'])}
    url = "{}/repos/{}/{}?access_token={}" . format(api_url, data['owner'], data['name'], data['github_access_token'])
    result = requests.delete(url, headers=headers)
    if result.status_code == 204:
        return False, True, {"status": "SUCCESS"}
    if result.status_code == 404:
        result = {"status": result.status_code, "data": result.json()}
        return False, False, result
    else:
        result = {"status": result.status_code, "data": result.json()}
        return True, False, result


def main():
    fields = {
        "github_access_token": {"required": True, "type": "str"},
        "name": {"required": True, "type": "str"},
        "organization": {"required": False, "type": "str"},
        "collaborators": {"required": False, "type": "str"},
        "description": {"required": False, "type": "str"},
        "homepage": {"required": False, "type": "str"},
        "private": {"default": False, "type": "bool"},
        "topics": {"required": False, "type": "list"},
        "has_issues": {"default": True, "type": "bool"},
        "has_projects": {"default": True, "type": "bool"},
        "has_wiki": {"default": True, "type": "bool"},
        "has_downloads": {"default": True, "type": "bool"},
        "is_template": {"default": False, "type": "bool"},
        "team_id": {"required": False, "type": "int"},
        "no_pr_tomerge": {"required": True, "type": "int"},
        "state": {
            "default": "present",
            "choices": ['present', 'absent'],
            "type": 'str'
        },
        "account_level": {
            "default": "organization",
            "choices": ['personal','organization'],
            "type": 'str'
        },
        "auto_init": {"default": False, "type": "bool"},
        "owner":    {"required": False, "type": "str"}
    }
    choice_map = {
        "present": github_repo_present,
        "absent": github_repo_absent
    }
    module = AnsibleModule(argument_spec=fields)
    is_error, has_changed, result = choice_map.get(
      module.params['state'])(module.params)

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Failed with this repo action", meta=result)


if __name__ == '__main__':
    main()

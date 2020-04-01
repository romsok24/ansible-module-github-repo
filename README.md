# ansible-module-github-repo (ansible module)
-------

This module is aimed to allow managing  GitHub repositories from ansible code.

Supported scope
-------
Right now the module supports only create and delete functions - both at the organization and personal level.

Please be aware of [API token access constrain](https://help.github.com/en/github/setting-up-and-managing-organizations-and-teams/about-oauth-app-access-restrictions#setting-up-oauth-app-access-restrictions). 
For that reason - you may need to update your token rights.


Usage
-------
A test playbook is included into this repo, so you can easily learn how to use this module. Additionally feel free to inspect the module help docs. Example usage:

ansible-playbook CE_createrepo_playbook.yml --tags="RepoCreate, Debug" -e repo_name="ansible-module-HCremediation-SAP" -e repo_owner="Continuous-Engineering" -e repo_descr="Your repo description goes here" -e collab_name="username of the collaborator" -e github_access_token="********************************"  --flush-cache


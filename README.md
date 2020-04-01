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

ansible-playbook CE_createrepo_playbook.yml --tags="RepoCreate, Debug" -e repo_name="ansible-module-HCremediation-SAP" -e repo_owner="Continuous-Engineering" -e repo_descr="https://github.ibm.com/Continuous-Engineering/Ansible/issues/33" -e collab_name="Raveerna-Movva" -e github_access_token="********************************"  --flush-cache

This module is aimed to be used inside the IBM so it is configured to work with IBM github API only.

License
-------

IBM Intellectual Property

Author Information
------------------


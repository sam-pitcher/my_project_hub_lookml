import looker_sdk
import urllib3
import os
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# env variables have been declared in the yaml file

project_id = 'my_project_spoke' # project name in looker
instance = 'test.looker.shredr.xyz/'  # host name e.g. 'mydomain.looker.com'
release_branch = 'uat'  # name of git branch, e.g. 'release-xyz'

sdk = looker_sdk.init40()

# change to dev mode in spoke project
body = {"workspace_id": "dev"}
sdk.update_session(body)

# update dependancies with new code in hub project
sdk.lock_all(project_id)

# validate the code in spoke didn't break
project_validation = sdk.validate_project(project_id)
print(f"Errors: {project_validation.errors}")
print(f"Models not validated: {project_validation.models_not_validated}")

# try:
#     sdk.deploy_ref_to_production(project_id=project_id, branch=release_branch)
#     print(f'Production mode for {project_id} in {instance} set to branch: {release_branch} \n')
# except:
#     print(f'Failed to Update Production mode for {project_id} in {instance} \n')
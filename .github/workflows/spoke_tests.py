import looker_sdk
import urllib3
import os
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

hub_commit_sha = os.getenv('GITHUB_COMMIT_SHA')
git_branch = os.getenv('GITHUB_BRANCH')
print(F"Current git branch: {git_branch}")


# env variables have been declared in the yaml file
instance = 'test.looker.shredr.xyz/'  # host name e.g. 'mydomain.looker.com'

sdk = looker_sdk.init40()

spoke_project_id="my_project_spoke"
hub_project_id="my_project_hub"

# briefly deploy new code to production in dev instance
sdk.deploy_ref_to_production(project_id=hub_project_id, branch=git_branch)

# change to dev mode in dev instance
body = {"workspace_id": "dev"}
sdk.update_session(body)

# update dependancies in spoke project with new deployed code from hub
sdk.lock_all(spoke_project_id)

# validate the code in spoke didn't break
project_validation = sdk.validate_project(spoke_project_id)
print(f"Errors: {project_validation.errors}")
print(f"Models not validated: {project_validation.models_not_validated}")

# revert back to master branch in hub
# sdk.deploy_ref_to_production(project_id=hub_project_id, branch='master')



# try:
#     sdk.deploy_ref_to_production(project_id=project_id, branch=release_branch)
#     print(f'Production mode for {project_id} in {instance} set to branch: {release_branch} \n')
# except:
#     print(f'Failed to Update Production mode for {project_id} in {instance} \n')
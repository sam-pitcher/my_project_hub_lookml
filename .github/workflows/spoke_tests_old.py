import looker_sdk
import urllib3
import os
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

hub_commit_sha = os.getenv('GITHUB_COMMIT_SHA')

# env variables have been declared in the yaml file
instance = 'test.looker.shredr.xyz/'  # host name e.g. 'mydomain.looker.com'

sdk = looker_sdk.init40()

# change to dev mode in spoke project
body = {"workspace_id": "dev"}
sdk.update_session(body)

project_id = 'my_project_spoke'

# create and check out new branch in spoke
branch_name = "hub_test"
try:
  response = sdk.create_git_branch(
    project_id,
    body=looker_sdk.models40.WriteGitBranch(
        name=branch_name
    ))
  print(response)
except:
  print(f"branch: {branch_name} doesn't exist")

# update manifest to include hub commit sha


# update dependancies in spoke with new code from hub
sdk.lock_all(project_id)

# validate the code in spoke didn't break
project_validation = sdk.validate_project(project_id)
print(f"Errors: {project_validation.errors}")
print(f"Models not validated: {project_validation.models_not_validated}")

# delete branch
response = sdk.delete_git_branch(
    project_id=project_id,
    branch_name="sdfsdf")

# try:
#     sdk.deploy_ref_to_production(project_id=project_id, branch=release_branch)
#     print(f'Production mode for {project_id} in {instance} set to branch: {release_branch} \n')
# except:
#     print(f'Failed to Update Production mode for {project_id} in {instance} \n')
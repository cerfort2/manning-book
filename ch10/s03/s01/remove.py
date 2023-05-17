#Retrieves the list of sundew users from iam.py in sundew_production_iam. Referencing the variable from the separated IaC allows you to run the removal automation for future refactoring efforts.
from sundew_production_iam import iam
import subprocess

#If the removal failed and did not already remove the resource, outputs the error
def check_state_remove_status(ret, err):
    return ret != 0 \
        and 'No matching objects found' not in str(err)

#Creates a method that wraps around Terraform’s state removal command. The command passes the resource type, such as service account and identifier to remove.
def state_remove(resource_type, resource_identifier):
    command = ['terraform', 'state', 'rm', '-no-color',
               f'{resource_type}.{resource_identifier}']
    return _terraform(command)

#Opens a subprocess that runs the Terraform command to remove the resource from the state
def _terraform(command):
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return process.returncode, stdout, stderr


if __name__ == "__main__":
    sundew_iam = iam.users #Retrieves the list of sundew users from iam.py in sundew_production_iam. Referencing the variable from the separated IaC allows you to run the removal automation for future refactoring efforts.
    for user in iam.users:
        #Removes the GCP service account from the monolith’s Terraform state based on its user identifier
        ret, _, err = state_remove(
            iam.TERRAFORM_GCP_SERVICE_ACCOUNT_TYPE,
            iam.get_user_id(user))
        #Checks that the subprocess’s Terraform command successfully removed the resource from the monolith’s state
        if check_state_remove_status(ret, err):
            print(f'remove service account from state failed: {err}')
        #Removes the GCP role assignment from the monolith’s Terraform state based on its user identifier
        ret, _, err = state_remove(
            iam.TERRAFORM_GCP_ROLE_ASSIGNMENT_TYPE,
            iam.get_user_id(user))
        #Checks that the subprocess’s Terraform command successfully removed the resource from the monolith’s state
        if check_state_remove_status(ret, err):
            print(f'remove role assignment from state failed: {err}')

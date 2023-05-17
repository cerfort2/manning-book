import os

TEAM = 'sundew'
#Sets the resource types that Terraform uses as constants so you can reference them later if needed
TERRAFORM_GCP_SERVICE_ACCOUNT_TYPE = 'google_service_account'
TERRAFORM_GCP_ROLE_ASSIGNMENT_TYPE = 'google_project_iam_member'

#Keeps all of the users you added to the project as part of the monolith
users = {
    'audit-team': 'roles/viewer',
    'automation-watering': 'roles/editor',
    'user-02': 'roles/owner'
}

project = os.environ['CLOUDSDK_CORE_PROJECT']


def get_user_id(user):
    return user.replace('-', '_')


def build():
    return iam()

#Uses the module to create the JSON configuration for the IAM policies outside the monolith
def iam(users=users):
    iam_members = []
    for user, role in users.items():
        user_id = get_user_id(user)
        iam_members.append({
            #Creates a GCP service account for the project for each user in the sundew production project
            TERRAFORM_GCP_SERVICE_ACCOUNT_TYPE: [{
                user_id: [{
                    'account_id': user,
                    'display_name': user
                }]
            }]
        })
        iam_members.append({
            #Assigns the specific role defined for each service account, such as viewer, editor, or owner
            TERRAFORM_GCP_ROLE_ASSIGNMENT_TYPE: [{
                user_id: [{
                    'role': role,
                    'member': 'serviceAccount:${google_service_account.'
                    + f'{user_id}' + '.email}',
                    'project': project
                }]
            }]
        })
    return iam_members

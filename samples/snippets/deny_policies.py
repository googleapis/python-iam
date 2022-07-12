# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START iam_create_deny_policy]
def create_deny_policy(project_id: str, policy_id: str) -> None:
    from google.cloud import iam_v2beta
    from google.cloud.iam_v2beta import Policy, types
    from google.type import expr_pb2

    """
      Create a deny policy.
      You can add deny policies to organizations, folders, and projects.
      Each of these resources can have up to 5 deny policies.

      Deny policies contain deny rules, which specify the following:
      1. The permissions to deny and/or exempt.
      2. The principals that are denied, or exempted from denial.
      3. An optional condition on when to enforce the deny rules.

      Params:
      project_id: ID or number of the Google Cloud project you want to use.
      policy_id: Specify the id of the Deny policy you want to create.
    """
    policies_client = iam_v2beta.PoliciesClient()

    # Each deny policy is attached to an organization, folder, or project.
    # To work with deny policies, specify the attachment point.
    #
    # Its format can be one of the following:
    # 1. cloudresourcemanager.googleapis.com/organizations/ORG_ID
    # 2. cloudresourcemanager.googleapis.com/folders/FOLDER_ID
    # 3. cloudresourcemanager.googleapis.com/projects/PROJECT_ID
    #
    # The attachment point is identified by its URL-encoded resource name. Hence, replace
    # the "/" with "%2F".
    attachment_point = f"cloudresourcemanager.googleapis.com%2Fprojects%2F{project_id}"

    deny_rule = types.DenyRule()
    # Add one or more principals who should be denied the permissions specified in this rule.
    # For more information on allowed values, see: https://cloud.google.com/iam/docs/principal-identifiers
    deny_rule.denied_principals = ["principalSet://goog/public:all"]

    # Optionally, set the principals who should be exempted from the
    # list of denied principals. For example, if you want to deny certain permissions
    # to a group but exempt a few principals, then add those here.
    # deny_rule.exception_principals = ["principalSet://goog/group/project-admins@example.com"]

    # Set the permissions to deny.
    # The permission value is of the format: service_fqdn/resource.action
    # For the list of supported permissions, see: https://cloud.google.com/iam/help/deny/supported-permissions
    deny_rule.denied_permissions = [
        "cloudresourcemanager.googleapis.com/projects.delete"
    ]

    # Optionally, add the permissions to be exempted from this rule.
    # Meaning, the deny rule will not be applicable to these permissions.
    # deny_rule.exception_permissions = ["cloudresourcemanager.googleapis.com/projects.create"]

    # Set the condition which will enforce the deny rule.
    # If this condition is true, the deny rule will be applicable. Else, the rule will not be enforced.
    # The expression uses Common Expression Language syntax (CEL).
    # Here we block access based on tags.
    #
    # A tag is a key-value pair that can be attached to an organization, folder, or project. You can use deny policies to deny permissions based on tags without adding an IAM Condition to every role grant.
    # For example, imagine that you tag all of your projects as dev, test, or prod. You want only members of project-admins@example.com to be able to perform operations on projects that are tagged prod.
    # To solve this problem, you create a deny rule that denies the cloudresourcemanager.googleapis.com/projects.delete permission to everyone except project-admins@example.com for resources that are tagged test.
    deny_rule.denial_condition = expr_pb2.Expr(
        expression="!resource.matchTag('12345678/env', 'test')"
    )

    # Add the deny rule and a description for it.
    policy_rule = types.PolicyRule()
    policy_rule.description = "block all principals from deleting projects, unless the principal is a member of project-admins@example.com and the project being deleted has a tag with the value test"
    policy_rule.deny_rule = deny_rule

    policy = types.Policy()
    policy.display_name = "Restrict project deletion access"
    policy.rules = [policy_rule]

    # Set the policy resource path, policy rules and a unique ID for the policy.
    request = types.CreatePolicyRequest()
    # Construct the full path of the policy.
    # Its format is: "policies/{attachmentPoint}/denypolicies/{policyId}"
    request.parent = f"policies/{attachment_point}/denypolicies"
    request.policy = policy
    request.policy_id = policy_id

    # Build the create policy request.
    policies_client.create_policy(request=request)
    print(f"Created the deny policy: {policy_id}")


# [END iam_create_deny_policy]


# [START iam_list_deny_policy]
def list_deny_policy(project_id: str) -> None:
    from google.cloud import iam_v2beta
    from google.cloud.iam_v2beta import types

    """
    List all the deny policies that are attached to a resource.
    A resource can have up to 5 deny policies.

    project_id: ID or number of the Google Cloud project you want to use.
    """
    policies_client = iam_v2beta.PoliciesClient()

    # Each deny policy is attached to an organization, folder, or project.
    # To work with deny policies, specify the attachment point.
    #
    # Its format can be one of the following:
    # 1. cloudresourcemanager.googleapis.com/organizations/ORG_ID
    # 2. cloudresourcemanager.googleapis.com/folders/FOLDER_ID
    # 3. cloudresourcemanager.googleapis.com/projects/PROJECT_ID
    #
    # The attachment point is identified by its URL-encoded resource name. Hence, replace
    # the "/" with "%2F".
    attachment_point = f"cloudresourcemanager.googleapis.com%2Fprojects%2F{project_id}"

    request = types.ListPoliciesRequest()
    # Construct the full path of the resource to which the policy is attached.
    # Its format is: "policies/{attachmentPoint}/denypolicies"
    request.parent = f"policies/{attachment_point}/denypolicies"

    # Create a list request and iterate over the returned policies.
    policies = policies_client.list_policies(request=request)

    for policy in policies:
        print(policy.name)
    print("Listed all deny policies")


# [END iam_list_deny_policy]


# [START iam_get_deny_policy]
def get_deny_policy(project_id: str, policy_id: str):
    from google.cloud import iam_v2beta
    from google.cloud.iam_v2beta import Policy, types

    """
    Retrieve the deny policy given the project ID and policy ID.

    project_id: ID or number of the Google Cloud project you want to use.
    policy_id: Specify the ID of the deny policy you want to retrieve.
    """
    policies_client = iam_v2beta.PoliciesClient()

    # Each deny policy is attached to an organization, folder, or project.
    # To work with deny policies, specify the attachment point.
    #
    # Its format can be one of the following:
    # 1. cloudresourcemanager.googleapis.com/organizations/ORG_ID
    # 2. cloudresourcemanager.googleapis.com/folders/FOLDER_ID
    # 3. cloudresourcemanager.googleapis.com/projects/PROJECT_ID
    #
    # The attachment point is identified by its URL-encoded resource name. Hence, replace
    # the "/" with "%2F".
    attachment_point = f"cloudresourcemanager.googleapis.com%2Fprojects%2F{project_id}"

    request = types.GetPolicyRequest()
    # Construct the full path of the policy.
    # Its format is: "policies/{attachmentPoint}/denypolicies/{policyId}"
    request.name = f"policies/{attachment_point}/denypolicies/{policy_id}"

    # Execute the GetPolicy request.
    policy = policies_client.get_policy(request=request)
    print(f"Retrieved the deny policy: {policy_id} : {policy}")
    return policy


# [END iam_get_deny_policy]


# [START iam_update_deny_policy]
def update_deny_policy(project_id: str, policy_id: str, etag: str) -> None:
    from google.cloud import iam_v2beta
    from google.cloud.iam_v2beta import types
    from google.type import expr_pb2

    """
    Update the deny rules and/ or its display name after policy creation.

    project_id: ID or number of the Google Cloud project you want to use.

    policy_id: Specify the ID of the deny policy you want to retrieve.

    etag: Etag field that identifies the policy version. The etag changes each time
    you update the policy. Get the etag of an existing policy by performing a GetPolicy request.
    """
    policies_client = iam_v2beta.PoliciesClient()

    # Each deny policy is attached to an organization, folder, or project.
    # To work with deny policies, specify the attachment point.
    #
    # Its format can be one of the following:
    # 1. cloudresourcemanager.googleapis.com/organizations/ORG_ID
    # 2. cloudresourcemanager.googleapis.com/folders/FOLDER_ID
    # 3. cloudresourcemanager.googleapis.com/projects/PROJECT_ID
    #
    # The attachment point is identified by its URL-encoded resource name. Hence, replace
    # the "/" with "%2F".
    attachment_point = f"cloudresourcemanager.googleapis.com%2Fprojects%2F{project_id}"

    deny_rule = types.DenyRule()

    # Add one or more principals who should be denied the permissions specified in this rule.
    # For more information on allowed values, see: https://cloud.google.com/iam/docs/principal-identifiers
    deny_rule.denied_principals = ["principalSet://goog/public:all"]

    # Optionally, set the principals who should be exempted from the list of principals added in "DeniedPrincipals".
    # Example, if you want to deny certain permissions to a group but exempt a few principals, then add those here.
    # deny_rule.exception_principals = ["principalSet://goog/group/project-admins@example.com"]

    # Set the permissions to deny.
    # The permission value is of the format: service_fqdn/resource.action
    # For the list of supported permissions, see: https://cloud.google.com/iam/help/deny/supported-permissions
    deny_rule.denied_permissions = [
        "cloudresourcemanager.googleapis.com/projects.delete"
    ]

    # Add the permissions to be exempted from this rule.
    # Meaning, the deny rule will not be applicable to these permissions.
    # deny_rule.exception_permissions = ["cloudresourcemanager.googleapis.com/projects.get"]

    # Set the condition which will enforce the deny rule.
    # If this condition is true, the deny rule will be applicable. Else, the rule will not be enforced.
    #
    # The expression uses Common Expression Language syntax (CEL). Here we block access based on tags.
    #
    # A tag is a key-value pair that can be attached to an organization, folder, or project. You can use deny policies to deny permissions based on tags without adding an IAM Condition to every role grant.
    # For example, imagine that you tag all of your projects as dev, test, or prod. You want only members of project-admins@example.com to be able to perform operations on projects that are tagged prod.
    # To solve this problem, you create a deny rule that denies the cloudresourcemanager.googleapis.com/projects.delete permission to everyone except project-admins@example.com for resources that are tagged prod.
    deny_rule.denial_condition = expr_pb2.Expr(
        expression="!resource.matchTag('12345678/env', 'prod')"
    )

    # Set the rule description and deny rule to update.
    policy_rule = types.PolicyRule()
    policy_rule.description = "block all principals from deleting projects, unless the principal is a member of project-admins@example.com and the project being deleted has a tag with the value prod"
    policy_rule.deny_rule = deny_rule

    # Set the policy resource path, version (etag) and the updated deny rules.
    policy = types.Policy()
    # Construct the full path of the policy.
    # Its format is: "policies/{attachmentPoint}/denypolicies/{policyId}"
    policy.name = f"policies/{attachment_point}/denypolicies/{policy_id}"
    policy.etag = etag
    policy.rules = [policy_rule]

    # Create the update policy request.
    request = types.UpdatePolicyRequest()
    request.policy = policy

    policies_client.update_policy(request=request)
    print(f"Updated the deny policy: {policy_id}")


# [END iam_update_deny_policy]


# [START iam_delete_deny_policy]
def delete_deny_policy(project_id: str, policy_id: str) -> None:
    from google.cloud import iam_v2beta
    from google.cloud.iam_v2beta import types

    """
    Delete the policy if you no longer want to enforce the rules in a deny policy.

    project_id: ID or number of the Google Cloud project you want to use.
    policy_id: Specify the ID of the deny policy you want to retrieve.
    """
    policies_client = iam_v2beta.PoliciesClient()

    # Each deny policy is attached to an organization, folder, or project.
    # To work with deny policies, specify the attachment point.
    #
    # Its format can be one of the following:
    # 1. cloudresourcemanager.googleapis.com/organizations/ORG_ID
    # 2. cloudresourcemanager.googleapis.com/folders/FOLDER_ID
    # 3. cloudresourcemanager.googleapis.com/projects/PROJECT_ID
    #
    # The attachment point is identified by its URL-encoded resource name. Hence, replace
    # the "/" with "%2F".
    attachment_point = f"cloudresourcemanager.googleapis.com%2Fprojects%2F{project_id}"

    request = types.DeletePolicyRequest()
    # Construct the full path of the policy.
    # Its format is: "policies/{attachmentPoint}/denypolicies/{policyId}"
    request.name = f"policies/{attachment_point}/denypolicies/{policy_id}"

    # Create the DeletePolicy request.
    policies_client.delete_policy(request=request)
    print(f"Deleted the deny policy: {policy_id}")


# [END iam_delete_deny_policy]


if __name__ == "__main__":
    import uuid

    # Your Google Cloud project id.
    project_id = "your-google-cloud-project-id"
    # Any unique id (0 to 63 chars) starting with a lowercase alphabet.
    policy_id = f"deny-{uuid.uuid4()}"

    # Test the policy lifecycle.
    create_deny_policy(project_id, policy_id)
    list_deny_policy(project_id)
    policy = get_deny_policy(project_id, policy_id)
    update_deny_policy(project_id, policy_id, policy.etag)
    delete_deny_policy(project_id, policy_id)

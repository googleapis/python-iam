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

import uuid

from google.type import expr_pb2

from google.cloud import iam_v2beta
from google.cloud.iam_v2beta import types, Policy


def create_deny_policy(project_id: str, policy_id: str) -> None:
    policies_client = iam_v2beta.PoliciesClient()

    expr = expr_pb2.Expr(
        expression="!resource.matchTag('12345678/env', 'test')"
    )

    deny_rule = types.DenyRule()
    deny_rule.denied_principals = ["principalSet://goog/public:all"]
    # deny_rule.exception_principals = ["principalSet://goog/group/project-admins@example.com"]
    deny_rule.denied_permissions = ["cloudresourcemanager.googleapis.com/projects.delete"]
    deny_rule.denial_condition = expr

    policy_rule = types.PolicyRule()
    policy_rule.description = "block all principals from deleting projects, unless the principal is a member of project-admins@example.com and the project being deleted has a tag with the value test"
    policy_rule.deny_rule = deny_rule

    policy = types.Policy()
    policy.name = "Restrict access to test env project deletion"
    policy.display_name = "Restrict xyz access for a member abc"
    policy.rules = [policy_rule]

    attachment_point = f"cloudresourcemanager.googleapis.com%2Fprojects%2F{project_id}"

    request = types.CreatePolicyRequest()
    request.parent = f"policies/{attachment_point}/denypolicies"
    request.policy = policy
    request.policy_id = policy_id

    policies_client.create_policy(request=request)
    print(f"Created the deny policy: {policy_id}")


def list_deny_policy(project_id: str) -> None:
    policies_client = iam_v2beta.PoliciesClient()

    request = types.ListPoliciesRequest()

    attachment_point = f"cloudresourcemanager.googleapis.com%2Fprojects%2F{project_id}"
    request.parent = f"policies/{attachment_point}/denypolicies"

    policies = policies_client.list_policies(request=request)

    for policy in policies:
        print(policy.name)
    print("Listed all deny policies")


def get_deny_policy(project_id: str, policy_id: str) -> Policy:
    policies_client = iam_v2beta.PoliciesClient()

    request = types.GetPolicyRequest()

    attachment_point = f"cloudresourcemanager.googleapis.com%2Fprojects%2F{project_id}"
    request.name = f"policies/{attachment_point}/denypolicies/{policy_id}"

    policy = policies_client.get_policy(request=request)
    print(f"Retrieved the deny policy: {policy_id} : {policy}")
    return policy


def update_deny_policy(project_id: str, policy_id: str, etag: str) -> None:
    policies_client = iam_v2beta.PoliciesClient()

    expr = expr_pb2.Expr(
        expression="!resource.matchTag('12345678/env', 'prod')"
    )

    deny_rule = types.DenyRule()
    deny_rule.denied_principals = ["principalSet://goog/public:all"]
    # deny_rule.exception_principals = ["principalSet://goog/group/project-admins@example.com"]
    deny_rule.denied_permissions = ["cloudresourcemanager.googleapis.com/projects.delete"]
    deny_rule.denial_condition = expr

    policy_rule = types.PolicyRule()
    policy_rule.description = "block all principals from deleting projects, unless the principal is a member of project-admins@example.com and the project being deleted has a tag with the value test"
    policy_rule.deny_rule = deny_rule

    attachment_point = f"cloudresourcemanager.googleapis.com%2Fprojects%2F{project_id}"

    policy = types.Policy()
    policy.name = f"policies/{attachment_point}/denypolicies/{policy_id}"
    policy.display_name = "Restrict xyz access for a member abc"
    policy.rules = [policy_rule]
    policy.etag = etag

    request = types.UpdatePolicyRequest()
    request.policy = policy

    policies_client.update_policy(request=request)
    print(f"Updated the deny policy: {policy_id}")


def delete_deny_policy(project_id: str, policy_id: str) -> None:
    policies_client = iam_v2beta.PoliciesClient()

    request = types.DeletePolicyRequest()
    attachment_point = f"cloudresourcemanager.googleapis.com%2Fprojects%2F{project_id}"
    request.name = f"policies/{attachment_point}/denypolicies/{policy_id}"

    policies_client.delete_policy(request=request)
    print(f"Deleted the deny policy: {policy_id}")


if __name__ == "__main__":
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

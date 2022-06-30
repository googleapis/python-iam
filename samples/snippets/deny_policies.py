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


def create_deny_policy(project_id: str, policy_name: str):
    policies_client = iam_v2beta.PoliciesClient()

    expr = expr_pb2.Expr(
        expression="!resource.matchTag('12345678/env', 'test')"
    )

    deny_rule = iam_v2beta.DenyRule()
    deny_rule.denied_principals = ["principalSet://goog/public:all"]
    deny_rule.exception_principals = ["principalSet://goog/group/project-admins@example.com"]
    deny_rule.denied_permissions = ["cloudresourcemanager.googleapis.com/projects.delete"]
    deny_rule.denial_condition = expr

    policy_rule = iam_v2beta.PolicyRule()
    policy_rule.description = "block all principals from deleting projects, unless the principal is a member of project-admins@example.com and the project being deleted has a tag with the value test"
    policy_rule.deny_rule = deny_rule

    policy = iam_v2beta.Policy()
    policy.name = policy_name
    policy.display_name = "Restrict xyz access for a member abc"
    policy.rules = [policy_rule]

    attachment_point = f"cloudresourcemanager.googleapis.com%2Fprojects%2F{project_id}"

    request = iam_v2beta.CreatePolicyRequest()
    request.parent = f"policies/{attachment_point}/denypolicies"
    request.policy = policy
    request.policy_id = f"deny-{uuid.uuid4()}"

    response = policies_client.create_policy(request=request)
    print(f"Created the deny policy: {response.result()}")


def list_deny_policy(project_id: str):
    policies_client = iam_v2beta.PoliciesClient()

    request = iam_v2beta.ListPoliciesRequest()

    attachment_point = f"cloudresourcemanager.googleapis.com%2Fprojects%2F{project_id}"
    request.parent = f"policies/{attachment_point}/denypolicies"

    policies = policies_client.list_policies(request=request)

    for policy in policies:
        print(policy)
    print("Listed all deny policies")


def get_deny_policy(project_id: str, policy_name: str):
    policies_client = iam_v2beta.PoliciesClient()

    request = iam_v2beta.GetPolicyRequest()

    attachment_point = f"cloudresourcemanager.googleapis.com%2Fprojects%2F{project_id}"
    request.name = f"policies/{attachment_point}/denypolicies/{policy_name}"

    policy = policies_client.get_policy(request=request)
    print(f"Retrieved the deny policy: {policy}")


def update_deny_policy(project_id: str, policy_name: str):
    policies_client = iam_v2beta.PoliciesClient()

    expr = expr_pb2.Expr(
        expression="!resource.matchTag('12345678/env', 'prod')"
    )

    deny_rule = iam_v2beta.DenyRule()
    deny_rule.denied_principals = ["principalSet://goog/public:all"]
    deny_rule.exception_principals = ["principalSet://goog/group/project-admins@example.com"]
    deny_rule.denied_permissions = ["cloudresourcemanager.googleapis.com/projects.delete"]
    deny_rule.denial_condition = expr

    policy_rule = iam_v2beta.PolicyRule()
    policy_rule.description = "block all principals from deleting projects, unless the principal is a member of project-admins@example.com and the project being deleted has a tag with the value test"
    policy_rule.deny_rule = deny_rule

    policy = iam_v2beta.Policy()
    policy.name = policy_name
    policy.display_name = "Restrict xyz access for a member abc"
    policy.rules = policy_rule

    attachment_point = f"cloudresourcemanager.googleapis.com%2Fprojects%2F{project_id}"

    request = iam_v2beta.UpdatePolicyRequest()
    request.parent = f"policies/{attachment_point}/denypolicies"
    request.policy = policy

    response = policies_client.update_policy(request=request)
    print(f"Updated the deny policy : {response}")


def delete_deny_policy(project_id: str, policy_name: str):
    policies_client = iam_v2beta.PoliciesClient()

    request = iam_v2beta.DeletePolicyRequest()
    attachment_point = f"cloudresourcemanager.googleapis.com%2Fprojects%2F{project_id}"
    request.name = f"policies/{attachment_point}/denypolicies/{policy_name}"

    operation = policies_client.delete_policy(request=request)
    print(f"Deleted the deny policy: {operation}")

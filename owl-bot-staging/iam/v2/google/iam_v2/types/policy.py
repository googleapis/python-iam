# -*- coding: utf-8 -*-
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
#
import proto  # type: ignore

from google.iam_v2.types import deny
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package='google.iam.v2',
    manifest={
        'Policy',
        'PolicyRule',
        'ListPoliciesRequest',
        'ListPoliciesResponse',
        'GetPolicyRequest',
        'CreatePolicyRequest',
        'UpdatePolicyRequest',
        'DeletePolicyRequest',
        'ListApplicablePoliciesRequest',
        'ListApplicablePoliciesResponse',
        'PolicyOperationMetadata',
    },
)


class Policy(proto.Message):
    r"""Data for an IAM policy.

    Attributes:
        name (str):
            Immutable. The resource name of the ``Policy``, which must
            be unique. Format:
            ``policies/{attachment_point}/denypolicies/{policy_id}``

            The attachment point is identified by its URL-encoded full
            resource name, which means that the forward-slash character,
            ``/``, must be written as ``%2F``. For example,
            ``policies/cloudresourcemanager.googleapis.com%2Fprojects%2Fmy-project/denypolicies/my-deny-policy``.

            For organizations and folders, use the numeric ID in the
            full resource name. For projects, requests can use the
            alphanumeric or the numeric ID. Responses always contain the
            numeric ID.
        uid (str):
            Immutable. The globally unique ID of the ``Policy``.
            Assigned automatically when the ``Policy`` is created.
        kind (str):
            Output only. The kind of the ``Policy``. Always contains the
            value ``DenyPolicy``.
        display_name (str):
            A user-specified description of the ``Policy``. This value
            can be up to 63 characters.
        annotations (Mapping[str, str]):
            A key-value map to store arbitrary metadata for the
            ``Policy``. Keys can be up to 63 characters. Values can be
            up to 255 characters.
        etag (str):
            An opaque tag that identifies the current version of the
            ``Policy``. IAM uses this value to help manage concurrent
            updates, so they do not cause one update to be overwritten
            by another.

            If this field is present in a [CreatePolicy][] request, the
            value is ignored.
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the ``Policy`` was created.
        update_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the ``Policy`` was last updated.
        delete_time (google.protobuf.timestamp_pb2.Timestamp):
            Output only. The time when the ``Policy`` was deleted. Empty
            if the policy is not deleted.
        rules (Sequence[google.iam_v2.types.PolicyRule]):
            A list of rules that specify the behavior of the ``Policy``.
            All of the rules should be of the ``kind`` specified in the
            ``Policy``.
        managing_authority (str):
            Immutable. Specifies that this policy is
            managed by an authority and can only be modified
            by that authority. Usage is restricted.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    uid = proto.Field(
        proto.STRING,
        number=2,
    )
    kind = proto.Field(
        proto.STRING,
        number=3,
    )
    display_name = proto.Field(
        proto.STRING,
        number=4,
    )
    annotations = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=5,
    )
    etag = proto.Field(
        proto.STRING,
        number=6,
    )
    create_time = proto.Field(
        proto.MESSAGE,
        number=7,
        message=timestamp_pb2.Timestamp,
    )
    update_time = proto.Field(
        proto.MESSAGE,
        number=8,
        message=timestamp_pb2.Timestamp,
    )
    delete_time = proto.Field(
        proto.MESSAGE,
        number=9,
        message=timestamp_pb2.Timestamp,
    )
    rules = proto.RepeatedField(
        proto.MESSAGE,
        number=10,
        message='PolicyRule',
    )
    managing_authority = proto.Field(
        proto.STRING,
        number=11,
    )


class PolicyRule(proto.Message):
    r"""A single rule in a ``Policy``.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        deny_rule (google.iam_v2.types.DenyRule):
            A rule for a deny policy.

            This field is a member of `oneof`_ ``kind``.
        description (str):
            A user-specified description of the rule.
            This value can be up to 256 characters.
    """

    deny_rule = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof='kind',
        message=deny.DenyRule,
    )
    description = proto.Field(
        proto.STRING,
        number=1,
    )


class ListPoliciesRequest(proto.Message):
    r"""Request message for ``ListPolicies``.

    Attributes:
        parent (str):
            Required. The resource that the policy is attached to, along
            with the kind of policy to list. Format:
            ``policies/{attachment_point}/denypolicies``

            The attachment point is identified by its URL-encoded full
            resource name, which means that the forward-slash character,
            ``/``, must be written as ``%2F``. For example,
            ``policies/cloudresourcemanager.googleapis.com%2Fprojects%2Fmy-project/denypolicies``.

            For organizations and folders, use the numeric ID in the
            full resource name. For projects, you can use the
            alphanumeric or the numeric ID.
        page_size (int):
            The maximum number of policies to return. IAM
            ignores this value and uses the value 1000.
        page_token (str):
            A page token received in a
            [ListPoliciesResponse][google.iam.v2.ListPoliciesResponse].
            Provide this token to retrieve the next page.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    page_size = proto.Field(
        proto.INT32,
        number=2,
    )
    page_token = proto.Field(
        proto.STRING,
        number=3,
    )


class ListPoliciesResponse(proto.Message):
    r"""Response message for ``ListPolicies``.

    Attributes:
        policies (Sequence[google.iam_v2.types.Policy]):
            Metadata for the policies that are attached
            to the resource.
        next_page_token (str):
            A page token that you can use in a
            [ListPoliciesRequest][google.iam.v2.ListPoliciesRequest] to
            retrieve the next page. If this field is omitted, there are
            no additional pages.
    """

    @property
    def raw_page(self):
        return self

    policies = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message='Policy',
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=2,
    )


class GetPolicyRequest(proto.Message):
    r"""Request message for ``GetPolicy``.

    Attributes:
        name (str):
            Required. The resource name of the policy to retrieve.
            Format:
            ``policies/{attachment_point}/denypolicies/{policy_id}``

            Use the URL-encoded full resource name, which means that the
            forward-slash character, ``/``, must be written as ``%2F``.
            For example,
            ``policies/cloudresourcemanager.googleapis.com%2Fprojects%2Fmy-project/denypolicies/my-policy``.

            For organizations and folders, use the numeric ID in the
            full resource name. For projects, you can use the
            alphanumeric or the numeric ID.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )


class CreatePolicyRequest(proto.Message):
    r"""Request message for ``CreatePolicy``.

    Attributes:
        parent (str):
            Required. The resource that the policy is attached to, along
            with the kind of policy to create. Format:
            ``policies/{attachment_point}/denypolicies``

            The attachment point is identified by its URL-encoded full
            resource name, which means that the forward-slash character,
            ``/``, must be written as ``%2F``. For example,
            ``policies/cloudresourcemanager.googleapis.com%2Fprojects%2Fmy-project/denypolicies``.

            For organizations and folders, use the numeric ID in the
            full resource name. For projects, you can use the
            alphanumeric or the numeric ID.
        policy (google.iam_v2.types.Policy):
            Required. The policy to create.
        policy_id (str):
            The ID to use for this policy, which will become the final
            component of the policy's resource name. The ID must contain
            3 to 63 characters. It can contain lowercase letters and
            numbers, as well as dashes (``-``) and periods (``.``). The
            first character must be a lowercase letter.
    """

    parent = proto.Field(
        proto.STRING,
        number=1,
    )
    policy = proto.Field(
        proto.MESSAGE,
        number=2,
        message='Policy',
    )
    policy_id = proto.Field(
        proto.STRING,
        number=3,
    )


class UpdatePolicyRequest(proto.Message):
    r"""Request message for ``UpdatePolicy``.

    Attributes:
        policy (google.iam_v2.types.Policy):
            Required. The policy to update.

            To prevent conflicting updates, the ``etag`` value must
            match the value that is stored in IAM. If the ``etag``
            values do not match, the request fails with a ``409`` error
            code and ``ABORTED`` status.
    """

    policy = proto.Field(
        proto.MESSAGE,
        number=1,
        message='Policy',
    )


class DeletePolicyRequest(proto.Message):
    r"""Request message for ``DeletePolicy``.

    Attributes:
        name (str):
            Required. The resource name of the policy to delete. Format:
            ``policies/{attachment_point}/denypolicies/{policy_id}``

            Use the URL-encoded full resource name, which means that the
            forward-slash character, ``/``, must be written as ``%2F``.
            For example,
            ``policies/cloudresourcemanager.googleapis.com%2Fprojects%2Fmy-project/denypolicies/my-policy``.

            For organizations and folders, use the numeric ID in the
            full resource name. For projects, you can use the
            alphanumeric or the numeric ID.
        etag (str):
            Optional. The expected ``etag`` of the policy to delete. If
            the value does not match the value that is stored in IAM,
            the request fails with a ``409`` error code and ``ABORTED``
            status.

            If you omit this field, the policy is deleted regardless of
            its current ``etag``.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    etag = proto.Field(
        proto.STRING,
        number=2,
    )


class ListApplicablePoliciesRequest(proto.Message):
    r"""``ListApplicablePoliciesRequest`` represents the Request message for
    the ``ListApplicablePolicies`` method. It provides the input for a
    filterable query of Policies that apply to a certain GCP Resource,
    specified by the field ``attachment_point``, found on this message.
    Example:

    ::

       {
          attachment_point:
          'cloudresourcemanager.googleapis.com%2Forganizations%2F212345678901'
          filter: 'kind:denyPolicies'
       }

    Attributes:
        attachment_point (str):
            Required. The Cloud resource at which the applicable
            policies are to be retrieved. Format: ``{attachment-point}``
            Use the URL-encoded full resource name, which means that the
            forward-slash character, ``/``, must be written as ``%2F``.
            For example,
            ``cloudresourcemanager.googleapis.com%2Fprojects%2Fmy-project``.
        filter (str):
            Filtering currently only supports the kind of policies to
            return, and must be in the format “kind:[policyKind1] OR
            kind:[policyKind2]”. New policy kinds may be added in the
            future without notice.

            Example value: “kind:denyPolicies”
        page_token (str):
            If present, then retrieve the batch of results following the
            results from the preceding call to this method.
            ``page_token`` must be the value of ``next_page_token``
            [ListApplicablePoliciesResponse.next_page_token][google.iam.v2.ListApplicablePoliciesResponse.next_page_token]
            from the previous response. The values of other method
            parameters should be identical to those in the previous
            call.
        page_size (int):
            Limit on the number of policies to include in the response.
            Further policies can subsequently be obtained by including
            the
            [ListApplicablePoliciesResponse.next_page_token][google.iam.admin.v1.ListApplicablePoliciesResponse.next_page_token]
            in a subsequent request. The minimum is 25, and the maximum
            is 100.
    """

    attachment_point = proto.Field(
        proto.STRING,
        number=1,
    )
    filter = proto.Field(
        proto.STRING,
        number=2,
    )
    page_token = proto.Field(
        proto.STRING,
        number=3,
    )
    page_size = proto.Field(
        proto.INT32,
        number=4,
    )


class ListApplicablePoliciesResponse(proto.Message):
    r"""Response message for [ListApplicablePolicies][] method.

    Attributes:
        policies (Sequence[google.iam_v2.types.Policy]):
            Ordered list starting from the resource on
            which this API was called then proceeding up the
            hierarchy. Policies for the same attachment
            point will be grouped, but no further ordering
            is guaranteed.
        inaccessible (Sequence[str]):
            A list of resources that the caller does not have permission
            to retrieve. List or Get can be used to get detailed error
            messages. Get:
            ``policies/{attachment-point}/denypolicies/{policy-id}``
            List: ``policies/{attachment-point}/denypolicies``
        next_page_token (str):
            A page token that can be used in a
            [ListApplicablePoliciesRequest][google.iam.v2.ListApplicablePoliciesRequest]
            to retrieve the next page. If this field is blank, there are
            no additional pages.
    """

    @property
    def raw_page(self):
        return self

    policies = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message='Policy',
    )
    inaccessible = proto.RepeatedField(
        proto.STRING,
        number=2,
    )
    next_page_token = proto.Field(
        proto.STRING,
        number=3,
    )


class PolicyOperationMetadata(proto.Message):
    r"""Metadata for long-running ``Policy`` operations.

    Attributes:
        create_time (google.protobuf.timestamp_pb2.Timestamp):
            Timestamp when the ``google.longrunning.Operation`` was
            created.
    """

    create_time = proto.Field(
        proto.MESSAGE,
        number=1,
        message=timestamp_pb2.Timestamp,
    )


__all__ = tuple(sorted(__protobuf__.manifest))

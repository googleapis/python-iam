# -*- coding: utf-8 -*-
#
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Accesses the google.iam.credentials.v1 IAMCredentials API."""

import pkg_resources
import warnings

from google.oauth2 import service_account
import google.api_core.client_options
import google.api_core.gapic_v1.client_info
import google.api_core.gapic_v1.config
import google.api_core.gapic_v1.method
import google.api_core.gapic_v1.routing_header
import google.api_core.grpc_helpers
import google.api_core.path_template
import grpc

from google.cloud.iam_credentials_v1.gapic import iam_credentials_client_config
from google.cloud.iam_credentials_v1.gapic.transports import (
    iam_credentials_grpc_transport,
)
from google.cloud.iam_credentials_v1.proto import common_pb2
from google.cloud.iam_credentials_v1.proto import iamcredentials_pb2_grpc
from google.protobuf import duration_pb2


_GAPIC_LIBRARY_VERSION = pkg_resources.get_distribution("google-cloud-iam").version


class IAMCredentialsClient(object):
    """
    A service account is a special type of Google account that belongs to your
    application or a virtual machine (VM), instead of to an individual end user.
    Your application assumes the identity of the service account to call Google
    APIs, so that the users aren't directly involved.

    Service account credentials are used to temporarily assume the identity
    of the service account. Supported credential types include OAuth 2.0 access
    tokens, OpenID Connect ID tokens, self-signed JSON Web Tokens (JWTs), and
    more.
    """

    SERVICE_ADDRESS = "iamcredentials.googleapis.com:443"
    """The default address of the service."""

    # The name of the interface for this client. This is the key used to
    # find the method configuration in the client_config dictionary.
    _INTERFACE_NAME = "google.iam.credentials.v1.IAMCredentials"

    @classmethod
    def from_service_account_file(cls, filename, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            IAMCredentialsClient: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @classmethod
    def service_account_path(cls, project, service_account):
        """Return a fully-qualified service_account string."""
        return google.api_core.path_template.expand(
            "projects/{project}/serviceAccounts/{service_account}",
            project=project,
            service_account=service_account,
        )

    def __init__(
        self,
        transport=None,
        channel=None,
        credentials=None,
        client_config=None,
        client_info=None,
        client_options=None,
    ):
        """Constructor.

        Args:
            transport (Union[~.IamCredentialsGrpcTransport,
                    Callable[[~.Credentials, type], ~.IamCredentialsGrpcTransport]): A transport
                instance, responsible for actually making the API calls.
                The default transport uses the gRPC protocol.
                This argument may also be a callable which returns a
                transport instance. Callables will be sent the credentials
                as the first argument and the default transport class as
                the second argument.
            channel (grpc.Channel): DEPRECATED. A ``Channel`` instance
                through which to make calls. This argument is mutually exclusive
                with ``credentials``; providing both will raise an exception.
            credentials (google.auth.credentials.Credentials): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is mutually exclusive with providing a
                transport instance to ``transport``; doing so will raise
                an exception.
            client_config (dict): DEPRECATED. A dictionary of call options for
                each method. If not specified, the default configuration is used.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            client_options (Union[dict, google.api_core.client_options.ClientOptions]):
                Client options used to set user options on the client. API Endpoint
                should be set through client_options.
        """
        # Raise deprecation warnings for things we want to go away.
        if client_config is not None:
            warnings.warn(
                "The `client_config` argument is deprecated.",
                PendingDeprecationWarning,
                stacklevel=2,
            )
        else:
            client_config = iam_credentials_client_config.config

        if channel:
            warnings.warn(
                "The `channel` argument is deprecated; use " "`transport` instead.",
                PendingDeprecationWarning,
                stacklevel=2,
            )

        api_endpoint = self.SERVICE_ADDRESS
        if client_options:
            if type(client_options) == dict:
                client_options = google.api_core.client_options.from_dict(
                    client_options
                )
            if client_options.api_endpoint:
                api_endpoint = client_options.api_endpoint

        # Instantiate the transport.
        # The transport is responsible for handling serialization and
        # deserialization and actually sending data to the service.
        if transport:
            if callable(transport):
                self.transport = transport(
                    credentials=credentials,
                    default_class=iam_credentials_grpc_transport.IamCredentialsGrpcTransport,
                    address=api_endpoint,
                )
            else:
                if credentials:
                    raise ValueError(
                        "Received both a transport instance and "
                        "credentials; these are mutually exclusive."
                    )
                self.transport = transport
        else:
            self.transport = iam_credentials_grpc_transport.IamCredentialsGrpcTransport(
                address=api_endpoint, channel=channel, credentials=credentials
            )

        if client_info is None:
            client_info = google.api_core.gapic_v1.client_info.ClientInfo(
                gapic_version=_GAPIC_LIBRARY_VERSION
            )
        else:
            client_info.gapic_version = _GAPIC_LIBRARY_VERSION
        self._client_info = client_info

        # Parse out the default settings for retry and timeout for each RPC
        # from the client configuration.
        # (Ordinarily, these are the defaults specified in the `*_config.py`
        # file next to this one.)
        self._method_configs = google.api_core.gapic_v1.config.parse_method_configs(
            client_config["interfaces"][self._INTERFACE_NAME]
        )

        # Save a dictionary of cached API call functions.
        # These are the actual callables which invoke the proper
        # transport methods, wrapped with `wrap_method` to add retry,
        # timeout, and the like.
        self._inner_api_calls = {}

    # Service calls
    def generate_access_token(
        self,
        name,
        scope,
        delegates=None,
        lifetime=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Generates an OAuth 2.0 access token for a service account.

        Example:
            >>> from google.cloud import iam_credentials_v1
            >>>
            >>> client = iam_credentials_v1.IAMCredentialsClient()
            >>>
            >>> name = client.service_account_path('[PROJECT]', '[SERVICE_ACCOUNT]')
            >>>
            >>> # TODO: Initialize `scope`:
            >>> scope = []
            >>>
            >>> response = client.generate_access_token(name, scope)

        Args:
            name (str): Required. The resource name of the service account for which the
                credentials are requested, in the following format:
                ``projects/-/serviceAccounts/{ACCOUNT_EMAIL_OR_UNIQUEID}``. The ``-``
                wildcard character is required; replacing it with a project ID is
                invalid.
            scope (list[str]): Required. Code to identify the scopes to be included in the OAuth 2.0 access token.
                See https://developers.google.com/identity/protocols/googlescopes for more
                information.
                At least one value required.
            delegates (list[str]): The sequence of service accounts in a delegation chain. Each service
                account must be granted the ``roles/iam.serviceAccountTokenCreator``
                role on its next service account in the chain. The last service account
                in the chain must be granted the
                ``roles/iam.serviceAccountTokenCreator`` role on the service account
                that is specified in the ``name`` field of the request.

                The delegates must have the following format:
                ``projects/-/serviceAccounts/{ACCOUNT_EMAIL_OR_UNIQUEID}``. The ``-``
                wildcard character is required; replacing it with a project ID is
                invalid.
            lifetime (Union[dict, ~google.cloud.iam_credentials_v1.types.Duration]): The desired lifetime duration of the access token in seconds.
                Must be set to a value less than or equal to 3600 (1 hour). If a value is
                not specified, the token's lifetime will be set to a default value of one
                hour.

                If a dict is provided, it must be of the same form as the protobuf
                message :class:`~google.cloud.iam_credentials_v1.types.Duration`
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.iam_credentials_v1.types.GenerateAccessTokenResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "generate_access_token" not in self._inner_api_calls:
            self._inner_api_calls[
                "generate_access_token"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.generate_access_token,
                default_retry=self._method_configs["GenerateAccessToken"].retry,
                default_timeout=self._method_configs["GenerateAccessToken"].timeout,
                client_info=self._client_info,
            )

        request = common_pb2.GenerateAccessTokenRequest(
            name=name, scope=scope, delegates=delegates, lifetime=lifetime
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["generate_access_token"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def generate_id_token(
        self,
        name,
        audience,
        delegates=None,
        include_email=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Generates an OpenID Connect ID token for a service account.

        Example:
            >>> from google.cloud import iam_credentials_v1
            >>>
            >>> client = iam_credentials_v1.IAMCredentialsClient()
            >>>
            >>> name = client.service_account_path('[PROJECT]', '[SERVICE_ACCOUNT]')
            >>>
            >>> # TODO: Initialize `audience`:
            >>> audience = ''
            >>>
            >>> response = client.generate_id_token(name, audience)

        Args:
            name (str): Required. The resource name of the service account for which the
                credentials are requested, in the following format:
                ``projects/-/serviceAccounts/{ACCOUNT_EMAIL_OR_UNIQUEID}``. The ``-``
                wildcard character is required; replacing it with a project ID is
                invalid.
            audience (str): Required. The audience for the token, such as the API or account that this token
                grants access to.
            delegates (list[str]): The sequence of service accounts in a delegation chain. Each service
                account must be granted the ``roles/iam.serviceAccountTokenCreator``
                role on its next service account in the chain. The last service account
                in the chain must be granted the
                ``roles/iam.serviceAccountTokenCreator`` role on the service account
                that is specified in the ``name`` field of the request.

                The delegates must have the following format:
                ``projects/-/serviceAccounts/{ACCOUNT_EMAIL_OR_UNIQUEID}``. The ``-``
                wildcard character is required; replacing it with a project ID is
                invalid.
            include_email (bool): Include the service account email in the token. If set to ``true``,
                the token will contain ``email`` and ``email_verified`` claims.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.iam_credentials_v1.types.GenerateIdTokenResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "generate_id_token" not in self._inner_api_calls:
            self._inner_api_calls[
                "generate_id_token"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.generate_id_token,
                default_retry=self._method_configs["GenerateIdToken"].retry,
                default_timeout=self._method_configs["GenerateIdToken"].timeout,
                client_info=self._client_info,
            )

        request = common_pb2.GenerateIdTokenRequest(
            name=name,
            audience=audience,
            delegates=delegates,
            include_email=include_email,
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["generate_id_token"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def sign_blob(
        self,
        name,
        payload,
        delegates=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Signs a blob using a service account's system-managed private key.

        Example:
            >>> from google.cloud import iam_credentials_v1
            >>>
            >>> client = iam_credentials_v1.IAMCredentialsClient()
            >>>
            >>> name = client.service_account_path('[PROJECT]', '[SERVICE_ACCOUNT]')
            >>>
            >>> # TODO: Initialize `payload`:
            >>> payload = b''
            >>>
            >>> response = client.sign_blob(name, payload)

        Args:
            name (str): Required. The resource name of the service account for which the
                credentials are requested, in the following format:
                ``projects/-/serviceAccounts/{ACCOUNT_EMAIL_OR_UNIQUEID}``. The ``-``
                wildcard character is required; replacing it with a project ID is
                invalid.
            payload (bytes): Required. The bytes to sign.
            delegates (list[str]): The sequence of service accounts in a delegation chain. Each service
                account must be granted the ``roles/iam.serviceAccountTokenCreator``
                role on its next service account in the chain. The last service account
                in the chain must be granted the
                ``roles/iam.serviceAccountTokenCreator`` role on the service account
                that is specified in the ``name`` field of the request.

                The delegates must have the following format:
                ``projects/-/serviceAccounts/{ACCOUNT_EMAIL_OR_UNIQUEID}``. The ``-``
                wildcard character is required; replacing it with a project ID is
                invalid.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.iam_credentials_v1.types.SignBlobResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "sign_blob" not in self._inner_api_calls:
            self._inner_api_calls[
                "sign_blob"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.sign_blob,
                default_retry=self._method_configs["SignBlob"].retry,
                default_timeout=self._method_configs["SignBlob"].timeout,
                client_info=self._client_info,
            )

        request = common_pb2.SignBlobRequest(
            name=name, payload=payload, delegates=delegates
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["sign_blob"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

    def sign_jwt(
        self,
        name,
        payload,
        delegates=None,
        retry=google.api_core.gapic_v1.method.DEFAULT,
        timeout=google.api_core.gapic_v1.method.DEFAULT,
        metadata=None,
    ):
        """
        Signs a JWT using a service account's system-managed private key.

        Example:
            >>> from google.cloud import iam_credentials_v1
            >>>
            >>> client = iam_credentials_v1.IAMCredentialsClient()
            >>>
            >>> name = client.service_account_path('[PROJECT]', '[SERVICE_ACCOUNT]')
            >>>
            >>> # TODO: Initialize `payload`:
            >>> payload = ''
            >>>
            >>> response = client.sign_jwt(name, payload)

        Args:
            name (str): Required. The resource name of the service account for which the
                credentials are requested, in the following format:
                ``projects/-/serviceAccounts/{ACCOUNT_EMAIL_OR_UNIQUEID}``. The ``-``
                wildcard character is required; replacing it with a project ID is
                invalid.
            payload (str): Required. The JWT payload to sign: a JSON object that contains a JWT Claims Set.
            delegates (list[str]): The sequence of service accounts in a delegation chain. Each service
                account must be granted the ``roles/iam.serviceAccountTokenCreator``
                role on its next service account in the chain. The last service account
                in the chain must be granted the
                ``roles/iam.serviceAccountTokenCreator`` role on the service account
                that is specified in the ``name`` field of the request.

                The delegates must have the following format:
                ``projects/-/serviceAccounts/{ACCOUNT_EMAIL_OR_UNIQUEID}``. The ``-``
                wildcard character is required; replacing it with a project ID is
                invalid.
            retry (Optional[google.api_core.retry.Retry]):  A retry object used
                to retry requests. If ``None`` is specified, requests will
                be retried using a default configuration.
            timeout (Optional[float]): The amount of time, in seconds, to wait
                for the request to complete. Note that if ``retry`` is
                specified, the timeout applies to each individual attempt.
            metadata (Optional[Sequence[Tuple[str, str]]]): Additional metadata
                that is provided to the method.

        Returns:
            A :class:`~google.cloud.iam_credentials_v1.types.SignJwtResponse` instance.

        Raises:
            google.api_core.exceptions.GoogleAPICallError: If the request
                    failed for any reason.
            google.api_core.exceptions.RetryError: If the request failed due
                    to a retryable error and retry attempts failed.
            ValueError: If the parameters are invalid.
        """
        # Wrap the transport method to add retry and timeout logic.
        if "sign_jwt" not in self._inner_api_calls:
            self._inner_api_calls[
                "sign_jwt"
            ] = google.api_core.gapic_v1.method.wrap_method(
                self.transport.sign_jwt,
                default_retry=self._method_configs["SignJwt"].retry,
                default_timeout=self._method_configs["SignJwt"].timeout,
                client_info=self._client_info,
            )

        request = common_pb2.SignJwtRequest(
            name=name, payload=payload, delegates=delegates
        )
        if metadata is None:
            metadata = []
        metadata = list(metadata)
        try:
            routing_header = [("name", name)]
        except AttributeError:
            pass
        else:
            routing_metadata = google.api_core.gapic_v1.routing_header.to_grpc_metadata(
                routing_header
            )
            metadata.append(routing_metadata)

        return self._inner_api_calls["sign_jwt"](
            request, retry=retry, timeout=timeout, metadata=metadata
        )

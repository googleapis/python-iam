# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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

from google.cloud.iam_credentials_v1.services.iam_credentials.client import IAMCredentialsClient
from google.cloud.iam_credentials_v1.services.iam_credentials.async_client import IAMCredentialsAsyncClient

from google.cloud.iam_credentials_v1.types.common import GenerateAccessTokenRequest
from google.cloud.iam_credentials_v1.types.common import GenerateAccessTokenResponse
from google.cloud.iam_credentials_v1.types.common import GenerateIdTokenRequest
from google.cloud.iam_credentials_v1.types.common import GenerateIdTokenResponse
from google.cloud.iam_credentials_v1.types.common import SignBlobRequest
from google.cloud.iam_credentials_v1.types.common import SignBlobResponse
from google.cloud.iam_credentials_v1.types.common import SignJwtRequest
from google.cloud.iam_credentials_v1.types.common import SignJwtResponse

__all__ = ('IAMCredentialsClient',
    'IAMCredentialsAsyncClient',
    'GenerateAccessTokenRequest',
    'GenerateAccessTokenResponse',
    'GenerateIdTokenRequest',
    'GenerateIdTokenResponse',
    'SignBlobRequest',
    'SignBlobResponse',
    'SignJwtRequest',
    'SignJwtResponse',
)

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

import os
import re

import pytest
from _pytest.capture import CaptureFixture

from samples.snippets.deny_policies import create_deny_policy, delete_deny_policy, get_deny_policy, list_deny_policy, \
    update_deny_policy

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
GOOGLE_APPLICATION_CREDENTIALS = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]


@pytest.fixture
def deny_policy():
    policy_name = "limit-project-deletion"

    create_deny_policy(PROJECT_ID, policy_name)

    yield policy_name

    delete_deny_policy(PROJECT_ID, policy_name)


def test_retrieve_and_update_policy(capsys: CaptureFixture, deny_policy):
    get_deny_policy(PROJECT_ID, deny_policy)
    out, _ = capsys.readouterr()
    assert re.search("Retrieved the deny policy", out)

    list_deny_policy(PROJECT_ID)
    out, _ = capsys.readouterr()
    assert re.search("Listed all deny policies", out)

    update_deny_policy(PROJECT_ID, deny_policy)
    out, _ = capsys.readouterr()
    assert re.search("Updated the deny policy", out)

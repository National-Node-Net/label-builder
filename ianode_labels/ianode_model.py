# SPDX-License-Identifier: Apache-2.0
# Originally developed by Telicent Ltd.; subsequently adapted, enhanced, and maintained by the National Digital Twin Programme.


# Copyright (c) Telicent Ltd.
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

# Modifications made by the National Digital Twin Programme (NDTP)
# © Crown Copyright 2026. This work has been developed by the National Digital Twin Programme
# and is legally attributed to the UK's Department for Business, Innovation, Science and Trade (BIST) as the governing entity.


import logging
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Annotated

from pydantic import AwareDatetime, BaseModel, PlainSerializer, field_validator

from ianode_labels.security_labels import SecurityLabelBuilder
from ianode_labels.ianodev2 import IANodeSecurityLabelsV2


log = logging.getLogger(__name__)

DEFAULT_OPTIONAL_DT = datetime(2023, 12, 14, 0, 0, 0, tzinfo=timezone.utc)
SerialisableDt = Annotated[AwareDatetime, PlainSerializer(lambda x: x.isoformat(), return_type=str, when_used="always")]


class IANodeMixin(BaseModel, ABC):
    @abstractmethod
    def build_security_labels(self):
        pass


class IANodeModel(IANodeMixin):
    apiVersion: str | None = "v1alpha"
    specification: str | None = "***REDACTED***"
    identifier: str
    classification: str
    permittedOrgs: list[str]
    permittedNats: list[str]
    orGroups: list[str]
    andGroups: list[str]

    createdDateTime: SerialisableDt | None = DEFAULT_OPTIONAL_DT
    originator: str | None = None
    custodian: str | None = None
    policyRef: str | None = None
    dataSet: list[str]
    authRef: list[str]
    dispositionDate: SerialisableDt | None = DEFAULT_OPTIONAL_DT
    dispositionProcess: str | None = None
    dissemination: list[str]

    @field_validator('classification')
    def non_empty_string(cls, value: str, info):
        if value.strip() == "":
            raise ValueError(f"The {info.field_name} field cannot be an empty string.")
        return value

    @field_validator('permittedOrgs', 'permittedNats', 'orGroups', 'andGroups', 'dataSet',
                     'authRef', 'dissemination', mode='before')
    def non_empty_list(cls, value: list[str], info):
        clean_list = [x for x in value if x]
        if not clean_list or len(clean_list) == 0:
            raise ValueError(f"The {info.field_name} field cannot be an empty list.")
        return value

    def build_security_labels(self):
        builder = SecurityLabelBuilder()

        builder.add(IANodeSecurityLabelsV2.CLASSIFICATION.value, self.classification)
        builder.add_multiple(IANodeSecurityLabelsV2.PERMITTED_ORGANISATIONS.value, *self.permittedOrgs)
        builder.add_multiple(IANodeSecurityLabelsV2.PERMITTED_NATIONALITIES.value, *self.permittedNats)
        builder.add_multiple(IANodeSecurityLabelsV2.AND_GROUPS.value, *self.andGroups)
        builder.add_multiple(IANodeSecurityLabelsV2.OR_GROUPS.value, *self.orGroups)

        return builder.build()

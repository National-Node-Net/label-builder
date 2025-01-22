import logging
from datetime import datetime, timezone
from typing import Annotated

from pydantic import AwareDatetime, BaseModel, PlainSerializer, field_validator

from ianode_labels.security_labels import SecurityLabelBuilder
from ianode_labels.ianodev2 import IANodeSecurityLabelsV2

__license__ = """
Copyright (c) Telicent Ltd.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

log = logging.getLogger(__name__)

DEFAULT_OPTIONAL_DT = datetime(2023, 12, 14, 0, 0, 0, tzinfo=timezone.utc)
SerialisableDt = Annotated[AwareDatetime, PlainSerializer(lambda x: x.isoformat(), return_type=str, when_used="always")]


class IANodeMixin(BaseModel):
    def build_security_labels(self):
        print(self.creationDate)
        builder = SecurityLabelBuilder()

        builder.add(IANodeSecurityLabelsV2.CLASSIFICATION.value, self.access.classification)
        if len(self.access.allowedOrgs) > 0:
            builder.add_multiple(IANodeSecurityLabelsV2.PERMITTED_ORGANISATIONS.value, *self.access.allowedOrgs)
        if len(self.access.allowedNats) > 0:
            builder.add_multiple(IANodeSecurityLabelsV2.PERMITTED_NATIONALITIES.value, *self.access.allowedNats)
        if len(self.access.groups) > 0:
            builder.add_multiple(IANodeSecurityLabelsV2.AND_GROUPS.value, *self.access.groups)

        return builder.build()



class AccessModel(BaseModel):
    classification: str
    allowedOrgs: list[str]
    allowedNats: list[str]
    groups: list[str]

    @field_validator('classification')
    def non_empty_string(cls, value: str, info):
        if value.strip() == "":
            raise ValueError(f"The {info.field_name} field cannot be an empty string.")
        if value.strip() not in ("O", "OS", "S", "TS"):
            raise ValueError(f"The {info.field_name} field must be 'O', 'OS', 'S' or 'TS'.")
        return value


class OwnershipModel(BaseModel):
    originatingOrg: str
    user: str | None = None

class IDHModel(IANodeMixin):

    apiVersion: str | None = "v1alpha"
    uuid: str
    creationDate: SerialisableDt | None = DEFAULT_OPTIONAL_DT
    containsPii: bool
    dataSource: str | None = None
    ownership: OwnershipModel
    access: AccessModel

    def build_security_labels(self):
        return super().build_security_labels()

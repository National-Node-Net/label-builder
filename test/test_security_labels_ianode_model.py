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


import unittest

from ianode_labels import SecurityLabelBuilder, IANodeLabelsV1


class SecurityLabelBuilderTestCase(unittest.TestCase):
    def test_simple_single_label_access(self):
        pn = IANodeLabelsV1.CLASSIFICATION.value
        test_classifcation = "S"

        basic_label = pn.create_label(test_classifcation)

        self.assertEqual(basic_label, "clearance=S")

        multi_label = pn.construct(test_classifcation)

        self.assertEqual(multi_label, "clearance=S")

    def test_simple_multi_label_access(self):
        pn = IANodeLabelsV1.PERMITTED_NATIONALITIES.value
        test_nationality_1 = "GBR"
        test_nationality_2 = "NOR"
        basic_label = pn.create_label(test_nationality_1)

        self.assertEqual(basic_label, "nationality=GBR")

        multi_label = pn.construct(test_nationality_1, test_nationality_2)

        self.assertEqual(multi_label, "(nationality=GBR|nationality=NOR)")

    def test_security_label_builder(self):
        test_org_1 = "ndtp"
        test_org_2 = "nhs"
        test_classification = "S"
        test_classification_1 = "O"
        slb1 = (
            SecurityLabelBuilder()
            .add_multiple(
                IANodeLabelsV1.PERMITTED_ORGANISATIONS.value,
                test_org_1,
                test_org_2,
            )
            .add(IANodeLabelsV1.CLASSIFICATION.value, test_classification)
            .build()
        )
        self.assertEqual(
            slb1,
            "((deployed_organisation=ndtp|deployed_organisation=nhs)&clearance=S)",
        )

        slb2 = (
            SecurityLabelBuilder()
            .add(IANodeLabelsV1.PERMITTED_ORGANISATIONS.value, test_org_1)
            .add(IANodeLabelsV1.CLASSIFICATION.value, test_classification_1)
            .build()
        )

        self.assertEqual(
            slb2,
            "((deployed_organisation=ndtp)&clearance=O)",
        )

        slb3 = (
            SecurityLabelBuilder()
            .add_or_expression(slb1)
            .add_or_expression(slb2)
            .build()
        )

        self.assertEqual(
            slb3,
            "((deployed_organisation=ndtp|deployed_organisation=nhs)&clearance=S)|"
            "((deployed_organisation=ndtp)&clearance=O)",
        )

        slb4 = (
            SecurityLabelBuilder()
            .add_multiple(
                IANodeLabelsV1.PERMITTED_ORGANISATIONS.value,
                test_org_1,
                test_org_2,
            )
            .add(IANodeLabelsV1.CLASSIFICATION.value, test_classification)
            .add_or_expression(slb2)
            .build()
        )

        self.assertEqual(
            slb4,
            "((deployed_organisation=ndtp|deployed_organisation=nhs)&clearance=S)|"
            "((deployed_organisation=ndtp)&clearance=O)",
        )

    def test_security_label_builder_complex(self):
        test_org_1 = "nhs"
        test_classification = "S"

        test_nationality_1 = "GBR"
        test_nationality_2 = "USA"

        slb = (
            SecurityLabelBuilder()
            .add(IANodeLabelsV1.PERMITTED_ORGANISATIONS.value, test_org_1)
            .add(IANodeLabelsV1.CLASSIFICATION.value, test_classification)
            .add_multiple(
                IANodeLabelsV1.PERMITTED_NATIONALITIES.value,
                test_nationality_1,
                test_nationality_2,
            )
            .build()
        )
        self.assertEqual(
            slb,
            "((deployed_organisation=nhs)&clearance=S&(nationality=GBR|nationality=USA))",
        )

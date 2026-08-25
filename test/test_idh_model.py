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

from ianode_labels import IDHModel


class IDHModelTestCase(unittest.TestCase):
    def test_simple_label(self):
        label = {
            "apiVersion": "v1alpha",
            "uuid": "test_Abc_123",
            "creationDate": "2024-09-27 00:00:00+00:00",
            "containsPii": False,
            "dataSource": "Tom Test",
            "access": {
                "classification": "O",
                "allowedOrgs": ["NDTP"],
                "allowedNats": ["GBR"],
                "groups": ["urn:ndtp:groups:developer"]
            },
            "ownership":{
                "originatingOrg": "NDTP"
            }
        }

        security_label = IDHModel(**label).build_security_labels()
        self.assertEqual(security_label, "(classification=O&(permitted_organisations=NDTP)&"
                                         "(permitted_nationalities=GBR)&urn:ndtp:groups:developer:and)")
    def test_simple_label_multi_group(self):
        label = {
            "apiVersion": "v1alpha",
            "uuid": "test_Abc_123",
            "creationDate": "2024-09-27 00:00:00+00:00",
            "containsPii": False,
            "dataSource": "Tom Test",
            "access": {
                "classification": "O",
                "allowedOrgs": ["NDTP"],
                "allowedNats": ["GBR"],
                "groups": ["urn:ndtp:groups:developer", "urn:ndtp:groups:africa"]
            },
            "ownership":{
                "originatingOrg": "NDTP"
            }
        }

        security_label = IDHModel(**label).build_security_labels()
        self.assertEqual(security_label, "(classification=O&(permitted_organisations=NDTP)&"
                                         "(permitted_nationalities=GBR)&urn:ndtp:groups:developer:and&"
                                         "urn:ndtp:groups:africa:and)")
    def test_simple_label_multi_nationality(self):
        label = {
            "apiVersion": "v1alpha",
            "uuid": "test_Abc_123",
            "creationDate": "2024-09-27 00:00:00+00:00",
            "containsPii": False,
            "dataSource": "Tom Test",
            "access": {
                "classification": "O",
                "allowedOrgs": ["NDTP"],
                "allowedNats": ["GBR", "FRA"],
                "groups": ["urn:ndtp:groups:developer", "urn:ndtp:groups:africa"]
            },
            "ownership":{
                "originatingOrg": "NDTP"
            }
        }

        security_label = IDHModel(**label).build_security_labels()
        self.assertEqual(security_label, "(classification=O&(permitted_organisations=NDTP)&"
                                         "(permitted_nationalities=GBR|permitted_nationalities=FRA)&"
                                         "urn:ndtp:groups:developer:and&urn:ndtp:groups:africa:and)")
    def test_simple_label_multi_organisation(self):
        label = {
            "apiVersion": "v1alpha",
            "uuid": "test_Abc_123",
            "creationDate": "2024-09-27 00:00:00+00:00",
            "containsPii": False,
            "dataSource": "Tom Test",
            "access": {
                "classification": "O",
                "allowedOrgs": ["NDTP", "NHS"],
                "allowedNats": ["GBR", "FRA"],
                "groups": ["urn:ndtp:groups:developer", "urn:ndtp:groups:africa"]
            },
            "ownership":{
                "originatingOrg": "NDTP"
            }
        }

        security_label = IDHModel(**label).build_security_labels()
        self.assertEqual(security_label, "(classification=O&"
                                         "(permitted_organisations=NDTP|permitted_organisations=NHS)&"
                                         "(permitted_nationalities=GBR|permitted_nationalities=FRA)&"
                                         "urn:ndtp:groups:developer:and&urn:ndtp:groups:africa:and)")

    def test_error_label_no_classification(self):
        label = {
            "apiVersion": "v1alpha",
            "uuid": "test_Abc_123",
            "creationDate": "2024-09-27 00:00:00+00:00",
            "containsPii": False,
            "dataSource": "Tom Test",
            "access": {
                "classification": "",
                "allowedOrgs": ["NDTP", "NHS"],
                "allowedNats": ["GBR", "FRA"],
                "groups": ["urn:ndtp:groups:developer", "urn:ndtp:groups:africa"]
            },
            "ownership":{
                "originatingOrg": "NDTP"
            }
        }
        with self.assertRaises(ValueError) as context:
            IDHModel(**label)
        self.assertTrue("The classification field cannot be an empty string" in str(context.exception) )

    def test_error_label_wrong_classification(self):
        label = {
            "apiVersion": "v1alpha",
            "uuid": "test_Abc_123",
            "creationDate": "2024-09-27 00:00:00+00:00",
            "containsPii": False,
            "dataSource": "Tom Test",
            "access": {
                "classification": "P",
                "allowedOrgs": ["NDTP", "NHS"],
                "allowedNats": ["GBR", "FRA"],
                "groups": ["urn:ndtp:groups:developer", "urn:ndtp:groups:africa"]
            },
            "ownership":{
                "originatingOrg": "NDTP"
            }
        }
        with self.assertRaises(ValueError) as context:
            IDHModel(**label)
        self.assertTrue("The classification field must be 'O', 'OS', 'S' or 'TS'." in str(context.exception) )

    def test_simple_label_only_classification(self):
        label = {
            "apiVersion": "v1alpha",
            "uuid": "test_Abc_123",
            "creationDate": "2024-09-27 00:00:00+00:00",
            "containsPii": False,
            "dataSource": "Tom Test",
            "access": {
                "classification": "O",
                "allowedOrgs": [],
                "allowedNats": [],
                "groups": []
            },
            "ownership":{
                "originatingOrg": "NDTP"
            }
        }

        security_label = IDHModel(**label).build_security_labels()
        self.assertEqual(security_label, "(classification=O)")

    def test_error_label_missing_fields(self):
        label = {
            "apiVersion": "v1alpha",
            "uuid": "test_Abc_123",
            "creationDate": "2024-09-27 00:00:00+00:00",
            "containsPii": False,
            "dataSource": "Tom Test",
            "access": {
                "classification": "O",

            },
            "ownership":{
                "originatingOrg": "NDTP"
            }
        }

        with self.assertRaises(ValueError) as context:
            IDHModel(**label)

        self.assertTrue("access.allowedNats" in str(context.exception) )
        self.assertTrue("access.allowedOrgs" in str(context.exception) )
        self.assertTrue("access.groups" in str(context.exception) )

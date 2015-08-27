# Copyright (c) 2014 Scopely, Inc.
# Copyright (c) 2015 Mitch Garnaat
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
import unittest
import os

import mock

from skew import scan
from tests.unit.mock_awsclient import get_awsclient
import skew.awsclient

skew.awsclient.get_awsclient = get_awsclient


class TestARN(unittest.TestCase):

    def setUp(self):
        self.environ = {}
        self.environ_patch = mock.patch('os.environ', self.environ)
        self.environ_patch.start()
        credential_path = os.path.join(os.path.dirname(__file__), 'cfg',
                                       'aws_credentials')
        self.environ['AWS_CONFIG_FILE'] = credential_path
        config_path = os.path.join(os.path.dirname(__file__), 'cfg',
                                   'skew.yml')
        self.environ['SKEW_CONFIG'] = config_path

    def tearDown(self):
        pass

    def test_ec2_instance(self):
        arn = scan('arn:aws:ec2:us-west-2:123456789012:instance/*')
        # Fetch all Instance resources
        l = list(arn)
        self.assertEqual(len(l), 2)

    def test_ec2_keypairs(self):
        arn = scan('arn:aws:ec2:*:234567890123:key-pair/*')
        l = list(arn)
        self.assertEqual(len(l), 2)

    def test_ec2_securitygroup(self):
        arn = scan('arn:aws:ec2:*:123456789012:security-group/*')
        l = list(arn)
        self.assertEqual(len(l), 10)

    def test_elb_loadbalancer(self):
        arn = scan('arn:aws:elb:us-west-2:123456789012:loadbalancer/*')
        l = list(arn)
        self.assertEqual(len(l), 1)
        arn = scan('arn:aws:elb:us-west-2:234567890123:loadbalancer/*')
        l = list(arn)
        self.assertEqual(len(l), 5)

    def test_vpcs(self):
        arn = scan('arn:aws:ec2:us-west-2:123456789012:vpc/*')
        l = list(arn)
        self.assertEqual(len(l), 2)

    def test_routetable(self):
        arn = scan('arn:aws:ec2:us-west-2:123456789012:route-table/*')
        l = list(arn)
        self.assertEqual(len(l), 3)

    def test_network_acls(self):
        arn = scan('arn:aws:ec2:us-west-2:123456789012:network-acl/*')
        l = list(arn)
        self.assertEqual(len(l), 4)

    def test_users(self):
        arn = scan('arn:aws:iam:us-east-1:234567890123:user/*')
        l = list(arn)
        self.assertEqual(len(l), 3)
        arn = scan('arn:aws:iam:us-east-1:234567890123:user/foo')
        l = list(arn)
        self.assertEqual(len(l), 1)

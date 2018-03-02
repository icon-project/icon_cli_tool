#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2018 theloop Inc.
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

import hashlib
from secp256k1 import PrivateKey


class IcxSigner(object):

    def __init__(self, data=None, raw=None):
        """
        :param data(object): bytes or der
        :param raw(bool): True(bytes) False(der)
        """
        self.__private_key = PrivateKey(data, raw)

    @property
    def private_key_bytes(self):
        return self.__private_key.private_key

    @private_key_bytes.setter
    def private_key(self, data):
        self.__private_key.set_raw_privkey(data)

    @property
    def public_key_bytes(self):
        return self.__private_key.pubkey.serialize(compressed=False)

    @property
    def address(self):
        public_key_bytes = self.public_key_bytes
        return hashlib.sha3_256(public_key_bytes[1:]).digest()[-20:]

    @staticmethod
    def from_bytes(data):
        return IcxSigner(data, raw=True)

    @staticmethod
    def from_der(data):
        return IcxSigner(data, raw=False)
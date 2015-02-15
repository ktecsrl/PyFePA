##################################################################################################################
#
# Copyright (C) 2014 KTec S.r.l.
#
# Author: Luigi Di Naro: Luigi.DiNaro@KTec.it
#
# This program is free software: you can redistribute it and/or modify it under the terms of the
# GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
#
###################################################################################################################

"""Unit test for fepa.py"""

from PyFePA import fepa
import unittest
from xml.etree import ElementTree
from PyFePA import serializer
import os

DPATH = os.path.dirname(os.path.abspath(__file__))


class fepaTest(unittest.TestCase):

    def testData1(self):
        with open(DPATH+'/IT01234567890_11001.xml', 'rt') as f:
            tree = ElementTree.parse(f)
            fe = serializer.deserialize(element=tree)
            strxml = serializer.serializer(fe,'xml')
            self.assertIsInstance(strxml, str)
            self.assertIsInstance(fe, fepa.FatturaElettronica)

    def testData2(self):
        with open(DPATH+'/IT01234567890_11002.xml', 'rt') as f:
            tree = ElementTree.parse(f)
            fe = serializer.deserialize(element=tree)
            strxml = serializer.serializer(fe,'xml')
            self.assertIsInstance(strxml, str)
            self.assertIsInstance(fe, fepa.FatturaElettronica)

    def testData3(self):
        with open(DPATH+'/IT01234567890_11003.xml', 'rt') as f:
            tree = ElementTree.parse(f)
            fe = serializer.deserialize(element=tree)
            strxml = serializer.serializer(fe,'xml')
            self.assertIsInstance(strxml, str)
            self.assertIsInstance(fe, fepa.FatturaElettronica)

    def testData4(self):
        with open(DPATH+'/IT01234567890_11004.xml', 'rt') as f:
            tree = ElementTree.parse(f)
            fe = serializer.deserialize(element=tree)
            strxml = serializer.serializer(fe,'xml')
            self.assertIsInstance(strxml, str)
            self.assertIsInstance(fe, fepa.FatturaElettronica)
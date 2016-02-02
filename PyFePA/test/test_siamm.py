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

"""Unit test for siamm.py"""

import PyFePA.siamm as siamm
import datetime
import unittest

rtag = ('beneficiario', 'tipopagamento', 'entepagante', 'numerofattura', 'registro', 'datafattura',
        'importototale', 'importoiva', 'sede', 'datainizioprestazione', 'datafineprestazione',
        'nomemagistrato', 'cognomemagistrato', 'tipointercettazione')

otag = ('id', 'nr_rg', 'numeromodello37')

testdata = {'beneficiario': 'IT04578140875',
            'tipopagamento': 'AC',
            'id': 123,
            'entepagante': 'F',
            'numerofattura': 'E021',
            'registro': 'NOTI',
            'datafattura': datetime.datetime.strptime('2014-11-28T00:00:00', '%Y-%m-%dT%H:%M:%S'),
            'dataemissioneprovv': datetime.datetime.strptime('2014-11-28T00:00:00', '%Y-%m-%dT%H:%M:%S'),
            'importototale': 14480.00,
            'importoiva': 3185.60,
            'nr_rg': '000001/2012',
            'sede': '08500402104',
            'numeromodello37': None,
            'datainizioprestazione': datetime.datetime.strptime('2014-07-31T00:00:00', '%Y-%m-%dT%H:%M:%S'),
            'datafineprestazione': datetime.datetime.strptime('2014-10-20T00:00:00', '%Y-%m-%dT%H:%M:%S'),
            'nomemagistrato': 'Stefano',
            'cognomemagistrato': 'Luciani',
            'tipointercettazione': 'C'}

xmldata = "<?xml version='1.0' encoding='UTF-8'?>\n" \
          '<dataroot xmlns:od="urn:schemas-microsoft-com:officedata" ' \
          'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' \
          'xsi:noNamespaceSchemaLocation="Intercettazioni.xsd"><Intercettazioni>' \
          '<ID>123</ID><Beneficiario>04578140875</Beneficiario>' \
          '<TipoPagamento>AC</TipoPagamento><EntePagante>F</EntePagante><NumeroFattura>E021</NumeroFattura>' \
          '<DataEmissioneProvv /><NumeroModello37 /><Registro>NOTI</Registro>' \
          '<DataFattura>2014-11-28T00:00:00</DataFattura><ImportoTotale>14480.00</ImportoTotale>' \
          '<ImportoIVA>3185.60</ImportoIVA><NR_RG>000001/2012</NR_RG><Sede>08500402104</Sede>' \
          '<DataInizioPrestazione>2014-07-31T00:00:00</DataInizioPrestazione>' \
          '<DataFinePrestazione>2014-10-20T00:00:00</DataFinePrestazione>' \
          '<CognomeMagistrato>Luciani</CognomeMagistrato><NomeMagistrato>Stefano</NomeMagistrato>' \
          '<TipoIntercettazione>C</TipoIntercettazione></Intercettazioni></dataroot>'


class SiammBadInputTest(unittest.TestCase):

    def testBadDate(self):
        """validate should fail with bad date"""
        errordata = testdata.copy()
        errordata ['datafattura'] = 'errore'
        self.assertRaises(siamm.ValidateException, siamm.validate, errordata)

    def testBadInteger(self):
        """validate should fail with bad integer"""
        errordata = testdata.copy()
        errordata ['importoiva'] = 'errore'
        self.assertRaises(siamm.ValidateException, siamm.validate, errordata)

    def testBadProtocollo(self):
        """validate should fail with bad protocollo"""
        errordata = testdata.copy()
        errordata ['numeromodello37'] = 'errore'
        self.assertRaises(siamm.ValidateException, siamm.validate, errordata)
        errordata = testdata.copy()
        errordata ['nr_rg'] = 'errore'
        self.assertRaises(siamm.ValidateException, siamm.validate, errordata)

    def testBadSerialization(self):
        """serialization should fail with bad data"""
        errordata = testdata.copy()
        errordata ['datafattura'] = 'errore'
        self.assertRaises(siamm.ValidateException, siamm.serialize, errordata)

    def testBadpiva(self):
        """piva should fail with bad data"""
        piva = siamm.piva('666666')
        self.assertEqual(False,piva)

    def testBadvalidateprot(self):
        """validateprot should fail with bad data"""
        prot = siamm.validateprot('666666')
        self.assertEqual(False,prot)
        prot = siamm.validateprot(None)
        self.assertEqual(False,prot)

    def testBadis_number(self):
        """is_number should fail with bad data"""
        numb = siamm.is_number('a')
        self.assertEqual(False,numb)

    def testBadTag(self):
        """serialization should fail with None data"""
        for t in rtag:
            errordata = testdata.copy()
            errordata[t] = None
            self.assertRaises(siamm.ValidateException, siamm.serialize, errordata)


class SiammInputTest(unittest.TestCase):

    def testSerialization(self):
        """validate serialization"""
        ser = siamm.serialize(testdata)
        self.assertIsInstance(ser, str)
        #: self.assertEqual(xmldata,ser)

    def testSerualizationList(self):
        serlist = [testdata,testdata,testdata]
        ser = siamm.serialize(serlist)
        self.assertIsInstance(ser, str)

    def testpiva(self):
        """piva should not fail"""
        piva = siamm.piva('IT04578140875')
        self.assertEqual(True,piva)

    def testvalidateprot(self):
        """validateprot should not fail"""
        prot = siamm.validateprot('124/2014')
        self.assertEqual(True,prot)

    def testvalidateprot2(self):
        """validateprot should fail"""
        prot = siamm.validateprot('124/14')
        self.assertEqual(False,prot)

    def testfillprot(self):
        """validateprot should not fail"""
        prot = siamm.fillprot('124/2014')
        self.assertEqual('000124/2014',prot)

    def testSerializationOptional(self):
        """validate serialization whit opts None"""
        errordata = testdata.copy()
        for t in otag:
            errordata.pop(t)
        ser = siamm.serialize(errordata)
        idint = True if ser.find('<ID>1</ID>') != -1 else False
        nrrg = True if (ser.find('<NR_RG/>') != -1  or ser.find('<NR_RG />') != -1) else False
        mod37 = True if (ser.find('<NUMEROMODELLO37 />') != -1 or ser.find('<NUMEROMODELLO37/>') != -1) else False
        self.assertEqual(True,idint)
        self.assertEqual(True,nrrg)
        self.assertEqual(True,mod37)
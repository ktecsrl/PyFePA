# coding=utf-8

import os

DPATH = os.path.dirname(os.path.abspath(__file__))

try:
    import lxml.etree as ElementTree
except ImportError:
    import xml.etree.ElementTree as ElementTree

import PyFePA.serializer as serializer
import PyFePA.siamm as siamm
import datetime

testdata = {'beneficiario': 'IT04578140875',
            'tipopagamento': 'AC',
            'id': 123,
            'entepagante': 'F',
            'numerofattura': 'E021',
            'registro': 'NOTI',
            'datafattura': datetime.datetime.strptime('2014-11-28T00:00:00', '%Y-%m-%dT%H:%M:%S'),
            'importototale': 14480.00,
            'importoiva': 3185.60,
            'nr_rg': '000001/2012',
            'sede': '08500402104',
            'numeromodello37': None,
            'datainizioprestazione': datetime.datetime.strptime('2014-07-31T00:00:00', '%Y-%m-%dT%H:%M:%S'),
            'datafineprestazione': datetime.datetime.strptime('2014-10-20T00:00:00', '%Y-%m-%dT%H:%M:%S'),
            'nomemagistrato': 'Stefanò'.decode('utf-8'),
            'cognomemagistrato': 'Luciani',
            'tipointercettazione': 'C'}

with open(DPATH+'/PyFePA/test/IT01234567890_11001.xml', 'rt') as f:
    tree = ElementTree.parse(f)
    fe = serializer.deserialize(element=tree)
    print serializer.serializer(fe,'xml')

testdata.pop('nr_rg')
print siamm.serialize(testdata)
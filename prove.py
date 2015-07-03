# coding=utf-8

import os

DPATH = os.path.dirname(os.path.abspath(__file__))

try:
    import lxml.etree as ElementTree
except ImportError:
    import xml.etree.ElementTree as ElementTree

tree = None

with open(DPATH+'/PyFePA/test/IT01234567890_11001.xml', 'rt') as f:
    tree = ElementTree.parse(f)

with open(DPATH+'/PyFePA/xsd/fatturapa_v1.1.xsd', 'rt') as f:
    xmlschema_doc = ElementTree.parse(f)
    xmlschema = ElementTree.XMLSchema(xmlschema_doc)
    if not xmlschema.validate(tree):
        print xmlschema.error_log

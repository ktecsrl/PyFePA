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

from PyFePA.fields import *
import PyFePA.fepa as fepa
import PyFePA.utils as utils
import os

DPATH = os.path.dirname(os.path.abspath(__file__))

lxml = False

try:
    import lxml.etree as ElementTree
    lxml = True
except ImportError:
    import xml.etree.ElementTree as ElementTree


class ValidateException(Exception):
    pass


def validate(invoice_part):

    taglist = {}
    for k, v in invoice_part.__class__.__dict__.items():
        if isinstance(v, FieldType):
            value = invoice_part.__getattribute__(k)
            if value:
                value = value if isinstance(v,FieldObject) or (isinstance(value,list) and v.multi) else v.tostring(value)
            if not (value or value == 0) and v.required and not v.conflict:
                raise ValidateException('Missing required value on {0}.{1}'.format(invoice_part.__class__.__name__, k))
            taglist[v.code] = {'tag': k, 'value': value, 'type': v.type, 'depend': v.depend,
                               'conflict': v.conflict, 'required': v.required}

    # Risolve Dipendenze e Conflitti
    for v in taglist.values():
        if v['value'] is not None and v['depend'] is not None:
            for d in v['depend']:
                if taglist[d]['value'] is None:
                    raise ValidateException('{0} Depend fail on codes {1}'.format(v['tag'],v['depend']))
        elif v['value'] is not None and v['conflict'] is not None:
            for d in v['conflict']:
                if taglist[d]['value'] is not None:
                    raise ValidateException('{0} Conflict whit {1}'.format(v['tag'],v['conflict']))
        elif v['value'] is None and v['conflict'] is not None and v['required']:
            for d in v['conflict']:
                if taglist[d]['value'] is None:
                    raise ValidateException('{0} or {1} mast be specify'.format(v['tag'],v['conflict']))

    return taglist


def globalvalidation(fattura):

    #: Non viene fatto nessun controllo sui dati ma solo controlli formali per garantire
    #: che i dati immessi siano conformi alla specifica. Ad esempio non viene controllata
    #: la quadratura della fattura o se i campi di testo hanno valori verosimili o meno.
    #: I controlli dovrebbero essere gli stessi che esegue SDI pertanto un file generato
    #: non dovrebbe essere scartato

    if fattura.FatturaElettronicaHeader.DatiTrasmissione.IdTrasmittente.IdPaese == 'IT' and \
            not utils.piva(fattura.FatturaElettronicaHeader.DatiTrasmissione.IdTrasmittente.IdCodice):
        raise ValidateException('00300 - PIVA SoggettoTrasmittente non valida')
    elif fattura.FatturaElettronicaHeader.CedentePrestatore.DatiAnagrafici.IdFiscaleIVA.IdCodice == 'IT' and \
            not utils.piva(fattura.CedentePrestatore.DatiAnagrafici.IdFiscaleIVA.IdCodice):
        raise ValidateException('00301 - PIVA CedentePrestatore non valida')
    elif fattura.FatturaElettronicaHeader.CedentePrestatore.DatiAnagrafici.IdFiscaleIVA is None and \
         fattura.FatturaElettronicaHeader.CedentePrestatore.DatiAnagrafici.Anagrafica.CodiceFiscale is None:
        raise ValidateException('00417 - CedentePrestatore almeno 1 tra IdFiscaleIVA e CodiceFiscale deve esistere')

    try:
        if fattura.FatturaElettronicaHeader.SoggettoEmittente == 'TZ' \
                and fattura.FatturaElettronicaHeader.TerzoIntermediarioOSoggettoEmittente is None:
            raise ValidateException('Dettagli Terzo Intermediario Necessari')
        for feb in fattura.FatturaElettronicaBody:
            if feb.DatiGenerali.DatiGeneraliDocumento.DatiRitenuta is not None:
                if feb.DatiGenerali.DatiGeneraliDocumento.DatiRitenuta.TipoRitenuta == 'RT01' \
                        and fattura.FatturaElettronicaHeader.CedentePrestatore.DatiAnagrafici.Anagrafica.Nome is None:
                    raise ValidateException('Nome e Cognome del Professionista Mancanti')
                if feb.DatiGenerali.DatiGeneraliDocumento.DatiRitenuta.TipoRitenuta == 'RT02' \
                        and fattura.FatturaElettronicaHeader.CedentePrestatore.DatiAnagrafici.Anagrafica.Denominazione is None:
                    raise ValidateException('Denominazione Azienda Mancante')
        for feb in fattura.FatturaElettronicaBody:
            if feb.DatiGenerali.DatiGeneraliDocumento.Data > datetime.date.today():
                print feb.DatiGenerali.DatiGeneraliDocumento.Data, '- TODAY -', datetime.date.today()
                raise ValidateException('00403 - Data Fattura non puo essere nel futuro')
            for ln in feb.DatiBeniServizi.DettaglioLinee:
                if ln.Ritenuta and not feb.DatiGenerali.DatiGeneraliDocumento.DatiRitenuta:
                    raise  ValidateException('00411 - Blocco Dati Ritenuta Mancante')
                elif (ln.AliquotaIVA is None or ln.AliquotaIVA == 0) and not ln.Natura:
                    raise ValidateException('00400 - Campo Natura mancante')
                elif (ln.AliquotaIVA or ln.AliquotaIVA != 0) and ln.Natura:
                    raise ValidateException('00401 - Campo Natura non deve essere presente')
    except AttributeError:
        raise ValidateException

    return True


def serializexml(invoice_part,tagname):

    taglist = validate(invoice_part)

    #: lxml and ElementTree support, different namespace definition
    #: try find better solution

    if tagname == 'FatturaElettronica' and lxml:
        NSMAP = {'ds': 'http://www.w3.org/2000/09/xmldsig#',
                 'p': 'http://www.fatturapa.gov.it/sdi/fatturapa/v1.1',
                 'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}
        fe = ElementTree.Element('{http://www.fatturapa.gov.it/sdi/fatturapa/v1.1}'+tagname, nsmap = NSMAP)
        fe.set('versione', '1.1')
    elif tagname == 'FatturaElettronica':
        fe = ElementTree.Element('p:'+tagname)
        fe.set('versione', '1.1')
        fe.set('xmlns:ds', 'http://www.w3.org/2000/09/xmldsig#')
        fe.set('xmlns:p', 'http://www.fatturapa.gov.it/sdi/fatturapa/v1.1')
        fe.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    else:
        fe = ElementTree.Element(tagname)

    for k in sorted(taglist):
        if isinstance(taglist[k]['value'], list):
            if taglist[k]['type'] == 'S':
                for t in taglist[k]['value']:
                    (ElementTree.SubElement(fe, taglist[k]['tag'])).text = t
            else:
                for t in taglist[k]['value']:
                    fe.append(serializexml(t, taglist[k]['tag']))
        elif taglist[k]['type'] == 'S' and taglist[k]['value'] is not None:
            (ElementTree.SubElement(fe, taglist[k]['tag'])).text = taglist[k]['value']
        elif taglist[k]['type'] == 'O' and taglist[k]['value'] is not None:
            fe.append(serializexml(taglist[k]['value'],taglist[k]['tag']))

    return fe


def serializer(obj,toformat,**kwargs):
    if toformat == 'xml':
        globalvalidation(obj)
        ser = serializexml(obj,'FatturaElettronica')
        if lxml:
            with open(DPATH+'/xsd/fatturapa_v1.2.xsd', 'rt') as f:
                xmlschema_doc = ElementTree.parse(f)
                xmlschema = ElementTree.XMLSchema(xmlschema_doc)
                if not xmlschema.validate(ser):
                    raise ValidateException('XSD validation Exception: '+str(xmlschema.error_log))

            return ElementTree.tostring(ser, xml_declaration=True, encoding='UTF-8', pretty_print=True)
        else:
            return ElementTree.tostring(ser, encoding='UTF-8')


def deserialize(**kwargs):

    if 'element' in kwargs:
        root = kwargs['element'].getroot()
        fe = fepa.FatturaElettronica()
        fe.from_element(root)
        return fe
    else:
        return None

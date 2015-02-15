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

from fields import *
from fepa import GenFePA

lxml = False

try:
    import lxml.etree as ElementTree
    lxml = True
except ImportError:
    import xml.etree.ElementTree as ElementTree


class NotificaScarto(GenFePA):
    IdentificativoSdI = FieldString()
    NomeFile = FieldString()
    DataOraRicezione = FieldDate()
    RiferimentoArchivio = FieldObject(object_class='RiferimentoArchivio')
    ListaErrori = FieldObject(object_class='ListaErrori')
    MessageId = FieldString()
    PecMessageId = FieldString()
    Note = FieldString()


class RiferimentoArchivio(GenFePA):
    IdentificativoSdI = FieldString()
    NomeFile = FieldString()


class ListaErrori(GenFePA):
    Errore = FieldObject(object_class='Errore')


class Errore(GenFePA):
    Codice = FieldInteger()
    Descrizione = FieldString()


class RicevutaConsegna(GenFePA):
    IdentificativoSdI = FieldString()
    NomeFile = FieldString()
    DataOraRicezione = FieldDate()
    DataOraConsegna = FieldDate
    Destinatario = FieldObject(object_class='Destinatario')
    MessageId = FieldString()
    Note = FieldString()


class Destinatario(GenFePA):
    Codice = FieldString()
    Descrizione = FieldString()


class NotificaMancataConsegna(GenFePA):
    IdentificativoSdI = FieldString()
    NomeFile = FieldString()
    DataOraRicezione = FieldDate()
    Descrizione = FieldString()
    MessageId = FieldString()
    Note = FieldString()

class MetadatiInvioFile(GenFePA):
    IdentificativoSdI = FieldString()
    NomeFile = FieldString()
    CodiceDestinatario = FieldString()
    Formato = FieldString()
    TentativiInvio = FieldInteger()
    MessageId = FieldString()
    Note = FieldString()


class NotificaEsitoCommittente(GenFePA):
    IdentificativoSdI = FieldString()
    RiferimentoFattura = FieldObject(object_class='RiferimentoFattura')
    Esito = FieldString()
    Descrizione = FieldString()
    MessageIdCommittente = FieldString()


class RiferimentoFattura(GenFePA):
    NumeroFattura = FieldString()
    AnnoFattura = FieldInteger()
    PosizioneFattura = FieldInteger()

class ScartoEsitoCommittente(GenFePA):
    IdentificativoSdI = FieldString()
    Scarto = FieldString()
    MessageId = FieldString()
    MessageIdCommittente = FieldString()
    Note = FieldString()

class NotificaEsito(GenFePA):
    IdentificativoSdI = FieldString()
    NomeFile = FieldString()
    EsitoCommittente = FieldObject(object_class='NotificaEsitoCommittente')
    MessageId = FieldString()
    Note = FieldString()


class NotificaDecorrenzaTermini(GenFePA):
    IdentificativoSdI = FieldString()
    NomeFile = FieldString()
    Descrizione = FieldString()
    MessageId = FieldString()
    Note = FieldString()


class AttestazioneTrasmissioneFattura(GenFePA):
    IdentificativoSdI = FieldString()
    NomeFile = FieldString()
    DataOraRicezione = FieldDate()
    Destinatario = FieldObject(object_class='Destinatario')
    MessageId = FieldString()
    Note = FieldString()
    HashFileOriginale = FieldString()

test = NotificaScarto()
test.DataOraRicezione = '2015-01-01'
test.IdentificativoSdI = '12334'

print test
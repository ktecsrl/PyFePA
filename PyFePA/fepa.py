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
import sys


#Static Values
RF = ('RF01', 'RF02', 'RF03', 'RF04', 'RF05', 'RF06', 'RF07', 'RF08', 'RF09', 'RF10',
      'RF11', 'RF12', 'RF13', 'RF14', 'RF15', 'RF16', 'RF17', 'RF18', 'RF19')
SU = ('SU', 'SM')
SL = ('LS', 'LN')
TD = map(lambda td: 'TD{:0=2d}'.format(td), range(1, 6))
TR = ['RT01','RT01']
TC = map(lambda tc: 'TC{:0=2d}'.format(tc), range(1,22))
NT = map(lambda nt: 'NT{:0=2d}'.format(nt), range(1,7))
TCP = ('SC', 'PR', 'AB', 'AC')
SM = ('SC', 'MG')
TP = ('TP01', 'TP02', 'TP03')
MP = map(lambda mp: 'MP{:0=2d}'.format(mp), range(1,22))
EI = ('I','D','S')


class GenFePA(object):

    def __setattr__(self,item,value):

        if value is None:
            return

        try:
            validator = self.__class__.__dict__[item]
            vval = validator.validate(value)
            if vval or vval == 0:
                super(GenFePA, self).__setattr__(item,vval)
            else:
                raise ValueError('Value {0} not allowed in {1}.{2}'.format(value,self.__class__,item))
        except KeyError:
            raise AttributeError('No attribute {0} on class {1}'.format(item,self.__class__))

    def __getattribute__(self, item):

        retval = super(GenFePA,self).__getattribute__(item)

        if isinstance(retval,FieldType):
            return None

        return retval

    def from_element(self, element):

        for k, v in self.__class__.__dict__.items():
            if isinstance(v,FieldType):
                tagg = [t for t in list(element) if str.lower(t.tag) == str.lower(k)]
                if len(tagg) == 1 or (v.multi and len(tagg) > 1):
                    current_module = sys.modules[__name__]
                    for t in tagg:
                        if isinstance(v, FieldObject):
                            c = getattr(current_module, v.object_class)()
                            c.from_element(t)
                            if v.multi and self.__getattribute__(k) is None:
                                self.__setattr__(k, [c])
                            elif v.multi:
                                self.__getattribute__(k).append(c)
                            else:
                                self.__setattr__(k, c)
                            element.remove(t)
                        else:
                            if v.multi and self.__getattribute__(k) is None:
                                self.__setattr__(k,[t.text])
                            elif v.multi:
                                self.__getattribute__(k).append(t.text)
                            else:
                                self.__setattr__(k, t.text)
                            element.remove(t)
                elif len(tagg) != 0:
                    raise ValueError()


class FatturaElettronica(GenFePA):

    FatturaElettronicaHeader = FieldObject(required=True,object_class='FatturaElettronicaHeader', code=1)
    FatturaElettronicaBody = FieldObject(required=True,object_class='FatturaElettronicaBody', multi=True, code=2)


class FatturaElettronicaHeader(GenFePA):

    DatiTrasmissione = FieldObject(required=True,object_class='DatiTrasmissione', code=1)
    CedentePrestatore = FieldObject(required=True,object_class='CedentePrestatore', code=2)
    RappresentanteFiscale = FieldObject(object_class='RappresentanteFiscale', code=3)
    CessionarioCommittente = FieldObject(required=True,object_class='CessionarioCommittente', code=4)
    TerzoIntermediarioOSoggettoEmittente = FieldObject(object_class='TerzoIntermediarioOSoggettoEmittente',
                                                       code=5, depend= [6])
    SoggettoEmittente = FieldCostant(cvalue=['CC','TZ'],code=6)


class DatiTrasmissione(GenFePA):

    IdTrasmittente = FieldObject(required=True,object_class='IdTrasmittente', code=1)
    ProgressivoInvio = FieldString(minlen=1,maxlen=10,required=True,code=2)
    FormatoTrasmissione = FieldCostant(cvalue=['FPA12','FPR12'],required=True,code=3)
    CodiceDestinatario = FieldString(minlen=6,maxlen=7,required=True,code=4)
    ContattiTrasmittente = FieldObject(object_class='ContattiTrasmittente', code=5)
    PECDestinatario = FieldString(minlen=7,maxlen=256,code=6)


class IdTrasmittente(GenFePA):

    IdPaese = FieldString(minlen=2,maxlen=2,required=True,code=1)
    IdCodice = FieldString(minlen=1,maxlen=28,required=True,code=2)


class ContattiTrasmittente(GenFePA):

    Telefono = FieldString(minlen=5,maxlen=12,code=1)
    Email = FieldString(minlen=7,maxlen=256,code=2)


class CedentePrestatore(GenFePA):

    DatiAnagrafici = FieldObject(required=True,object_class='DatiAnagraficiCP', code=1)
    Sede = FieldObject(required=True,object_class='Sede', code=2)
    StabileOrganizzazione = FieldObject(object_class='StabileOrganizzazione', code=3)
    IscrizioneREA = FieldObject(object_class='IscrizioneREA', code=4)
    Contatti = FieldObject(object_class='Contatti', code=5)
    RiferimentoAmministrazione = FieldString(minlen=1,maxlen=20,code=6)


class DatiAnagraficiRF(GenFePA):

    IdFiscaleIVA = FieldObject(required=True,object_class='IdFiscaleIVA', code=1)
    CodiceFiscale = FieldString(minlen=11, maxlen=16, code=2)
    Anagrafica = FieldObject(required=True, object_class='Anagrafica', code=3)

class DatiAnagraficiCC(GenFePA):

    IdFiscaleIVA = FieldObject(object_class='IdFiscaleIVA', code=1)
    CodiceFiscale = FieldString(minlen=11, maxlen=16, code=2)
    Anagrafica = FieldObject(required=True, object_class='Anagrafica', code=3)


class DatiAnagraficiCP(GenFePA):

    IdFiscaleIVA = FieldObject(required=True,object_class='IdFiscaleIVA', code=1)
    CodiceFiscale = FieldString(minlen=11, maxlen=16, code=2)
    Anagrafica = FieldObject(required=True, object_class='Anagrafica', code=3)
    AlboProfessionale = FieldString(minlen=1, maxlen=60, code=4, depend=[5,6,7])
    ProvinciaAlbo = FieldString(minlen=2, maxlen=2, code=5)
    NumeroIscrizioneAlbo = FieldString(minlen=1, maxlen=60, code=6)
    DataIscrizioneAlbo = FieldDate(code=7)
    RegimeFiscale = FieldCostant(cvalue=RF, required=True, code=8)


class IdFiscaleIVA(GenFePA):

    IdPaese = FieldString(minlen=2,maxlen=2,required=True,code=1)
    IdCodice = FieldString(minlen=1,maxlen=28,required=True,code=2)


class Anagrafica(GenFePA):

    Denominazione = FieldString(minlen=1,maxlen=80,code=1,required=True,conflict=[2,3])
    Nome = FieldString(minlen=1,maxlen=60,code=2,required=True,conflict=[1])
    Cognome = FieldString(minlen=1,maxlen=60,code=3,required=True,conflict=[1])
    Titolo = FieldString(minlen=2,maxlen=10,code=4)
    CodEORI = FieldString(minlen=1,maxlen=80,code=5)


class Sede(GenFePA):

    Indirizzo = FieldString(minlen=1,maxlen=60,required=True,code=1)
    NumeroCivico = FieldString(minlen=1,maxlen=8,code=2)
    CAP = FieldString(minlen=5,maxlen=5,required=True,code=3)
    Comune = FieldString(minlen=1,maxlen=60,required=True,code=4)
    Provincia = FieldString(minlen=2,maxlen=2,code=5)
    Nazione = FieldString(minlen=2,maxlen=2,required=True,code=6)


class StabileOrganizzazione(GenFePA):

    Indirizzo = FieldString(minlen=1,maxlen=60,required=True,code=1)
    NumeroCivico = FieldString(minlen=1,maxlen=8,code=2)
    CAP = FieldString(minlen=5,maxlen=5,required=True,code=3)
    Comune = FieldString(minlen=1,maxlen=60,required=True,code=4)
    Provincia = FieldString(minlen=2,maxlen=2,code=5)
    Nazione = FieldString(minlen=2,maxlen=2,required=True,code=6)


class IscrizioneREA(GenFePA):

    Ufficio = FieldString(minlen=2,maxlen=2,required=True,code=1)
    NumeroREA = FieldString(minlen=1,maxlen=20,required=True,code=2)
    CapitaleSociale = FieldDecimal(minlen=4,maxlen=16,code=3)
    SocioUnico = FieldCostant(cvalue=SU, code=4)
    StatoLiquidazione = FieldCostant(cvalue=SL, required=True, code=5)


class Contatti(GenFePA):

    Telefono = FieldString(minlen=5, maxlen=12, code=1)
    Fax = FieldString(minlen=5, maxlen=12, code=2)
    Email = FieldString(minlen=7, maxlen=256, code=3)


class RappresentanteFiscale(GenFePA):

    DatiAnagrafici = FieldObject(required=True, object_class='DatiAnagraficiRF', code=1)


class CessionarioCommittente(GenFePA):

    DatiAnagrafici = FieldObject(required=True, object_class='DatiAnagraficiCC', code=1)
    Sede = FieldObject(required=True, object_class='Sede', code=2)


class TerzoIntermediarioOSoggettoEmittente(GenFePA):

    DatiAnagrafici = FieldObject(required=True, object_class='DatiAnagraficiCC', code=1)


class FatturaElettronicaBody(GenFePA):

    DatiGenerali = FieldObject(required=True, object_class='DatiGenerali', code=1)
    DatiBeniServizi = FieldObject(required=True, object_class='DatiBeniServizi', code=2)
    DatiVeicoli = FieldObject(object_class='DatiVeicoli', code=3)
    DatiPagamento = FieldObject(object_class='DatiPagamento', multi=True, code=4)
    Allegati = FieldObject(object_class='Allegati', multi=True, code=5)


class DatiGenerali(GenFePA):

    DatiGeneraliDocumento = FieldObject(required=True, object_class='DatiGeneraliDocumento', code=1)
    DatiOrdineAcquisto = FieldObject(object_class='DatiOrdineAcquisto', multi=True, code=2)
    DatiContratto = FieldObject(object_class='DatiContratto', multi=True, code=3)
    DatiConvenzione = FieldObject(object_class='DatiConvenzione', multi=True, code=4)
    DatiRicezione = FieldObject(object_class='DatiRicezione', multi=True, code=5)
    DatiFattureCollegate = FieldObject(object_class='DatiFattureCollegate', code=6)
    DatiSAL = FieldObject(object_class='DatiSAL', multi=True, code=7)
    DatiDDT = FieldObject(object_class='DatiDDT', multi=True, code=8)
    DatiTrasporto = FieldObject(object_class='DatiTrasporto', code=9)
    FatturaPrincipale = FieldObject(object_class='FatturaPrincipale', code=10)


class DatiGeneraliDocumento(GenFePA):

    TipoDocumento = FieldCostant(cvalue=TD, required=True, code=1)
    Divisa = FieldString(minlen=3, maxlen=3,required=True, code=2)
    Data = FieldDate(required=True, code=3)
    Numero = FieldString(minlen=1, maxlen=20, required=True, code=4)
    DatiRitenuta = FieldObject(object_class='DatiRitenuta', code=5)
    DatiBollo = FieldObject(object_class='DatiBollo', code=6)
    DatiCassaPrevidenziale = FieldObject(object_class='DatiCassaPrevidenziale', multi=True, code=7)
    ScontoMaggiorazione = FieldObject(object_class='ScontoMaggiorazione', multi=True, code=8)
    ImportoTotaleDocumento = FieldDecimal(minlen=4, maxlen=16, code=9)
    Arrotondamento = FieldDecimal(minlen=4, maxlen=16, multi=True, code=10)
    Causale = FieldString(minlen=1, maxlen=200, code=11, multi=True)
    Art73 = FieldCostant(cvalue= ['SI'], code=12)


class DatiRitenuta(GenFePA):

    TipoRitenuta = FieldCostant(cvalue=TR, required=True, code=1)
    ImportoRitenuta = FieldDecimal(minlen=4, maxlen=16, code=2)
    AliquotaRitenuta = FieldDecimal(minlen=4, maxlen=6, code=3)
    CausalePagamento = FieldString(minlen=1, maxlen=1,required=True, code=4)


class DatiBollo(GenFePA):

    BolloVirtuale = FieldCostant(cvalue='SI', required=True, code=1)
    ImportoBollo = FieldDecimal(minlen=4, required=True, maxlen=15, code=2)


class DatiCassaPrevidenziale(GenFePA):

    TipoCassa = FieldCostant(cvalue=TC, required=True, code=1)
    AlCassa = FieldDecimal(minlen=4, maxlen=6, required=True, code=2)
    ImportoContributoCassa = FieldDecimal(minlen=4, maxlen=16, required=True, code=3)
    ImponibileCassa = FieldDecimal(minlen=4, maxlen=15, code=4)
    AliquotaIVA = FieldDecimal(minlen=4, maxlen=6, required=True, code=5)
    Ritenuta = FieldCostant(cvalue= ['SI'], code=6)
    Natura = FieldCostant(cvalue=NT, code=7)
    RiferimentoAmministrazione = FieldString(minlen=1, maxlen=20, code=8)


class DatiOrdineAcquisto(GenFePA):

    RiferimentoNumeroLinea = FieldInteger(minlen=1, maxlen=4, code=1)
    IdDocumento = FieldString(minlen=1, maxlen=20, required=True, code=2)
    Data = FieldDate(code=3)
    NumItem = FieldString(minlen=1, maxlen=20, code=4)
    CodiceCommessaConvenzione = FieldString(minlen=1, maxlen=100, code=5)
    CodiceCUP = FieldString(minlen=1, maxlen=15, code=6)
    CodiceCIG = FieldString(minlen=1, maxlen=15, code=7)


class DatiContratto(GenFePA):

    IdDocumento = FieldString(minlen=1, maxlen=20, required=True, code=1)
    RiferimentoNumeroLinea = FieldInteger(minlen=1, maxlen=4, code=2)
    Data = FieldDate(code=3)
    NumItem = FieldString(minlen=1, maxlen=20, code=4)
    CodiceCommessaConvenzione = FieldString(minlen=1, maxlen=100, code=5)
    CodiceCUP = FieldString(minlen=1, maxlen=15, code=6)
    CodiceCIG = FieldString(minlen=1, maxlen=15, code=7)


class DatiConvenzione(GenFePA):

    IdDocumento = FieldString(minlen=1, maxlen=20, required=True, code=1)
    RiferimentoNumeroLinea = FieldInteger(minlen=1, maxlen=4, code=2)
    Data = FieldDate(code=3)
    NumItem = FieldString(minlen=1, maxlen=20, code=4)
    CodiceCommessaConvenzione = FieldString(minlen=1, maxlen=100, code=5)
    CodiceCUP = FieldString(minlen=1, maxlen=15, code=6)
    CodiceCIG = FieldString(minlen=1, maxlen=15, code=7)


class DatiRicezione(GenFePA):

    IdDocumento = FieldString(minlen=1, maxlen=20, required=True, code=1)
    RiferimentoNumeroLinea = FieldInteger(minlen=1, maxlen=4, code=2)
    Data = FieldDate(code=3)
    NumItem = FieldString(minlen=1, maxlen=20, code=4)
    CodiceCommessaConvenzione = FieldString(minlen=1, maxlen=100, code=5)
    CodiceCUP = FieldString(minlen=1, maxlen=15, code=6)
    CodiceCIG = FieldString(minlen=1, maxlen=15, code=7)


class DatiFattureCollegate(GenFePA):

    IdDocumento = FieldString(minlen=1, maxlen=20, required=True, code=1)
    RiferimentoNumeroLinea = FieldInteger(minlen=1, maxlen=4, code=2)
    Data = FieldDate(code=3)
    NumItem = FieldString(minlen=1, maxlen=20, code=4)
    CodiceCommessaConvenzione = FieldString(minlen=1, maxlen=100, code=5)
    CodiceCUP = FieldString(minlen=1, maxlen=15, code=6)
    CodiceCIG = FieldString(minlen=1, maxlen=15, code=7)


class DatiSAL(GenFePA):

    RiferimentoFase = FieldString(minlen=1, maxlen=20, required=True, code=1)


class DatiDDT(GenFePA):

    NumeroDDT = FieldString(minlen=1, maxlen=20, required=True, code=1)
    DataDDT = FieldDate(required=True, code=2)
    RiferimentoNumeroLinea = FieldInteger(minlen=1,maxlen=4, code=3)


class DatiTrasporto(GenFePA):

    DatiAnagraficiVettore = FieldObject(required=True,object_class='DatiAnagraficiVettore', code=1)
    MezzoTrasporto = FieldString(minlen=11, maxlen=80, code=2)
    CausaleTrasporto = FieldString(minlen=11, maxlen=100, code=3)
    NumeroColli = FieldInteger(minlen=1,maxlen=4, code= 4)
    Descrizione = FieldString(minlen=11, maxlen=100, code=5)
    UnitaMisuraPeso = FieldString(minlen=11, maxlen=10, code=6)
    PesoLordo = FieldDecimal(minlen=4, maxlen=7, code=7)
    PesoNetto = FieldDecimal(minlen=4, maxlen=7, code=8)
    DataOraRitiro = FieldDate(code=9)
    DataInizioTrasporto = FieldDateTime(code=10)
    TipoResa = FieldString(minlen=3, maxlen=3, code=11)
    IndirizzoResa = FieldObject(object_class='IndirizzoResa', code=12)
    DataOraConsegna = FieldDateTime(code=13)


class DatiAnagraficiVettore(GenFePA):

    IdFiscaleIVA = FieldObject(required=True,object_class='IdFiscaleIVA', code=1)
    CodiceFiscale = FieldString(minlen=11, maxlen=16, code=2)
    Anagrafica = FieldObject(required=True, object_class='Anagrafica', code=3)
    NumeroLicenzaGuida = FieldString(minlen=1, maxlen=20, code=4)


class IndirizzoResa(GenFePA):

    Indirizzo = FieldString(minlen=1,maxlen=60,required=True,code=1)
    NumeroCivico = FieldString(minlen=1,maxlen=8,code=2)
    CAP = FieldString(minlen=5,maxlen=5,required=True,code=3)
    Comune = FieldString(minlen=1,maxlen=60,required=True,code=4)
    Provincia = FieldString(minlen=2,maxlen=2,code=5)
    Nazione = FieldString(minlen=2,maxlen=2,required=True,code=6)


class FatturaPrincipale(GenFePA):

    NumeroFatturaPrincipale = FieldString(minlen=1,maxlen=20,required=True,code=1)
    DataFatturaPrincipale = FieldDate(required=True, code=2)


class DatiBeniServizi(GenFePA):

    DettaglioLinee = FieldObject(object_class='DettaglioLinee', required=True, multi=True, code=1)
    DatiRiepilogo = FieldObject(object_class='DatiRiepilogo', required=True, multi=True, code=2)


class DettaglioLinee(GenFePA):

    NumeroLinea = FieldInteger(minlen=1, maxlen=4, required=True, code=1)
    TipoCessionePrestazione = FieldCostant(cvalue=TCP, code=2)
    CodiceArticolo = FieldObject(object_class='CodiceArticolo', code=3)
    Descrizione = FieldString(minlen=1, maxlen=1000, required=True, code=4)
    Quantita = FieldDecimal(minlen=4, maxlen=21, code=5)
    UnitaMisura = FieldString(minlen=1, maxlen=10, code=6)
    DataInizioPeriodo = FieldDate(code=7)
    DataFinePeriodo = FieldDate(code=8)
    PrezzoUnitario = FieldDecimal(minlen=4, maxlen=21, required=True, code=9)
    ScontoMaggiorazione = FieldObject(object_class='ScontoMaggiorazione', multi=True, code=10)
    PrezzoTotale = FieldDecimal(minlen=4, maxlen=21, required=True, code=11)
    AliquotaIVA = FieldDecimal(minlen=4, maxlen=6, required=True, code=12)
    Ritenuta = FieldCostant(cvalue=['SI'], code=13)
    Natura = FieldCostant(cvalue=NT, code=14)
    RiferimentoAmministrazione = FieldString(minlen=1, maxlen=20, code=15)
    AltriDatiGestionali = FieldObject(object_class='AltriDatiGestionali', multi=True, code=16)


class CodiceArticolo(GenFePA):

    CodiceTipo = FieldString(minlen=1, maxlen=35, required=True, code=1)
    CodiceValore = FieldString(minlen=1, maxlen=35,required=True, code=2)


class ScontoMaggiorazione(GenFePA):

    Tipo = FieldCostant(cvalue=SM, required=True, code=1)
    Percentuale = FieldDecimal(minlen=4, maxlen=6, code=2)
    Importo = FieldDecimal(minlen=4, maxlen=16, code=3)

class AltriDatiGestionali(GenFePA):

    TipoDato = FieldString(minlen=1, maxlen=10, required=True, code=1)
    RiferimentoTesto = FieldString(minlen=1, maxlen=60, code=2)
    RiferimentoNumero = FieldDecimal(minlen=4, maxlen=21, code=3)
    RiferimentoData = FieldDate(code=4)


class DatiRiepilogo(GenFePA):

    AliquotaIVA = FieldDecimal(minlen=4, maxlen=6, required=True, code=1)
    Natura = FieldCostant(cvalue=NT, code=2)
    SpeseAccessorie = FieldDecimal(minlen=4, maxlen=15, code=3)
    Arrotondamento = FieldDecimal(minlen=4, maxlen=21, code=4)
    ImponibileImporto = FieldDecimal(minlen=4, maxlen=15, required=True, code=5)
    Imposta = FieldDecimal(minlen=4, maxlen=15, required=True, code=6)
    EsigibilitaIVA = FieldCostant(cvalue=EI, code=7)
    RiferimentoNormativo = FieldString(minlen=1, maxlen=100, code=8)


class DatiVeicoli(GenFePA):

    Data = FieldDate(required=True, code=1)
    TotalePercorso = FieldString(minlen=1, maxlen=15, required=True, code=2)


class DatiPagamento(GenFePA):

    CondizioniPagamento = FieldCostant(cvalue=TP, required=True, code=1)
    DettaglioPagamento = FieldObject(object_class='DettaglioPagamento', required=True, multi=True, code=2)


class DettaglioPagamento(GenFePA):

    Beneficiario = FieldString(minlen=1, maxlen=200, code=1)
    ModalitaPagamento = FieldCostant(cvalue=MP, required=True, code=2)
    DataRiferimentoTerminiPagamento = FieldDate(code=3)
    GiorniTerminiPagamento = FieldInteger(minlen=1, maxlen=3, code=4)
    DataScadenzaPagamento = FieldDate(code=5)
    ImportoPagamento = FieldDecimal(minlen=4, maxlen=16, required=True, code=6)
    CodUfficioPostale = FieldString(minlen=1, maxlen=20, code=7)
    CognomeQuietanzante = FieldString(minlen=1, maxlen=60, code=8)
    NomeQuietanzante = FieldString(minlen=1, maxlen=60, code=9)
    CFQuietanzante = FieldString(minlen=1, maxlen=16, code=10)
    TitoloQuietanzante = FieldString(minlen=2, maxlen=10, code=11)
    IstitutoFinanziario = FieldString(minlen=1, maxlen=80, code=12)
    IBAN = FieldString(minlen=15, maxlen=34, code=13)
    ABI = FieldString(minlen=5, maxlen=5, code=14)
    CAB = FieldString(minlen=5, maxlen=5, code=15)
    BIC = FieldString(minlen=8, maxlen=11, code=16)
    ScontoPagamentoAnticipato = FieldDecimal(minlen=4, maxlen=15, code=17)
    DataLimitePagamentoAnticipato = FieldDate(code=18)
    PenalitaPagamentiRitardati = FieldDecimal(minlen=4, maxlen=15, code=19)
    DataDecorrenzaPenale = FieldDate(code=20)
    CodicePagamento = FieldString(minlen=2, maxlen=15, code=21)


class Allegati(GenFePA):

    NomeAttachment = FieldString(minlen=1, maxlen=60, required=True, code=1)
    AlgoritmoCompressione = FieldString(minlen=1, maxlen=10, code=2)
    FormatoAttachment = FieldString(minlen=1, maxlen=10, code=3)
    DescrizioneAttachment = FieldString(minlen=1, maxlen=100, code=4)
    Attachment = FieldString(minlen=1, required=True, code=5)
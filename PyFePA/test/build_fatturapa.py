from PyFePA.fepa import *
from PyFePA.serializer import serializer
from PyFePA.serializer import ValidateException

class FatturaPA(object):

    def get_fatturapa(self):

        fatturapa = FatturaElettronica()
        fatturapa.FatturaElettronicaHeader = self.header()
        fatturapa.FatturaElettronicaBody = self.body()

        return fatturapa

    def header(self):

        header = FatturaElettronicaHeader()
        header.DatiTrasmissione = self.trasmissione()
        header.CedentePrestatore = self.cedenteprestatore()
        header.CessionarioCommittente = self.cessionariocommittente()
        header.TerzoIntermediarioOSoggettoEmittente = self.terzointermediario()
        header.SoggettoEmittente = 'TZ'

        return header

    def body(self):

        bodys = []

        body = FatturaElettronicaBody()
        body.DatiGenerali = self.datigenerali()
        body.DatiBeniServizi = self.datibeniservizi()
        body.DatiPagamento = self.datipagamento()
        body.Allegati = self.allegati()
        bodys.append(body)

        return bodys

    def trasmissione(self):

        dt = DatiTrasmissione()

        dt.IdTrasmittente = IdTrasmittente()
        dt.IdTrasmittente.IdPaese = 'IT'
        dt.IdTrasmittente.IdCodice = '04200640870'
        dt.ProgressivoInvio = '12345'
        dt.CodiceDestinatario = 'TSTIPA'

        dt.ContattiTrasmittente = ContattiTrasmittente()
        dt.ContattiTrasmittente.Email = 'info@ktec.it'
        dt.ContattiTrasmittente.Telefono = '095-8998479'

        return dt

    def cedenteprestatore(self):

        cp = CedentePrestatore()

        cp.DatiAnagrafici = DatiAnagraficiCP()
        cp.DatiAnagrafici.IdFiscaleIVA = IdFiscaleIVA()
        cp.DatiAnagrafici.IdFiscaleIVA.IdPaese = 'IT'
        cp.DatiAnagrafici.IdFiscaleIVA.IdCodice = '04200640870'
        #cp.DatiAnagrafici.CodiceFiscale = None
        cp.DatiAnagrafici.Anagrafica = Anagrafica()
        cp.DatiAnagrafici.Anagrafica.Denominazione = 'KTec S.r.l.'
        #cp.DatiAnagrafici.Anagrafica.Nome = None
        #cp.DatiAnagrafici.Anagrafica.Cognome = None
        #cp.DatiAnagrafici.Anagrafica.Titolo = None
        #cp.DatiAnagrafici.Anagrafica.CodEORI = None
        cp.DatiAnagrafici.RegimeFiscale = 'RF01'
        cp.Sede = Sede()
        cp.Sede.Indirizzo = 'Corso Martiri della Liberta, 38'
        #cp.Sede.NumeroCivico = None
        cp.Sede.CAP = '95131'
        cp.Sede.Comune = 'Catania'
        cp.Sede.Provincia = 'CT'
        cp.Sede.Nazione = 'IT'
        cp.IscrizioneREA = IscrizioneREA()
        cp.IscrizioneREA.Ufficio = 'CT'
        cp.IscrizioneREA.NumeroREA = '279831'
        cp.IscrizioneREA.CapitaleSociale = 10000
        cp.IscrizioneREA.SocioUnico = 'SM'
        cp.IscrizioneREA.StatoLiquidazione = 'LN'
        cp.Contatti = Contatti()
        cp.Contatti.Telefono = '095-8998479'
        cp.Contatti.Email = 'info@ktec.it'
        cp.Contatti.Fax = '095-8992092'

        return cp

    def cessionariocommittente(self):

        cc = CessionarioCommittente()
        cc.DatiAnagrafici = DatiAnagraficiCC()
        #cc.DatiAnagrafici.IdFiscaleIVA = IdFiscaleIVA()
        #cc.DatiAnagrafici.IdFiscaleIVA.IdPaese = None
        #cc.DatiAnagrafici.IdFiscaleIVA.IdCodice = None
        cc.DatiAnagrafici.CodiceFiscale = '12345678901'
        cc.DatiAnagrafici.Anagrafica = Anagrafica()
        cc.DatiAnagrafici.Anagrafica.Denominazione = 'Amministrazione di Prova'
        #cc.DatiAnagrafici.Anagrafica.Nome = None
        #cc.DatiAnagrafici.Anagrafica.Cognome = None
        #cc.DatiAnagrafici.Anagrafica.Titolo = None
        #cc.DatiAnagrafici.Anagrafica.CodEORI = None
        cc.Sede = Sede()
        cc.Sede.Indirizzo = 'Via Tal dei Tali'
        #cc.Sede.NumeroCivico = None
        cc.Sede.CAP = '12345'
        cc.Sede.Comune = 'Di Fantasia'
        cc.Sede.Provincia = 'FL'
        cc.Sede.Nazione = 'FF'

        return cc

    def terzointermediario(self):

        tz = TerzoIntermediarioOSoggettoEmittente()
        tz.DatiAnagrafici = DatiAnagraficiCC()
        tz.DatiAnagrafici.IdFiscaleIVA = IdFiscaleIVA()
        tz.DatiAnagrafici.IdFiscaleIVA.IdPaese = 'IT'
        tz.DatiAnagrafici.IdFiscaleIVA.IdCodice = '04200640870'
        #tz.DatiAnagrafici.CodiceFiscale = '04200640870'
        tz.DatiAnagrafici.Anagrafica = Anagrafica()
        tz.DatiAnagrafici.Anagrafica.Denominazione = 'KTec S.r.l.'
        #tz.DatiAnagrafici.Anagrafica.Nome = None
        #tz.DatiAnagrafici.Anagrafica.Cognome = None
        #tz.DatiAnagrafici.Anagrafica.Titolo = None
        #tz.DatiAnagrafici.Anagrafica.CodEORI = None

        return tz

    def datigenerali(self):

        dg = DatiGenerali()
        dg.DatiGeneraliDocumento = DatiGeneraliDocumento()
        dg.DatiGeneraliDocumento.TipoDocumento = 'TD01'
        dg.DatiGeneraliDocumento.Divisa = 'EUR'
        dg.DatiGeneraliDocumento.Data = '2015-01-01'
        dg.DatiGeneraliDocumento.Numero = 'FAT/2014/00001'
        #dg.DatiGeneraliDocumento.ScontoMaggiorazione = ScontoMaggiorazione()
        #dg.DatiGeneraliDocumento.ScontoMaggiorazione.Tipo = None
        #dg.DatiGeneraliDocumento.ScontoMaggiorazione.Percentuale = None
        #dg.DatiGeneraliDocumento.ScontoMaggiorazione.Importo = None
        dg.DatiGeneraliDocumento.ImportoTotaleDocumento = 1220000
        #dg.DatiGeneraliDocumento.Arrotondamento = None
        dg.DatiGeneraliDocumento.Causale = ['Test PyFePA','Pippo']

        return dg

    def datibeniservizi(self):

        dbs = DatiBeniServizi()

        linee = []

        linea_nu = 1


        dtl = DettaglioLinee()
        dtl.NumeroLinea = linea_nu
        dtl.CodiceArticolo = CodiceArticolo()
        dtl.CodiceArticolo.CodiceTipo = 'INTERNO'
        dtl.CodiceArticolo.CodiceValore = '12345'
        dtl.Descrizione = 'Articolo di test PyFePA'
        dtl.Quantita = 1
        dtl.UnitaMisura = 'Unit(s)'
        dtl.PrezzoUnitario = 2000000
        dtl.ScontoMaggiorazione = ScontoMaggiorazione()
        dtl.ScontoMaggiorazione.Tipo = 'SC'
        dtl.ScontoMaggiorazione.Percentuale = 50

        dtl.PrezzoTotale = 1000000
        dtl.AliquotaIVA = 22
        linea_nu += 1
        linee.append(dtl)

        dbs.DettaglioLinee = linee

        dr = []

        drt = DatiRiepilogo()
        drt.AliquotaIVA = 22
        drt.ImponibileImporto = 1000000
        drt.Imposta = 220000
        drt.EsigibilitaIVA = 'S'
        drt.RiferimentoNormativo = 'Scissione nei pagamenti, IVA versata dal committente art 17 ter  D.P.R. n.633/ 72'
        dr.append(drt)

        dbs.DatiRiepilogo = dr

        return dbs

    def datipagamento(self):


        dp = DatiPagamento()
        dp.CondizioniPagamento = 'TP02'
        dp.DettaglioPagamento = DettaglioPagamento()
        dp.DettaglioPagamento.ModalitaPagamento = 'MP05'
        dp.DettaglioPagamento.ImportoPagamento = 1220000
        dp.DettaglioPagamento.IBAN = '12A 4567 890234 51234567 890236'
        dp.DettaglioPagamento.BIC = '12345678'

        return dp

    def allegati(self):


        allegati = []


        all = Allegati()
        all.NomeAttachment = 'Test'
        all.FormatoAttachment = 'XML'
        all.DescrizioneAttachment = 'Allegato di Test'
        all.Attachment = 'PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KCjxkYXRhcm9vdCB4bWxuczpvZD0idXJuOnNjaGVtYXMtbWljcm9zb2Z0LWNvbTpvZmZpY2VkYXRhIiAKCQkgIHhtbG5zOnhzaT0iaHR0cDovL3d3dy53My5vcmcvMjAwMS9YTUxTY2hlbWEtaW5zdGFuY2UiIAoJCSAgeHNpOm5vTmFtZXNwYWNlU2NoZW1hTG9jYXRpb249IkludGVyY2V0dGF6aW9uaS54c2QiIGdlbmVyYXRlZD0iMjAxMC0wMy0zMFQxMDo0MjoyMSI'
        allegati.append(all)

        return allegati

if __name__ == "__main__":
    fatturapa = FatturaPA()
    fpa = fatturapa.get_fatturapa()
    print serializer(fpa,'xml')
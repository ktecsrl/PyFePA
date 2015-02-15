from PyFePA.fepa import *

class OdooFatturaPA(object):

    def from_odoo(self):

        fatturapa = FatturaElettronica()
        fatturapa.FatturaElettronicaHeader = self.header_from_odoo()
        fatturapa.FatturaElettronicaBody = FatturaElettronicaBody()

    def header_from_odoo(self):

        header = FatturaElettronicaHeader()
        header.DatiTrasmissione = self.trasmissione_from_odoo()
        header.CedentePrestatore = self.cedenteprestatore_from_odoo()
        header.CessionarioCommittente = self.cessionariocommittente_from_odoo()
        header.TerzoIntermediarioOSoggettoEmittente = self.terzointermediario_from_odoo()
        #header.SoggettoEmittente = None

        return header

    def body_from_odoo(self):

        body = FatturaElettronicaBody()
        body.DatiGenerali = self.datigenerali_from_odoo()
        body.DatiBeniServizi = self.datibeniservizi_from_odoo()
        body.DatiPagamento = self.datipagamento_from_odoo()
        body.Allegati = self.allegati_from_odoo()

        return body

    def trasmissione_from_odoo(self, invoice):

        dt = DatiTrasmissione()
        dt.IdTrasmittente = IdTrasmittente()

        company = invoice.company_id

        if not company:
            user_obj = self.pool['res.users']
            company = user_obj.company_id

        dt.IdTrasmittente.IdPaese = company.vat[0:2]
        dt.IdTrasmittente.IdCodice = company.vat[2:]
        dt.ProgressivoInvio = None
        dt.CodiceDestinatario = invoice.partner_id.ipa_code

        if company.phone or company.email:
            dt.ContattiTrasmittente = ContattiTrasmittente()
            dt.ContattiTrasmittente.ContattiTrasmittente.Email = company.email
            dt.ContattiTrasmittente.Telefono = company.phone

        return dt

    def cedenteprestatore_from_odoo(self, invoice):

        company = invoice.company_id

        if not company:
            user_obj = self.pool['res.users']
            company = user_obj.company_id

        cp = CedentePrestatore()
        cp.DatiAnagrafici = DatiAnagraficiCP()
        cp.DatiAnagrafici.IdFiscaleIVA = IdFiscaleIVA()
        cp.DatiAnagrafici.IdFiscaleIVA.IdPaese = company.vat[0:2]
        cp.DatiAnagrafici.IdFiscaleIVA.IdCodice = company.vat[2:]
        #cp.DatiAnagrafici.CodiceFiscale = None
        cp.DatiAnagrafici.Anagrafica = Anagrafica()
        cp.DatiAnagrafici.Anagrafica.Denominazione = company.name
        #cp.DatiAnagrafici.Anagrafica.Nome = None
        #cp.DatiAnagrafici.Anagrafica.Cognome = None
        #cp.DatiAnagrafici.Anagrafica.Titolo = None
        #cp.DatiAnagrafici.Anagrafica.CodEORI = None
        cp.DatiAnagrafici.RegimeFiscale = company.regime_fiscale
        cp.Sede = Sede()
        cp.Sede.Indirizzo = company.street + company.street2
        #cp.Sede.NumeroCivico = None
        cp.Sede.CAP = company.zip
        cp.Sede.Comune = company.city
        cp.Sede.Provincia = company.state_id.code
        cp.Sede.Nazione = company.country_id.code
        cp.IscrizioneREA = IscrizioneREA()
        cp.IscrizioneREA.Ufficio = company.company_registry[0:2]
        cp.IscrizioneREA.NumeroREA = company.company_registry[2:]
        cp.IscrizioneREA.CapitaleSociale = company.capitale_sociale
        cp.IscrizioneREA.SocioUnico = company.socio_unico
        cp.IscrizioneREA.StatoLiquidazione = company.stato_liquidazione
        cp.Contatti = Contatti()
        cp.Contatti.Telefono = company.phone
        cp.Contatti.Email = company.fax
        cp.Contatti.Fax = company.email

        return cp

    def cessionariocommittente_from_odoo(self, invoice):

        cc = CessionarioCommittente()
        cc.DatiAnagrafici = DatiAnagraficiCC()
        #cc.DatiAnagrafici.IdFiscaleIVA = IdFiscaleIVA()
        #cc.DatiAnagrafici.IdFiscaleIVA.IdPaese = None
        #cc.DatiAnagrafici.IdFiscaleIVA.IdCodice = None
        cc.DatiAnagrafici.CodiceFiscale = invoice.partner_id.fiscalcode
        cc.DatiAnagrafici.Anagrafica = Anagrafica()
        cc.DatiAnagrafici.Anagrafica.Denominazione = invoice.partner_id.name
        #cc.DatiAnagrafici.Anagrafica.Nome = None
        #cc.DatiAnagrafici.Anagrafica.Cognome = None
        #cc.DatiAnagrafici.Anagrafica.Titolo = None
        #cc.DatiAnagrafici.Anagrafica.CodEORI = None
        cc.Sede = Sede()
        cc.Sede.Indirizzo = invoice.partner_id.street
        #cc.Sede.NumeroCivico = None
        cc.Sede.CAP = invoice.partner_id.zip
        cc.Sede.Comune = invoice.partner_id.city
        #cc.Sede.Provincia = None
        cc.Sede.Nazione = invoice.partner_id.coutry_id.code

        return cc

    def terzointermediario_from_odoo(self):

        tz = TerzoIntermediarioOSoggettoEmittente()
        tz.DatiAnagrafici = DatiAnagraficiCC()
        tz.DatiAnagrafici.IdFiscaleIVA = IdFiscaleIVA()
        tz.DatiAnagrafici.IdFiscaleIVA.IdPaese = None
        tz.DatiAnagrafici.IdFiscaleIVA.IdCodice = None
        tz.DatiAnagrafici.CodiceFiscale = None
        tz.DatiAnagrafici.Anagrafica = Anagrafica()
        tz.DatiAnagrafici.Anagrafica.Denominazione = None
        tz.DatiAnagrafici.Anagrafica.Nome = None
        tz.DatiAnagrafici.Anagrafica.Cognome = None
        tz.DatiAnagrafici.Anagrafica.Titolo = None
        tz.DatiAnagrafici.Anagrafica.CodEORI = None

        return tz

    def datigenerali_from_odoo(self, invoice):

        dg = DatiGenerali()
        dg.DatiGeneraliDocumento = DatiGeneraliDocumento()
        dg.DatiGeneraliDocumento.TipoDocumento = 'TD01'
        dg.DatiGeneraliDocumento.Divisa = invoice.currency_id.name
        dg.DatiGeneraliDocumento.Data = invoice.date_invoice
        dg.DatiGeneraliDocumento.Numero = invoice.number
        #dg.DatiGeneraliDocumento.ScontoMaggiorazione = ScontoMaggiorazione()
        #dg.DatiGeneraliDocumento.ScontoMaggiorazione.Tipo = None
        #dg.DatiGeneraliDocumento.ScontoMaggiorazione.Percentuale = None
        #dg.DatiGeneraliDocumento.ScontoMaggiorazione.Importo = None
        dg.DatiGeneraliDocumento.ImportoTotaleDocumento = invoice.amount_total
        #dg.DatiGeneraliDocumento.Arrotondamento = None
        if hasattr(invoice, 'siamm_intercettazioni'):
            dg.DatiGeneraliDocumento.Causale = 'PM: {0} {1} - NR-RG: {2} - Servizio dal {3} al {4} - {5}'.format(
                invoice.siamm_nomemagistrato,
                invoice.siamm_cognomemagistrato,
                invoice.siamm_nrrg,
                invoice.siamm_datainizioprestazione,
                invoice.siamm_datafineprestazione,
                invoice.comment
            )
        else:
            dg.DatiGeneraliDocumento.Causale = invoice.comment

        return dg

    def datibeniservizi_from_odoo(self, invoice):

        dbs = DatiBeniServizi()

        linee = []

        linea_nu = 1

        for line in invoice.invoice_line:

            dtl = DettaglioLinee()
            dtl.NumeroLinea = linea_nu
            if line.product_id.code:
                dtl.CodiceArticolo = CodiceArticolo()
                dtl.CodiceArticolo.CodiceTipo = 'INTERNO'
                dtl.CodiceArticolo.CodiceValore = line.product_id.code
            dtl.Descrizione = line.name
            dtl.Quantita = line.quantity
            dtl.UnitaMisura = line.uos_id.name
            dtl.PrezzoUnitario = line.price_unit

            if line.discount:
                dtl.ScontoMaggiorazione = ScontoMaggiorazione()
                dtl.ScontoMaggiorazione.Tipo = 'SC'
                dtl.ScontoMaggiorazione.Percentuale = line.discount

            dtl.PrezzoTotale = line.price_subtotal
            #To-Do: Tasse multiple sulla stessa linea vedere come risolvere eventuale errore
            dtl.AliquotaIVA = line.invoice_line_tax_id[0].amount*100
            linea_nu += 1
            linee.append(dtl)

        dr = []
        for tl in invoice.tax_line:
            drt = DatiRiepilogo()
            #To-Do: questo e' sbagliato
            drt.AliquotaIVA = tl.tax_amount*100
            drt.ImponibileImporto = tl.base
            dbs.DatiRiepilogo.Imposta = tl.amount
            #To-Do: sistemare esigibilita iva
            dbs.DatiRiepilogo.EsigibilitaIVA = 'D'
            dr.append(drt)

        dbs.DatiRiepilogo = dr

        return dbs

    def datipagamento_from_odoo(self, invoice):

        company = invoice.company_id

        if not company:
            user_obj = self.pool['res.users']
            company = user_obj.company_id

        bank = invoice.partner_bank_id

        if not bank:
            bank = company.bank_ids[0]

        dp = DatiPagamento()
        #to-do: implementare esterno
        dp.CondizioniPagamento = 'TP02'
        dp.DettaglioPagamento = DettaglioPagamento()
        dp.DettaglioPagamento.ImportoPagamento = invoice.amount_total
        dp.DettaglioPagamento.IBAN = bank.iban
        dp.DettaglioPagamento.BIC = bank.bank_bic

        return dp

    def allegati_from_odoo(self, invoice):

        attachments = self.env['ir.attachment'].search([('res_model', '=', 'account.invoice'),
                                                        ('res_id', '=', invoice.id)])
        allegati = []

        for f in attachments:
            if f.datas_fname[0:5] == 'FEPA_':
                all = Allegati()
                all.NomeAttachment = f.datas_fname
                all.FormatoAttachment = f.minetype
                all.DescrizioneAttachment = f.description
                all.Attachment = f.datas
                allegati.append(all)

        return allegati

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

"""Unit test for fields.py"""

from PyFePA import fields
from PyFePA import fepa
import unittest
import datetime

tdatetime = datetime.datetime.today()
tdate = datetime.date.today()
tstr = 'stringa'
tint = 10
tdec = 12.20
tobj = fepa.Contatti
tconst = 'S'
tb64 = 'PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KCjxkYXRhcm9vdCB4bWxuczpvZD0idXJuOnNjaGVtYXMtbWljcm9zb2Z0LWNvbTpvZmZpY2VkYXRhIiAKCQkgIHhtbG5zOnhzaT0iaHR0cDovL3d3dy53My5vcmcvMjAwMS9YTUxTY2hlbWEtaW5zdGFuY2UiIAoJCSAgeHNpOm5vTmFtZXNwYWNlU2NoZW1hTG9jYXRpb249IkludGVyY2V0dGF6aW9uaS54c2QiIGdlbmVyYXRlZD0iMjAxMC0wMy0zMFQxMDo0MjoyMSI+CgoJPEludGVyY2V0dGF6aW9uaT4KCQk8SUQ+MTE8L0lEPgoJCTxCRU5FRklDSUFSSU8+MDQ1NzgxNDA4NzU8L0JFTkVGSUNJQVJJTz4KCQk8VElQT1BBR0FNRU5UTz5BQzwvVElQT1BBR0FNRU5UTz4KCQk8RU5URVBBR0FOVEU+RjwvRU5URVBBR0FOVEU+CgkJPE5VTUVST0ZBVFRVUkE+RTAxMTwvTlVNRVJPRkFUVFVSQT4KCQk8REFUQUVNSVNTSU9ORVBST1ZWPjwvREFUQUVNSVNTSU9ORVBST1ZWPgoJCTxOVU1FUk9NT0RFTExPMzc+PC9OVU1FUk9NT0RFTExPMzc+IAoJCTxSRUdJU1RSTz5OT1RJPC9SRUdJU1RSTz4KCQk8REFUQUZBVFRVUkE+MjAxNC0xMC0zMFQwMDowMDowMDwvREFUQUZBVFRVUkE+CgkJPElNUE9SVE9UT1RBTEU+NTIwOC4wMDwvSU1QT1JUT1RPVEFMRT4KCQk8SU1QT1JUT0lWQT4xMTQ1Ljc2PC9JTVBPUlRPSVZBPgoJCTxOUl9SRz40MjI5LzIwMTA8L05SX1JHPgoJCTxTRURFPjA4NTAwNDAyMTA0PC9TRURFPgoJCTxEQVRBSU5JWklPUFJFU1RBWklPTkU+MjAxNC0wNS0wMVQwMDowMDowMDwvREFUQUlOSVpJT1BSRVNUQVpJT05FPgoJCTxEQVRBRklORVBSRVNUQVpJT05FPjIwMTQtMDUtMzFUMDA6MDA6MDA8L0RBVEFGSU5FUFJFU1RBWklPTkU+CgkJPE5PTUVNQUdJU1RSQVRPPlN0ZWZhbm88L05PTUVNQUdJU1RSQVRPPgoJCTxDT0dOT01FTUFHSVNUUkFUTz5MdWNpYW5pPC9DT0dOT01FTUFHSVNUUkFUTz4KCQk8VElQT0lOVEVSQ0VUVEFaSU9ORT5DPC9USVBPSU5URVJDRVRUQVpJT05FPgoJPC9JbnRlcmNldHRhemlvbmk+Cgo8L2RhdGFyb290Pg=='

class fepaTest(unittest.TestCase):

    def testFiledString(self):
        sf = fields.FieldString(required=True, minlen=1, maxlen=12)
        sfb64 = fields.FieldString(required=True, minlen=1)
        self.assertEqual(tstr, sf.validate(tstr))
        self.assertEqual(unicode(tdate), sf.validate(tdate))
        self.assertEqual(False, sf.validate(tdatetime))
        self.assertEqual(unicode(tint), sf.validate(tint))
        self.assertEqual(unicode(tdec), sf.validate(tdec))
        self.assertEqual(False, sf.validate(tobj))
        self.assertEqual(tconst, sf.validate(tconst))
        self.assertEqual(False, sf.validate('abcdefghilmnop'))
        self.assertEqual(tb64, sfb64.validate(tb64))

    def testFieldDate(self):
        sf = fields.FieldDate(required=True, minlen=1, maxlen=6)
        self.assertEqual(False, sf.validate(tstr))
        self.assertEqual(tdate, sf.validate(tdate))
        self.assertEqual(tdatetime, sf.validate(tdatetime))
        self.assertEqual(False, sf.validate(tint))
        self.assertEqual(False, sf.validate(tdec))
        self.assertEqual(False, sf.validate(tobj))
        self.assertEqual(False, sf.validate(tconst))
        self.assertEqual(datetime.date(2015,1,1),sf.validate('2015-01-01'))
        self.assertEqual(False,sf.validate('2015-13-01'))

    def testFieldInteger(self):
        sf = fields.FieldInteger(required=True, minlen=1, maxlen=6)
        self.assertEqual(False, sf.validate(tstr))
        self.assertEqual(False, sf.validate(tdate))
        self.assertEqual(False, sf.validate(tdatetime))
        self.assertEqual(tint, sf.validate(tint))
        self.assertEqual(int(tdec), sf.validate(tdec))
        self.assertEqual(False, sf.validate(tobj))
        self.assertEqual(False, sf.validate(tconst))

    def testFieldDecimal(self):
        sf = fields.FieldDecimal(required=True, minlen=1, maxlen=6)
        self.assertEqual(False, sf.validate(tstr))
        self.assertEqual(False, sf.validate(tdate))
        self.assertEqual(False, sf.validate(tdatetime))
        self.assertEqual(tint, sf.validate(tint))
        self.assertEqual(tdec, sf.validate(tdec))
        self.assertEqual(False, sf.validate(tobj))
        self.assertEqual(False, sf.validate(tconst))

    def testFieldCostant(self):
        sf = fields.FieldCostant(required=True, cvalue=('S'))
        self.assertEqual(False, sf.validate(tstr))
        self.assertEqual(False, sf.validate(tdate))
        self.assertEqual(False, sf.validate(tdatetime))
        self.assertEqual(False, sf.validate(tint))
        self.assertEqual(False, sf.validate(tdec))
        self.assertEqual(False, sf.validate(tobj))
        self.assertEqual('S', sf.validate(tconst))
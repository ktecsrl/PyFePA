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

import datetime
import importlib
import dateutil.parser


class FieldType(object):

    required = False
    depend = None
    conflict = None
    code = 0
    multi = False

    def __init__(self, **kwargs):
        self.required = kwargs['required'] if kwargs.has_key('required') else False
        self.depend = kwargs['depend'] if kwargs.has_key('depend') else None
        self.conflict = kwargs['conflict'] if kwargs.has_key('conflict') else None
        self.code = kwargs['code'] if kwargs.has_key('code') else None
        self.multi = kwargs['multi'] if kwargs.has_key('multi') else False

    def validate(self, value):
        retval = False
        if (isinstance(value,list) or isinstance(value,tuple)) and self.multi:
            for v in value:
                retval = retval or self.validate(v)
        return value if retval else retval


class FieldString(FieldType):

    minlen = None
    maxlen = None
    type = 'S'

    def validate(self, value):
        valid = False
        if super(FieldString,self).validate(value):
            return value
        elif not (self.minlen and self.maxlen ):
            valid = True
        elif self.minlen and not self.maxlen :
            valid = self.minlen <= len(unicode(value))
        elif self.maxlen and not self.minlen:
            valid = len(unicode(value)) <= self.maxlen
        else:
            valid = self.minlen <= len(unicode(value)) <= self.maxlen

        if valid:
            return value if isinstance(value,(str,unicode)) else unicode(value)
        else:
            return valid

    def __init__(self, **kwargs):

        self.minlen = kwargs['minlen'] if kwargs.has_key('minlen') else False
        self.maxlen = kwargs['maxlen'] if kwargs.has_key('maxlen') else False

        super(FieldString,self).__init__(**kwargs)

    @classmethod
    def tostring(cls,value):
        return unicode(value)


class FieldCostant(FieldType):

    cvalue = None
    type = 'S'

    def validate(self, value):
        if super(FieldCostant,self).validate(value):
            return value
        elif unicode(value) in self.cvalue:
            return value
        else:
            return False

    def __init__(self, **kwargs):

        self.cvalue = kwargs['cvalue'] if kwargs.has_key('cvalue') else None

        super(FieldCostant,self).__init__(**kwargs)

    @classmethod
    def tostring(cls,value):
        return unicode(value)


class FieldInteger(FieldType):

    minlen = None
    maxlen = None
    type = 'S'

    def validate(self, value):
        try:
            if super(FieldInteger,self).validate(value):
                return value
            elif self.minlen <= len('{:0d}'.format(int(value))) <= self.maxlen:
                return int(value)
        except (ValueError, TypeError):
            return False

    def __init__(self, **kwargs):

        self.minlen = kwargs['minlen'] if kwargs.has_key('minlen') else None
        self.maxlen = kwargs['maxlen'] if kwargs.has_key('maxlen') else None

        super(FieldInteger,self).__init__(**kwargs)

    @classmethod
    def tostring(cls,value):
        return '{:0d}'.format(int(value))


class FieldDecimal(FieldType):

    minlen = None
    maxlen = None
    type = 'S'

    def validate(self, value):
        try:
            if super(FieldDecimal,self).validate(value):
                return value
            elif self.minlen <= len('{:.2f}'.format(float(value))) <= self.maxlen:
                return float(value)
        except(ValueError, TypeError):
            print 'DEBUG- ', value
            return False

    def __init__(self, **kwargs):

        self.minlen = kwargs['minlen'] if kwargs.has_key('minlen') else None
        self.maxlen = kwargs['maxlen'] if kwargs.has_key('maxlen') else None

        super(FieldDecimal,self).__init__(**kwargs)

    @classmethod
    def tostring(cls,value):
        return '{:.2f}'.format(float(value))


class FieldDate(FieldType):

    type = 'S'

    def validate(self, value):
        try:
            if isinstance(value, datetime.date):
                return value
            elif isinstance(value, datetime.datetime):
                return value.date()
            elif datetime.datetime.strptime(value[0:10], '%Y-%m-%d'):
                return datetime.datetime.strptime(value[0:10], '%Y-%m-%d').date()
        except Exception:
            return super(FieldDate,self).validate(value)

    @classmethod
    def tostring(cls,value):
        return str(value)

class FieldDateTime(FieldType):

    type = 'S'

    def validate(self, value):
        try:
            if isinstance(value, datetime.datetime):
                return value
            elif dateutil.parser.parse(value):
                return dateutil.parser.parse(value)
        except Exception:
            return super(FieldDateTime,self).validate(value)

    @classmethod
    def tostring(cls,value):
        return value.isoformat()


class FieldObject(FieldType):

    object_class = None
    type = 'O'

    def validate(self, value):
        if super(FieldObject,self).validate(value) or \
                isinstance(value,class_for_name('PyFePA.fepa',self.object_class)):
           return value
        else:
            False

    def __init__(self, **kwargs):

        self.object_class = kwargs['object_class'] if kwargs.has_key('object_class') else False
        super(FieldObject,self).__init__(**kwargs)

    @classmethod
    def tostring(cls,value):
        return str('Object: '+str(value))


def class_for_name(module_name, class_name):

    m = importlib.import_module(module_name)
    c = getattr(m, class_name)
    return c
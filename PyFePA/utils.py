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

def piva(value):

    if value is None:
        return False

    value = value.strip('IT')

    if (len(value) != 11) or not value.isdigit():
        return False

    value = map(int, value)
    checksum = sum(map(lambda x: value[x], xrange(0, 10, 2)))
    checksum += sum(map(lambda x: (2 * value[x]) - 9 if (2 * value[x]) > 9 else (2 * value[x]) , xrange(1, 10, 2)))
    checksum = 10 - (checksum % 10) if checksum % 10 != 0 else 0

    return value[10] == checksum


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

from distutils.core import setup

files = ["xsd/*.xsd"]

setup(
  name = 'PyFePA',
  packages = ['PyFePA'],
  version = '1.2.1b',
  description = 'Python object of italian FatturaPA, serialize, deserialize and verify',
  author = 'Luigi Di Naro',
  author_email = 'Luigi.DiNaro@ktec.it',
  url = 'https://github.com/ktecsrl/PyFePA',
  download_url = 'https://github.com/ktecsrl/PyFePA/tarball/1.2.1b',
  keywords = ['FatturaPA', 'financial', 'utils'],
  platforms= 'OSX, *unix, win',
  package_data = {'PyFePA' : files },
  license= 'AGPLv3',
  classifiers = [],
)
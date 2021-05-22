# Python bindings for gnucash
#
# to get started have a look at
# * the example files
# * doxygen source docs (https://lists.gnucash.org/docs/MAINT/python_bindings_page.html)
# * wiki (https://wiki.gnucash.org/wiki/Python_Bindings)
# * source documentation (in some places rather sparse)
#
# import all the symbols from gnucash_core, so basic gnucash stuff can be
# loaded with:
# >>> from gnucash import thingy
# instead of
# >>> from gnucash.gnucash_core import thingy
#
##  @file
#   @brief helper file for the importing of gnucash
#   @author Mark Jenkins, ParIT Worker Co-operative <mark@parit.ca>
#   @author Jeff Green,   ParIT Worker Co-operative <jeff@parit.ca>
#   @ingroup python_bindings

from gnucash.gnucash_core import *
from . import app_utils
from . import deprecation

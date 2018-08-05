#!/usr/bin/env python
## @file
#  @brief Add __str__ and __unicode__ methods to financial objects so that
#  @code print object @endcode leads to human readable results
""" @package str_methods.py -- Add __str__ and __unicode__ methods to
   financial objects

   Import this module and str(Object) and unicode(Object) where Object is
   Transaction, Split,Invoice or Entry leads to human readable results. That
   is handy when using @code print object @endcode

   I chose to put these functions/methods in a seperate file to develop them
   like this and maybe if they prove to be useful they can be put in
   gnucash_core.py.

   I am searching to find the best way to serialize these complex objects.
   Ideally this serialization would be configurable.

   If someone has suggestions how to beautify, purify or improve this code in
   any way please feel free to do so.

   This is written as a first approach to a shell-environment using ipython to
   interactively manipulate GnuCashs Data."""

#   @author Christoph Holtermann, c.holtermann@gmx.de
#   @ingroup python_bindings_examples
#   @date May 2011
#
#   ToDo :
#
#   * Testing for SWIGtypes
#   * dealing the cutting format in a bit more elegant way
#   * having setflag as a classmethod makes it probably impossible to have
#     flags on instance level. Would changing that be useful ?
#   * It seems useful to have an object for each modification. That is
#     because there is some Initialisation to be done.
#

import gnucash
import function_class
import gnucash.gnucash_business

# Default values for encoding of strings in GnuCashs Database
DEFAULT_ENCODING = "UTF-8"
DEFAULT_ERROR = "ignore"


def setflag(self, name, value):
    if not(name in self.OPTIONFLAGS_BY_NAME):
        self.register_optionflag(name)
    if value is True:
        self.optionflags |= self.OPTIONFLAGS_BY_NAME[name]
    else:
        self.optionflags &= ~self.OPTIONFLAGS_BY_NAME[name]


def getflag(self, name):
    if not(name in self.OPTIONFLAGS_BY_NAME):
        raise KeyError(str(name)+" is not a registered key.")
    return ((self.optionflags & self.OPTIONFLAGS_BY_NAME[name]) != 0)


def register_optionflag(self,name):
    """Taken from doctest.py"""
    # Create a new flag unless `name` is already known.
    return self.OPTIONFLAGS_BY_NAME.setdefault(
        name,
        1 << len(self.OPTIONFLAGS_BY_NAME))


def ya_add_method(_class, function, method_name=None,
                  clsmethod=False, noinstance=False):
    """Calls add_method from function_methods.py but makes it
    possible to use functions in this module. Also keeps the
    docstring"""

    if method_name is None:
        method_name = function.__name__

    setattr(gnucash.gnucash_core_c, function.__name__, function)
    if clsmethod:
        mf = _class.ya_add_classmethod(function.__name__, method_name)
    elif noinstance:
        mf = _class.add_method(function.__name__, method_name)
    else:
        mf = _class.ya_add_method(function.__name__, method_name)
    if function.__doc__ is not None:
        setattr(mf, "__doc__", function.__doc__)


def infect(_class, function, method_name):
    if not getattr(_class, "OPTIONFLAGS_BY_NAME", None):
        _class.OPTIONFLAGS_BY_NAME = {}
        _class.optionflags = 0
        ya_add_method(_class, register_optionflag, clsmethod=True)
        ya_add_method(_class, setflag, clsmethod=True)
        ya_add_method(_class, getflag, clsmethod=True)
    ya_add_method(_class, function, method_name)


class ClassWithCutting__format__():
    """This class provides a __format__ method which cuts values
    to given width.

    If string is too wide '...' will be put to its end.
    """

    def __init__(self, value):
        self.value = value

    def __format__(self, fmt):
        def get_width(fmt_spec):
            """Parse fmt_spec to obtain width"""

            def remove_alignment(fmt_spec):
                if fmt_spec[1] in ["<", "^", ">"]:
                    fmt_spec = fmt_spec[2:len(fmt_spec)]
                return fmt_spec

            def remove_sign(fmt_spec):
                if fmt_spec[0] in ["-", "+", " "]:
                    fmt_spec = fmt_spec[1:len(fmt_spec)]
                return fmt_spec

            def remove_cross(fmt_spec):
                if fmt_spec[0] in ["#"]:
                    fmt_spec = fmt_spec[1:len(fmt_spec)]
                return fmt_spec

            def do_width(fmt_spec):
                n = ""

                while len(fmt_spec) > 0:
                    if fmt_spec[0].isdigit():
                        n += fmt_spec[0]
                        fmt_spec = fmt_spec[1:len(fmt_spec)]
                    else:
                        break
                if n:
                    return int(n)
                else:
                    return None

            if len(fmt_spec) >= 2:
                fmt_spec = remove_alignment(fmt_spec)
            if len(fmt_spec) >= 1:
                fmt_spec = remove_sign(fmt_spec)
            if len(fmt_spec) >= 1:
                fmt_spec = remove_cross(fmt_spec)
            width = do_width(fmt_spec)
            # Stop parsing here for we only need width

            return width

        def cut(s, width, replace_string="..."):
            """Cuts s to width and puts replace_string at it's end."""

            # s=s.decode('UTF-8', "replace")

            if len(s) > width:
                if len(replace_string) > width:
                    replace_string = replace_string[0:width]
                s = s[0:width-len(replace_string)]
                s = s+replace_string

            return s

        value = self.value

        # Replace Tabs and linebreaks
        if type(value) in [bytes, str]:
            value = value.replace("\t", "|")
            value = value.replace("\n", "|")

        try:
            # Do regular formatting of object - ignore errors
            value = format(value, fmt)

            # Cut resulting value if longer than specified by width
            width = get_width(fmt)
            if width:
                value = cut(value, width, "...")

        except:
            pass

        if not isinstance(value, str):
            return str(value)
        else:
            return value


def all_as_classwithcutting__format__(*args):
    """Converts every argument to instance of ClassWithCutting__format__"""

    l = []
    for a in args:
        if type(a) in [bytes]:
            a = str(a)
        l.append(ClassWithCutting__format__(a))

    return l


def all_as_classwithcutting__format__keys(encoding=None, error=None, **keys):
    """Converts every argument to instance of ClassWithCutting__format__"""

    d = {}
    if encoding is None:
        encoding = DEFAULT_ENCODING
    if error is None:
        error = DEFAULT_ERROR
    for a in keys:
        if type(keys[a]) in [bytes]:
            keys[a] = str(keys[a])
        d[a] = ClassWithCutting__format__(keys[a])

    return d


# Split
def __split__str__(self, encoding=None, error=None):
    """__str__(self, encoding=None, error=None) -> object

    Serialize the Split object and return as a new Unicode object.

    Keyword arguments:
    encoding -- defaults to str_methods.default_encoding
    error -- defaults to str_methods.default_error
    See help(unicode) for more details or
    http://docs.python.org/howto/unicode.html.

    """

    from gnucash import Split
    import time
    #self=Split(instance=self)

    lot = self.GetLot()
    if lot:
        if type(lot).__name__ == 'SwigPyObject':
            lot = gnucash.GncLot(instance=lot)
        lot_str = lot.get_title()
    else:
        lot_str = '---'

    transaction = self.GetParent()

    # This dict and the return statement can be changed according to individual
    # needs
    fmt_dict = {
        "account": self.GetAccount().name,
        "value": self.GetValue(),
        "memo": self.GetMemo(),
        "lot": lot_str}

    fmt_str = ("Account: {account:20} " +
               "Value: {value:10} " +
               "Memo: {memo:30} ")

    if self.optionflags & self.OPTIONFLAGS_BY_NAME["PRINT_TRANSACTION"]:
        fmt_t_dict = {
            "transaction_time": transaction.GetDate(),
            "transaction2": transaction.GetDescription()}
        fmt_t_str = (
            "Transaction: {transaction_time:30} " +
            "- {transaction2:30} " +
            "Lot: {lot:10}")
        fmt_dict.update(fmt_t_dict)
        fmt_str += fmt_t_str

    return fmt_str.format(**all_as_classwithcutting__format__keys(
        encoding, error, **fmt_dict))

# This could be something like an __init__. Maybe we could call it virus
# because it infects the Split object which thereafter mutates to have better
# capabilities.
infect(gnucash.Split, __split__str__, "__str__")
gnucash.Split.register_optionflag("PRINT_TRANSACTION")
gnucash.Split.setflag("PRINT_TRANSACTION", True)


def __transaction__str__(self):
    """__unicode__ method for Transaction class"""
    from gnucash import Transaction
    self = Transaction(instance=self)

    fmt_tuple = ('Date:', self.GetDate(),
                 'Description:', self.GetDescription(),
                 'Notes:', self.GetNotes())

    transaction_str = "{0:6}{1:25} {2:14}{3:40} {4:7}{5:40}".format(
                      *all_as_classwithcutting__format__(*fmt_tuple))
    transaction_str += "\n"

    splits_str = ""
    for n, split in enumerate(self.GetSplitList()):
        if not (type(split) == gnucash.Split):
            split = gnucash.Split(instance=split)

        transaction_flag = split.getflag("PRINT_TRANSACTION")
        split.setflag("PRINT_TRANSACTION", False)
        splits_str += "[{0:>2}] ".format(str(n))
        splits_str += str(split)
        splits_str += "\n"
        split.setflag("PRINT_TRANSACTION", transaction_flag)

    return transaction_str + splits_str

# These lines add transaction_str as method __str__ to Transaction object
gnucash.gnucash_core_c.__transaction__str__ = __transaction__str__
gnucash.Transaction.add_method("__transaction__str__", "__str__")


def __invoice__str__(self):
    """__str__ method for Invoice"""

    from gnucash.gnucash_business import Invoice
    self = Invoice(instance=self)

    # This dict and the return statement can be changed according to individual
    # needs
    fmt_dict = {
        "id_name": "ID:",
        "id_value": self.GetID(),
        "notes_name": "Notes:",
        "notes_value": self.GetNotes(),
        "active_name": "Active:",
        "active_value": str(self.GetActive()),
        "owner_name": "Owner Name:",
        "owner_value": self.GetOwner().GetName(),
        "total_name": "Total:",
        "total_value": str(self.GetTotal()),
        "currency_mnemonic": self.GetCurrency().get_mnemonic()}

    ret_invoice= ("{id_name:4}{id_value:10} {notes_name:7}{notes_value:20} {active_name:8}{active_value:7} {owner_name:12}{owner_value:20}"+
                  "{total_name:8}{total_value:10}{currency_mnemonic:3}").\
        format(**all_as_classwithcutting__format__keys(**fmt_dict))

    ret_entries = ""
    entry_list = self.GetEntries()
    for entry in entry_list:  # Type of entry has to be checked
        if not(type(entry) == Entry):
            entry = Entry(instance=entry)
        ret_entries += "  "+str(entry)+"\n"

    return ret_invoice+"\n"+ret_entries

gnucash.gnucash_core_c.__invoice__str__ = __invoice__str__
gnucash.gnucash_business.Invoice.add_method("__invoice__str__", "__str__")


def __entry__str__(self):
    """__unicode__ method for Entry"""

    from gnucash.gnucash_business import Entry
    self = Entry(instance=self)

    # This dict and the return statement can be changed according to individual
    # needs
    fmt_dict = {
        "date_name": "Date:",
        "date_value": str(self.GetDate()),
        "description_name": "Description:",
        "description_value": self.GetDescription(),
        "notes_name": "Notes:",
        "notes_value": self.GetNotes(),
        "quant_name": "Quantity:",
        "quant_value": str(self.GetQuantity()),
        "invprice_name": "InvPrice:",
        "invprice_value": str(self.GetInvPrice())}

    return ("{date_name:6}{date_value:15} {description_name:13}{description_value:20} {notes_name:7}{notes_value:20}"+
            "{quant_name:12}{quant_value:7} {invprice_name:10}{invprice_value:7}").\
        format(**all_as_classwithcutting__format__keys(**fmt_dict))


from gnucash.gnucash_business import Entry

gnucash.gnucash_core_c.__entry__str__ = __entry__str__
gnucash.gnucash_business.Entry.add_method("__entry__str__", "__str__")

from gnucash import GncNumeric

def __gncnumeric__str__(self):
    """Returns a human readable numeric value string as UTF8.

    on this level this is still a swig object. to_double can not be called.
    temporary conversion to python is necessary. there are surely better
    solutions. no conversion and finding an alternative to self.to_double
    or binding these methods in a level where conversion to python objects
    has already taken place.

    """

    if hasattr(self, '_ClassFromFunctions__WrappingObject'):
        higherself = getattr(self, '_ClassFromFunctions__WrappingObject')
    else:
        higherself = GncNumeric(instance=self)

    if higherself.denom() == 0:
        return "Division by zero"
    else:
        value_float = higherself.to_double()
        value_str = u"{0:.{1}f}".format(value_float, 2)
        # The second argument is the precision.
        # It would be nice to be able to make it configurable.

        return value_str


def __gncnumeric__format__(self, formatstring):
    """Format function for GncNumeric"""

    from gnucash import GncNumeric
    tempself = GncNumeric(instance=self)

    return format(str(tempself), formatstring)

gnucash.gnucash_core_c.__gncnumeric__str__ = __gncnumeric__str__
gnucash.gnucash_business.GncNumeric.add_method(
    "__gncnumeric__str__", "__str__")

gnucash.gnucash_core_c.__gncnumeric__format__ = __gncnumeric__format__
gnucash.gnucash_business.GncNumeric.add_method(
    "__gncnumeric__format__", "__format__")

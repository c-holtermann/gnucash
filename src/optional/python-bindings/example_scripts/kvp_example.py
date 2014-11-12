#!/usr/bin/env python
# -*- coding: UTF-8 -*-

##@file
# @ingroup python_bindings_examples
# @author Christoph Holtermann (c.holtermann (at) gmx.de)
# @date June 2014
# @brief Accessing key value pairs. Owners address is fetched here.

try:
    import sys
    import gnucash
    from IPython import embed
    from gncCompany import Company
except ImportError as import_error:
    print "Problem importing modules."
    print import_error
    sys.exit(2)

input_url = ""
a = 1

def main(argv=None):
    global input_url

    if argv is None:
        argv = sys.argv
        print "Reading url from arguments."
        if len(argv) == 1:
            print "No arguments given"
            print "invoke as", sys.argv[0], "GNUCASH_URL_TO_OPEN"
            return 2

    print input_url
    if input_url == "":
        input_url = argv[1]

    print "opening", input_url
    try:
        session = gnucash.Session(input_url, ignore_lock=True)
    except Exception as exception:
        print "Problem opening input."
        print exception
        return 2

    book = session.book
    slots = gnucash.gnucash_core.gnucash_core_c.qof_book_get_slots(book.instance)
    # or
    slots = book.get_slots()

    # or
    book_qof_instance = book.get_qof_instance()
    slots = gnucash.gnucash_core.gnucash_core_c.qof_instance_get_slots(book_qof_instance.instance)
    print "1) Slots:", slots
    # or
    slots = book_qof_instance.get_slots()
    print "2) Slots:", slots

    print slots.get_string("options/Business/Company Phone Number")

    c = Company(book)
    print c.GetName()

    # print gnucash.gnucash_core.gnucash_core_c.kvp_frame_to_string(slots.instance)
    # or
    print "Slots recursively printed:"
    print slots.to_string()

    # options = gnucash.gnucash_core.gnucash_core_c.kvp_frame_get_frame(slots.instance, "options")
    options = slots.get_frame("options")
    print "options:", options
    #business = gnucash.gnucash_core.gnucash_core_c.kvp_frame_get_frame(options, "Business")
    business = options.get_frame("Business")
    print "business:", business
    print "-to_string:", business.to_string()
    #print gnucash.gnucash_core.gnucash_core_c.kvp_frame_to_string(business)

    print "Phone number:",
    phone_number = options.get_string("Business/Company Phone Number")
    # phone_number = gnucash.gnucash_core.gnucash_core_c.kvp_frame_get_string(options, "Business/Company Phone Number")
    print phone_number

    # It's possible to get the book from qofinstance
    book2 = book_qof_instance.get_book()

    slots.print_rec()

    # Find an account with splits to demonstrate the kvp in Transactions
    r = book.get_root_account()
    for r_desc in r.get_descendants():
        if len(r_desc.GetSplitList()) != 0:
            splits_found = True
            print "Splits found in", r_desc.get_full_name()
            break

    # Print all kvp information in splits of this account
    for s in r_desc.GetSplitList():
        t=s.GetParent()
        gnucash.KvpFrame(instance=t.GetFrame()).print_rec()

    session.end()

if __name__ == "__main__":
    sys.exit(main())

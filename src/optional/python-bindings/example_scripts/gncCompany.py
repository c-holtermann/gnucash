#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class Company(object):
    """Information about the Company that owns the book.

    This object only exists in the python bindings. The c-API to
    access this information is going to change soon. So don't rely
    on this form of the object too much.
    """
    def __init__(self, book):
        self.book = book
        self.slots = self.book.get_slots()

    def GetName(self):
        return self.slots.get_string("options/Business/Company Name")

    def GetAddress(self):
        return self.slots.get_string("options/Business/Company Address")

    def GetID(self):
        return self.slots.get_string("options/Business/Company ID")

    def GetPhone(self):
        return self.slots.get_string("options/Business/Company Phone Number")

    def GetFax(self):
        return self.slots.get_string("options/Business/Company Fax Number")

    def GetWebsite(self):
        return self.slots.get_string("options/Business/Company Website URL")

    def GetEmail(self):
        return self.slots.get_string("options/Business/Company Email Address")

    def GetContactPerson(self):
        return self.slots.get_string("options/Business/Company Contact Person")

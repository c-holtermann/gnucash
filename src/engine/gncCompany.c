/********************************************************************\
 * gncCompany.c -- a Company object                                 *
 *                                                                  *
 * This program is free software; you can redistribute it and/or    *
 * modify it under the terms of the GNU General Public License as   *
 * published by the Free Software Foundation; either version 2 of   *
 * the License, or (at your option) any later version.              *
 *                                                                  *
 * This program is distributed in the hope that it will be useful,  *
 * but WITHOUT ANY WARRANTY; without even the implied warranty of   *
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the    *
 * GNU General Public License for more details.                     *
 *                                                                  *
 * You should have received a copy of the GNU General Public License*
 * along with this program; if not, contact:                        *
 *                                                                  *
 * Free Software Foundation           Voice:  +1-617-542-5942       *
 * 51 Franklin Street, Fifth Floor    Fax:    +1-617-542-2652       *
 * Boston, MA  02110-1301,  USA       gnu@gnu.org                   *
 *                                                                  *
\********************************************************************/

/*
 * Copyright (C) 2014 Christoph Holtermann
 * Author: Christoph Holtermann <c.holtermann@gmx.de>
 */

#include <config.h>
#include "gnc-engine.h"

#include <glib.h>
#include <qofinstance-p.h>

#include "gncCompany.h"
#include "gnc-features.h"

#include "qofbook.h"

struct _gncCompany
{
    QofInstance inst;

    QofBook *	book;
    gboolean	dirty;
    char *	name;
    char *	address;
    char *	id;
    char *	phone;
    char *	fax;
    char *	website;
    char *	email;
    char *	contactperson;
};

struct _gncCompanyClass
{
    QofInstanceClass parent_class;
};

static QofLogModule log_module = GNC_MOD_BUSINESS;

#define _GNC_MOD_NAME	GNC_COMPANY_MODULE_NAME

G_INLINE_FUNC void mark_company (GncCompany *company);
void mark_company (GncCompany *company)
{
    qof_instance_set_dirty(QOF_INSTANCE(company));
    qof_event_gen (QOF_INSTANCE(company), QOF_EVENT_MODIFY, NULL);
}

enum
{
    PROP_0,
    PROP_NAME,
    PROP_ADDR,
    PROP_ID,
    PROP_PHONE,
    PROP_FAX,
    PROP_WEBSITE,
    PROP_EMAIL,
    PROP_CONTACTPERSON
};


/* GObject Initialization */
G_DEFINE_TYPE(GncCompany, gnc_company, QOF_TYPE_INSTANCE);

static void
gnc_company_init(GncCompany* company)
{
}

static void
gnc_company_dispose(GObject *companyp)
{
    G_OBJECT_CLASS(gnc_company_parent_class)->dispose(companyp);
}

static void
gnc_company_finalize(GObject* companyp)
{
    G_OBJECT_CLASS(gnc_company_parent_class)->finalize(companyp);
}

static void
gnc_company_set_property (GObject         *object,
                          guint            prop_id,
                          const GValue          *value,
                          GParamSpec      *pspec)
{
    GncCompany *company;

    g_return_if_fail(GNC_IS_COMPANY(object));

    company = GNC_COMPANY(object);
    switch (prop_id)
    {
    case PROP_NAME:
        gncCompanySetName(company, g_value_get_string(value));
        break;
    case PROP_ADDR:
        gncCompanySetAddress(company, g_value_get_string(value));
        break;
    case PROP_ID:
        gncCompanySetId(company, g_value_get_string(value));
        break;
    case PROP_PHONE:
        gncCompanySetPhone(company, g_value_get_string(value));
        break;
    case PROP_FAX:
        gncCompanySetFax(company, g_value_get_string(value));
        break;
    case PROP_WEBSITE:
        gncCompanySetWebsite(company, g_value_get_string(value));
        break;
    case PROP_EMAIL:
        gncCompanySetEmail(company, g_value_get_string(value));
        break;
    case PROP_CONTACTPERSON:
        gncCompanySetContactperson(company, g_value_get_string(value));
        break;
    default:
        G_OBJECT_WARN_INVALID_PROPERTY_ID(object, prop_id, pspec);
        break;
    }
}



static void
gnc_company_get_property (GObject         *object,
                          guint            prop_id,
                          GValue          *value,
                          GParamSpec      *pspec)
{
    GncCompany *company;

    g_return_if_fail(GNC_IS_COMPANY(object));

    company = GNC_COMPANY(object);
    switch (prop_id)
    {
    case PROP_NAME:
        g_value_set_string(value, company->name);
        break;
    case PROP_ADDR:
        g_value_set_string(value, company->address);
        break;
    case PROP_ID:
        g_value_set_string(value, company->id);
        break;
    case PROP_PHONE:
        g_value_set_string(value, company->phone);
        break;
    case PROP_FAX:
        g_value_set_string(value, company->fax);
        break;
    case PROP_WEBSITE:
        g_value_set_string(value, company->website);
        break;
    case PROP_EMAIL:
        g_value_set_string(value, company->email);
        break;
    case PROP_CONTACTPERSON:
        g_value_set_string(value, company->contactperson);
        break;
    default:
        G_OBJECT_WARN_INVALID_PROPERTY_ID(object, prop_id, pspec);
        break;
    }
}

static void
gnc_company_class_init (GncCompanyClass *klass)
{
   GObjectClass *gobject_class = G_OBJECT_CLASS (klass);
   QofInstanceClass* qof_class = QOF_INSTANCE_CLASS(klass);	

   gobject_class->dispose = gnc_company_dispose;
   gobject_class->finalize = gnc_company_finalize;
   gobject_class->set_property = gnc_company_set_property;
   gobject_class->get_property = gnc_company_get_property;
  
   qof_class->get_display_name = NULL;
   qof_class->refers_to_object = NULL;
   qof_class->get_typed_referring_object_list = NULL;
   
   g_object_class_install_property(
     gobject_class,
     PROP_NAME,
     g_param_spec_string ("Name",
                          "",
			  "",
			  NULL,
                          G_PARAM_READWRITE));

   g_object_class_install_property(
     gobject_class,
     PROP_ADDR,
     g_param_spec_string ("Address",
			  "",
			  "",
                          NULL,
                          G_PARAM_READWRITE));

   g_object_class_install_property(
     gobject_class,
     PROP_ID,
     g_param_spec_string ("ID",
                          "",
			  "",
			  NULL,
                          G_PARAM_READWRITE));

   g_object_class_install_property(
     gobject_class,
     PROP_PHONE,
     g_param_spec_string ("Phone",
			  "",
			  "",
                          NULL,
                          G_PARAM_READWRITE));

   g_object_class_install_property(
     gobject_class,
     PROP_FAX,
     g_param_spec_string ("Fax",
			  "",
			  "",
                          NULL,
                          G_PARAM_READWRITE));

   g_object_class_install_property(
     gobject_class,
     PROP_WEBSITE,
     g_param_spec_string ("Website",
			  "",
			  "",
                          NULL,
                          G_PARAM_READWRITE));
    
   g_object_class_install_property(
     gobject_class,
     PROP_EMAIL,
     g_param_spec_string ("Email",
			  "",
			  "",
                          NULL,
                          G_PARAM_READWRITE));

   g_object_class_install_property(
     gobject_class,
     PROP_CONTACTPERSON,
     g_param_spec_string ("Contact Person",
			  "",
			  "",
                          NULL,
                          G_PARAM_READWRITE));
}

/* Create/Destroy functions */

GncCompany *
gncCompanyCreate (QofBook *book)
{
   GncCompany *company;

   if (!book) return NULL;

   company = g_object_new (GNC_TYPE_COMPANY, NULL);
   qof_instance_init_data(&company->inst, GNC_ID_COMPANY, book);
   company->book = book;
   company->dirty = FALSE;

   company->name = CACHE_INSERT ("");
   company->address = CACHE_INSERT ("");
   company->id = CACHE_INSERT ("");
   company->phone = CACHE_INSERT ("");
   company->fax = CACHE_INSERT ("");
   company->website = CACHE_INSERT ("");
   company->email = CACHE_INSERT ("");
   company->contactperson = CACHE_INSERT ("");	

   return company;
}

static GncCompany *
qofCompanyCreate (QofBook *book)
{
    return gncCompanyCreate(book);
}

void
gncCompanyDestroy (GncCompany *company)
{
    if (!company) return;
    qof_instance_set_destroying(company, TRUE);
    gncCompanyCommitEdit (company);
}

static void
gncCompanyFree (GncCompany *company)
{
    if (!company) return;

    qof_event_gen (&company->inst, QOF_EVENT_DESTROY, NULL);

    CACHE_REMOVE (company->address);
    CACHE_REMOVE (company->name);
    CACHE_REMOVE (company->id);
    CACHE_REMOVE (company->phone);
    CACHE_REMOVE (company->fax);
    CACHE_REMOVE (company->email);
    CACHE_REMOVE (company->website);
    CACHE_REMOVE (company->contactperson);

    /* qof_instance_release (&addr->inst); */
    g_object_unref (company);
}

/* Set functions */

#define SET_STR(obj, member, str) { \
	char * tmp; \
	\
	if (member == str) return; \
	if (!g_strcmp0 (member, str)) return; \
	gncCompanyBeginEdit (obj); \
	tmp = CACHE_INSERT (str); \
	CACHE_REMOVE (member); \
	member = tmp; \
	}

void gncCompanySetName (GncCompany *company, const char *name)
{
    const char * orig_val;

    if (!company) return;
    if (!name) return;

    orig_val = gncCompanyGetName(company);
    if (name == orig_val) return;
    if (!g_strcmp0 (name, orig_val)) return;
    gncCompanyBeginEdit (company);
    qof_book_set_string_option(company->book, "options/Business/Company Name", name);
    mark_company (company);
    gncCompanyCommitEdit (company);
}

void gncCompanySetAddress (GncCompany *company, const char *address)
{
    const char * orig_val;

    if (!company) return;
    if (!address) return;

    orig_val = gncCompanyGetAddress(company);
    if (address == orig_val) return;
    if (!g_strcmp0 (address, orig_val)) return;
    gncCompanyBeginEdit (company);
    qof_book_set_string_option(company->book, "options/Business/Company Address", address);
    mark_company (company);
    gncCompanyCommitEdit (company);
}

void gncCompanySetId (GncCompany *company, const char *id)
{
    const char * orig_val;

    if (!company) return;
    if (!id) return;

    orig_val = gncCompanyGetId(company);
    if (id == orig_val) return;
    if (!g_strcmp0 (id, orig_val)) return;
    gncCompanyBeginEdit (company);
    qof_book_set_string_option(company->book, "options/Business/Company ID", id);
    mark_company (company);
    gncCompanyCommitEdit (company);
}

void gncCompanySetPhone (GncCompany *company, const char *phone)
{
    const char * orig_val;

    if (!company) return;
    if (!phone) return;

    orig_val = gncCompanyGetPhone(company);
    if (phone == orig_val) return;
    if (!g_strcmp0 (phone, orig_val)) return;
    gncCompanyBeginEdit (company);
    qof_book_set_string_option(company->book, "options/Business/Company Phone Number", phone);
    mark_company (company);
    gncCompanyCommitEdit (company);
}

void gncCompanySetFax (GncCompany *company, const char *fax)
{
    const char * orig_val;

    if (!company) return;
    if (!fax) return;

    orig_val = gncCompanyGetFax(company);
    if (fax == orig_val) return;
    if (!g_strcmp0 (fax, orig_val)) return;
    gncCompanyBeginEdit (company);
    qof_book_set_string_option(company->book, "options/Business/Company Fax Number", fax);
    mark_company (company);
    gncCompanyCommitEdit (company);
}

void gncCompanySetWebsite (GncCompany *company, const char *website)
{
    const char * orig_val;

    if (!company) return;
    if (!website) return;

    orig_val = gncCompanyGetWebsite(company);
    if (website == orig_val) return;
    if (!g_strcmp0 (website, orig_val)) return;
    gncCompanyBeginEdit (company);
    qof_book_set_string_option(company->book, "options/Business/Company Website URL", website);
    mark_company (company);
    gncCompanyCommitEdit (company);
}

void gncCompanySetEmail (GncCompany *company, const char *email)
{
    const char * orig_val;

    if (!company) return;
    if (!email) return;

    orig_val = gncCompanyGetEmail(company);
    if (email == orig_val) return;
    if (!g_strcmp0 (email, orig_val)) return;
    gncCompanyBeginEdit (company);
    qof_book_set_string_option(company->book, "options/Business/Company Email", email);
    mark_company (company);
    gncCompanyCommitEdit (company);
}

void gncCompanySetContactperson (GncCompany *company, const char *contactperson)
{
    const char * orig_val;

    if (!company) return;
    if (!contactperson) return;

    orig_val = gncCompanyGetContactperson(company);
    if (contactperson == orig_val) return;
    if (!g_strcmp0 (contactperson, orig_val)) return;
    gncCompanyBeginEdit (company);
    qof_book_set_string_option(company->book, "options/Business/Company Contact Person", contactperson);
    mark_company (company);
    gncCompanyCommitEdit (company);
}

void gncCompanyBeginEdit (GncCompany *company)
{
    qof_begin_edit (&company->inst);
}

static void gncCompanyOnError (QofInstance *inst, QofBackendError errcode)
{
    PERR("Company QofBackend Failure: %d", errcode);
    gnc_engine_signal_commit_error( errcode );
}

static void gncCompanyOnDone (QofInstance *company) { }

static void company_free (QofInstance *inst)
{
    GncCompany *company = (GncCompany *) inst;
    gncCompanyFree (company);
}

void gncCompanyCommitEdit (GncCompany *company)
{
    /* GnuCash 2.6.3 and earlier didn't handle address kvp's... */
    /*if (!kvp_frame_is_empty (addr->inst.kvp_data))
        gnc_features_set_used (qof_instance_get_book (QOF_INSTANCE (addr)), GNC_FEATURE_KVP_EXTRA_DATA);*/

    if (!qof_commit_edit (QOF_INSTANCE(company))) return;
    qof_commit_edit_part2 (&company->inst, gncCompanyOnError,
                           gncCompanyOnDone, company_free);
}

/* Get Functions */
QofBook * gncCompanyGetBook (const GncCompany *company)
{
    if (!company) return NULL;
    return company->book;
}

const char * gncCompanyToString (const GncCompany *company)
{
    if (!company) return NULL;
    return kvp_frame_to_string(kvp_frame_get_frame(qof_instance_get_slots (QOF_INSTANCE (company->book)), "options/Business"));
}

const char * gncCompanyGetName (const GncCompany *company)
{
    if (!company) return NULL;
    return qof_book_get_string_option(company->book, "options/Business/Company Name");
}

const char * gncCompanyGetAddress (const GncCompany *company)
{
    if (!company) return NULL;
    return qof_book_get_string_option(company->book, "options/Business/Company Address");
}

const char * gncCompanyGetId (const GncCompany *company)
{
    if (!company) return NULL;
    return qof_book_get_string_option(company->book, "options/Business/Company ID");
}   

const char * gncCompanyGetPhone (const GncCompany *company)
{
    if (!company) return NULL;
    return qof_book_get_string_option(company->book, "options/Business/Company Phone Number");
}

const char * gncCompanyGetFax (const GncCompany *company)
{
    if (!company) return NULL;
    return qof_book_get_string_option(company->book, "options/Business/Company Fax Number");
}

const char * gncCompanyGetWebsite (const GncCompany *company)
{
    if (!company) return NULL;
    return qof_book_get_string_option(company->book, "options/Business/Company Website URL");
}

const char * gncCompanyGetEmail (const GncCompany *company)
{
    if (!company) return NULL;
    return qof_book_get_string_option(company->book, "options/Business/Company Email Address");
}

const char * gncCompanyGetContactperson (const GncCompany *company)
{
    if (!company) return NULL;
    return qof_book_get_string_option(company->book, "options/Business/Company Contact Person");
}   

static QofObject GncCompanyDesc =
{
    DI(.interface_version = ) QOF_OBJECT_VERSION,
    DI(.e_type            = ) GNC_ID_COMPANY,
    DI(.type_label        = ) "Company",
    DI(.create            = ) (gpointer)qofCompanyCreate,
    DI(.book_begin        = ) NULL,
    DI(.book_end          = ) NULL,
    DI(.is_dirty          = ) qof_collection_is_dirty,
    DI(.mark_clean        = ) qof_collection_mark_clean,
    DI(.foreach           = ) qof_collection_foreach,
    DI(.printable         = ) NULL,
    DI(.version_cmp       = ) (int (*)(gpointer, gpointer)) qof_instance_version_cmp,
};

gboolean gncCompanyRegister (void)
{
    static QofParam params[] =
    {

        { COMPANY_NAME,  QOF_TYPE_STRING, (QofAccessFunc)gncCompanyGetName,  (QofSetterFunc)gncCompanySetName },
        { COMPANY_ADDR,   QOF_TYPE_STRING, (QofAccessFunc)gncCompanyGetAddress, (QofSetterFunc)gncCompanySetAddress },
        { COMPANY_ID,   QOF_TYPE_STRING, (QofAccessFunc)gncCompanyGetId, (QofSetterFunc)gncCompanySetId },
        { COMPANY_PHONE, QOF_TYPE_STRING, (QofAccessFunc)gncCompanyGetPhone, (QofSetterFunc)gncCompanySetPhone },
        { COMPANY_FAX,  QOF_TYPE_STRING, (QofAccessFunc)gncCompanyGetFax, (QofSetterFunc)gncCompanySetFax },
        { COMPANY_WEBSITE, QOF_TYPE_STRING, (QofAccessFunc)gncCompanyGetWebsite, (QofSetterFunc)gncCompanySetWebsite },
        { COMPANY_EMAIL,   QOF_TYPE_STRING, (QofAccessFunc)gncCompanyGetEmail, (QofSetterFunc)gncCompanySetEmail },
        { COMPANY_CONTACTPERSON, QOF_TYPE_STRING, (QofAccessFunc)gncCompanyGetContactperson, (QofSetterFunc)gncCompanySetContactperson },
        { QOF_PARAM_BOOK, QOF_ID_BOOK,   (QofAccessFunc)qof_instance_get_book, NULL },
        { QOF_PARAM_GUID, QOF_TYPE_GUID, (QofAccessFunc)qof_instance_get_guid, NULL },
        { NULL },
    };

    /* qof_class_register (GNC_ID_ADDRESS, (QofSortFunc)gncAddressCompare, params);*/
    /*if (!qof_choice_add_class(GNC_ID_CUSTOMER, GNC_ID_ADDRESS, ADDRESS_OWNER))
    {
        return FALSE;
    }*/

    return qof_object_register(&GncCompanyDesc);
}


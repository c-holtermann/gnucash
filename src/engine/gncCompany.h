/********************************************************************\
* gncCompany.h -- a Company object *
* *
* This program is free software; you can redistribute it and/or *
* modify it under the terms of the GNU General Public License as *
* published by the Free Software Foundation; either version 2 of *
* the License, or (at your option) any later version. *
* *
* This program is distributed in the hope that it will be useful, *
* but WITHOUT ANY WARRANTY; without even the implied warranty of *
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the *
* GNU General Public License for more details. *
* *
* You should have received a copy of the GNU General Public License*
* along with this program; if not, contact: *
* *
* Free Software Foundation Voice: +1-617-542-5942 *
* 51 Franklin Street, Fifth Floor Fax: +1-617-542-2652 *
* Boston, MA 02110-1301, USA gnu@gnu.org *
* *
\********************************************************************/
/** @addtogroup Business */
#ifndef GNC_COMPANY_H_
#define GNC_COMPANY_H_
#include "qof.h"
#ifdef GNUCASH_MAJOR_VERSION
#include "gncBusiness.h"
#endif
#define GNC_COMPANY_MODULE_NAME "gncCompany"
#define GNC_ID_COMPANY GNC_COMPANY_MODULE_NAME
typedef struct _gncCompany GncCompany;
typedef struct _gncCompanyClass GncCompanyClass;

/* --- type macros --- */
#define GNC_TYPE_COMPANY            (gnc_company_get_type ())
#define GNC_COMPANY(o)              \
     (G_TYPE_CHECK_INSTANCE_CAST ((o), GNC_TYPE_COMPANY, GncCompany))
#define GNC_COMPANY_CLASS(k)        \
     (G_TYPE_CHECK_CLASS_CAST((k), GNC_TYPE_COMPANY, GncCompanyClass))
#define GNC_IS_COMPANY(o)           \
     (G_TYPE_CHECK_INSTANCE_TYPE ((o), GNC_TYPE_COMPANY))
#define GNC_IS_COMPANY_CLASS(k)     \
     (G_TYPE_CHECK_CLASS_TYPE ((k), GNC_TYPE_COMPANY))
#define GNC_COMPANY_GET_CLASS(o)    \
     (G_TYPE_INSTANCE_GET_CLASS ((o), GNC_TYPE_COMPANY, GncCompanyClass))
GType gnc_company_get_type(void);

/** @name Create/Destroy functions
 @{ */
GncCompany *gncCompanyCreate (QofBook *book);
void gncCompanyDestroy (GncCompany *company);
void gncCompanyBeginEdit (GncCompany *company);
void gncCompanyCommitEdit (GncCompany *company);

/** @name Set functions
 @{ */

void gncCompanySetName (GncCompany *company, const char *name);
void gncCompanySetAddress (GncCompany *company, const char *address);
void gncCompanySetId (GncCompany *company, const char *id);
void gncCompanySetPhone (GncCompany *company, const char *phone);
void gncCompanySetFax (GncCompany *company, const char *fax);
void gncCompanySetWebsite (GncCompany *company, const char *website);
void gncCompanySetEmail (GncCompany *company, const char *email);
void gncCompanySetContactperson (GncCompany *company, const char *contactperson);

/** @} */


/** @name Get Functions
 @{ */

const char * gncCompanyToString (const GncCompany *company);
QofBook * gncCompanyGetBook (const GncCompany *company);
const char * gncCompanyGetName (const GncCompany *company);
const char * gncCompanyGetAddress (const GncCompany *company);
const char * gncCompanyGetId (const GncCompany *company);
const char * gncCompanyGetPhone (const GncCompany *company);
const char * gncCompanyGetFax (const GncCompany *company);
const char * gncCompanyGetWebsite (const GncCompany *company);
const char * gncCompanyGetEmail (const GncCompany *company);
const char * gncCompanyGetContactperson (const GncCompany *company);

/** @} */

#define COMPANY_NAME    "name"
#define COMPANY_ADDR	"address"
#define COMPANY_ID	"id"
#define COMPANY_PHONE   "phone"
#define COMPANY_FAX	"fax"
#define COMPANY_WEBSITE "website"
#define COMPANY_EMAIL   "email"
#define COMPANY_CONTACTPERSON "contactperson"

#endif

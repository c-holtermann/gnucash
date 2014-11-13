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

struct _gncCompany
{
    QofInstance inst;

    QofBook *	book;
    QofInstance * parent;
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


/*
 * gnucash_core.i -- SWIG interface file for the core parts of GnuCash
 *
 * Copyright (C) 2008 ParIT Worker Co-operative <paritinfo@parit.ca>
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as
 * published by the Free Software Foundation; either version 2 of
 * the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, contact:
 *
 * Free Software Foundation           Voice:  +1-617-542-5942
 * 51 Franklin Street, Fifth Floor    Fax:    +1-617-542-2652
 * Boston, MA  02110-1301,  USA       gnu@gnu.org
 *
 * @author Mark Jenkins, ParIT Worker Co-operative <mark@parit.ca>
 * @author Jeff Green, ParIT Worker Co-operative <jeff@parit.ca>
 */

/** @file
    @brief SWIG interface file for the core parts of GnuCash

        This file is processed by SWIG and the resulting files are gnucash_core.c and gnucash_core_c.py.
        Have a look at the includes to see which parts of the GnuCash source SWIG takes as input.
    @author Mark Jenkins, ParIT Worker Co-operative <mark@parit.ca>
    @author Jeff Green,   ParIT Worker Co-operative <jeff@parit.ca>
    @ingroup python_bindings 

    @file gnucash_core.c
    @brief SWIG output file.
    @ingroup python_bindings
    @file gnucash_core_c.py
    @brief SWIG output file.
    @ingroup python_bindings
*/

%feature("autodoc", "1");
%module(package="gnucash") gnucash_core_c

/* Renaming "from" to "_from" to suppress the swig warning - they stop the make process
/src/libqof/qof/qofinstance-p.h:63: Warning 314: 'from' is a python keyword, renaming to '_from'
*/
%rename(_from) from;

%{
#include "config.h"
#include <datetime.h>
#include "qofsession.h"
#include "qofbook.h"
#include "qofbackend.h"
#include "qoflog.h"
#include "qofutil.h"
#include "qofid.h"
#include "guid.h"
#include "qofquery.h"
#include "qofquerycore.h"
#include "qofinstance.h"
#include "gnc-module/gnc-module.h"
#include "engine/gnc-engine.h"
#include "Transaction.h"
#include "Split.h"
#include "Account.h"
#include "gnc-commodity.h"
#include "gnc-lot.h"
#include "gnc-numeric.h"
#include "gncCustomer.h"
#include "gncCustomerP.h"
#include "gncEmployee.h"
#include "gncVendor.h"
#include "gncVendorP.h"
#include "gncAddress.h"
#include "gncBillTerm.h"
#include "gncOwner.h"
#include "gncInvoice.h"
#include "gncInvoiceP.h"
#include "gncJob.h"
#include "gncEntry.h"
#include "gncTaxTable.h"
#include "gncIDSearch.h"
#include "engine/gnc-pricedb.h"
#include "app-utils/gnc-prefs-utils.h"
#include "kvp-util.h"
#include "kvp-util-p.h"
#include "kvp_frame.h"
#include "qofinstance-p.h"
#include "glib.h"
%}

%include <glib.h>
void g_hash_table_destroy(GHashTable *hash_table);
GList *     g_hash_table_get_keys          (GHashTable     *hash_table);
GList *     g_hash_table_get_values        (GHashTable     *hash_table);
gpointer g_list_nth_data                (GList            *list,
                                         guint             n);

guint    g_list_length                  (GList            *list);
guint    g_slist_length                  (GSList           *list);
gpointer g_slist_nth_data                (GSList           *list,
                                          guint             n);
GSList * g_slist_nth                (GSList           *list,
                                          guint             n);

%include <timespec.i>

%include <base-typemaps.i>

%include <engine-common.i>

%include <qofbackend.h>

// this function is defined in qofsession.h, but isnt found in the libraries,
// ignored because SWIG attempts to link against (to create language bindings)
%ignore qof_session_not_saved;
%include <qofsession.h>

%include <qofbook.h>

%include <qofid.h>

%include <qofquery.h>

%include <qofquerycore.h>

/* SWIG doesn't like this macro, so redefine it to simply mean const */
#define G_CONST_RETURN const
%include <guid.h>

/* %include <Transaction.h>
%include <Split.h>
%include <Account.h> */

//Ignored because it is unimplemented
%ignore gnc_numeric_convert_with_error;
%include <gnc-numeric.h>

%include <gnc-commodity.h>

/* Key value pairs */
//Ignored because it is unimplemented
%ignore qof_instance_set_editlevel;
%ignore kvp_value_binary_append;
%ignore double_compare;

%include <kvp-util.h>
%include <kvp-util-p.h>
%include <kvp_frame.h>


/* QofInstance */
%inline %{
  /* I think this should rather be implemented in python now */
  KvpFrame *qof_book_get_slots (QofBook *book) {
       return qof_instance_get_slots (QOF_INSTANCE (book));
  }

  /* to be removed I guess */
  QofInstance *qof_book_get_qof_instance (QofBook *book) {
        return (QOF_INSTANCE (book));
  }

  /* to be removed I guess */
  gconstpointer *qof_book_get_qof_instance_gconstpointer (QofBook *book) {
        return QOF_INSTANCE (book);
  }
/**
  KvpValue *kvp_frame_get_value_n (KvpFrame *frame, int num) {
        GHashTable *gh;
        gh = kvp_frame_get_hash( frame );
        if (! gh) return NULL;

        GList *gl;
        gl = g_hash_table_get_values( gh );
        if (! gl) return NULL;

        return g_list_nth_data(gl, num);
  }
  
  char *kvp_frame_get_key_n (KvpFrame *frame, int num) {
        GHashTable *gh;
        gh = kvp_frame_get_hash( frame );
        if (! gh) return NULL;
        
        GList *gl;
        gl = g_hash_table_get_keys( gh );
        if (! gl) return NULL;

        return g_list_nth_data(gl, num);
  }

  int kvp_frame_get_length (KvpFrame *frame) {
        GHashTable *gh;
        gh = kvp_frame_get_hash( frame );
        if (! gh) return NULL; 
        
        GList *gl;
        gl = g_hash_table_get_keys( gh ); 
        if (! gl) return NULL;

        return g_list_length( gl );
  }

  PyObject* kvp_frame_get_keys_c (KvpFrame *frame) {
        PyObject *lst = NULL;
        int l_len, i, py_err;
        GHashTable *gh;
        GList *gl;
        PyObject *py_string_tmp;
        
        lst = PyList_New(l_len);
        if (! lst) return NULL;
        
        gh = kvp_frame_get_hash( frame );
        if (! gh) return lst;
        
        gl = g_hash_table_get_keys( gh );
        l_len = g_list_length( gl );
        
        for(i = l_len-1; i >= 0; i--)
        {
                char *k;
                k = g_list_nth_data(gl, i);
                py_string_tmp = PyString_FromString( k );
                
                py_err = PyList_SetItem(lst, i, py_string_tmp);
                if (py_err == -1) return NULL;
        }
        
        return lst;

  }    
*/
  /* Hier gibt's noch Probleme */
  /**
  PyObject *kvp_frame_get_values_c (KvpFrame *frame) {
        GHashTable *gh;
        gh = kvp_frame_get_hash( frame );
        
        GList *gl;
        gl = g_hash_table_get_values( gh );

        PyObject *lst = NULL;
        int l_len, i, py_err;

        l_len = g_list_length( gl );

        lst = PyList_New(l_len);
        if (! lst) return NULL;

        for(i = l_len-1; i >= 0; i--)
        {
                KvpValue *kv;

                kv = g_list_nth_data(gl, i);
                PyObject *o; 
                o = SWIG_NewPointerObj(kv,
                    SWIGTYPE_p_KvpValueType, SWIG_POINTER_OWN);
                 
                py_err = PyList_SetItem(lst, i, o);
                if (py_err == -1) return NULL; 
       */ 
                /* Py_DECREF(o); */
        /**
        }
        return lst;
        
  }*/
%}

/* the following functions use gconstpointer as arguments, make them accept QofInstance pointers */
extern QofBook *qof_instance_get_book (QofInstance *inst);
extern const GncGUID *  qof_instance_get_guid (QofInstance *ent);
extern guint32 qof_instance_get_idata (QofInstance *inst);

%typemap(out) GncOwner * {
    GncOwnerType owner_type = gncOwnerGetType($1);
    PyObject * owner_tuple = PyTuple_New(2);
    PyTuple_SetItem(owner_tuple, 0, PyInt_FromLong( (long) owner_type ) );
    PyObject * swig_wrapper_object;
    if (owner_type == GNC_OWNER_CUSTOMER ){
        swig_wrapper_object = SWIG_NewPointerObj(
	    gncOwnerGetCustomer($1), $descriptor(GncCustomer *), 0);
    }
    else if (owner_type == GNC_OWNER_JOB){
        swig_wrapper_object = SWIG_NewPointerObj(
	    gncOwnerGetJob($1), $descriptor(GncJob *), 0);
    }
    else if (owner_type == GNC_OWNER_VENDOR){
        swig_wrapper_object = SWIG_NewPointerObj(
	    gncOwnerGetVendor($1), $descriptor(GncVendor *), 0);
    }
    else if (owner_type == GNC_OWNER_EMPLOYEE){
        swig_wrapper_object = SWIG_NewPointerObj(
	    gncOwnerGetEmployee($1), $descriptor(GncEmployee *), 0);
    }
    else {
        swig_wrapper_object = Py_None;
	Py_INCREF(Py_None);
    }
    PyTuple_SetItem(owner_tuple, 1, swig_wrapper_object);
    $result = owner_tuple;
}

%typemap(in) GncOwner * {
    GncOwner * temp_owner = gncOwnerNew();
    void * pointer_to_real_thing;
    if ((SWIG_ConvertPtr($input, &pointer_to_real_thing,
                         $descriptor(GncCustomer *),
                         SWIG_POINTER_EXCEPTION)) == 0){
        gncOwnerInitCustomer(temp_owner, (GncCustomer *)pointer_to_real_thing);
        $1 = temp_owner;
    }
    else if ((SWIG_ConvertPtr($input, &pointer_to_real_thing,
                         $descriptor(GncJob *),
                         SWIG_POINTER_EXCEPTION)) == 0){
        gncOwnerInitJob(temp_owner, (GncJob *)pointer_to_real_thing);
        $1 = temp_owner;
    }
    else if ((SWIG_ConvertPtr($input, &pointer_to_real_thing,
                         $descriptor(GncVendor *),
                         SWIG_POINTER_EXCEPTION)) == 0){
        gncOwnerInitVendor(temp_owner, (GncVendor *)pointer_to_real_thing);
        $1 = temp_owner;
    }
    else if ((SWIG_ConvertPtr($input, &pointer_to_real_thing,
                         $descriptor(GncEmployee *),
                         SWIG_POINTER_EXCEPTION)) == 0){
        gncOwnerInitEmployee(temp_owner, (GncEmployee *)pointer_to_real_thing);
        $1 = temp_owner;
    }
    else {
	PyErr_SetString(
	    PyExc_ValueError,
	    "Python object passed to function with GncOwner * argument "
	    "couldn't be converted back to pointer of that type");
        return NULL;
    }
}

%typemap(freearg) GncOwner * {
    gncOwnerFree($1);
}


%include <gnc-lot.h>

//core business includes
%include <gncOwner.h>
%include <gncCustomer.h>
%include <gncCustomerP.h>
%include <gncEmployee.h>
%include <gncVendor.h>
%include <gncVendorP.h>
%include <gncAddress.h>
%include <gncBillTerm.h>
%include <gncInvoice.h>
%include <gncInvoiceP.h>
%include <gncJob.h>
%include <gncEntry.h>
%include <gncTaxTable.h>
%include <gncIDSearch.h>

%include <qofinstance.h>
%include <qofinstance-p.h>

// Commodity prices includes and stuff
%include <gnc-pricedb.h>

/* %inline %{
  
  KvpFrame *xaccTransFrame(const Transaction *trans)
  {
        KvpFrame *frame;
        frame = trans->inst.kvp_data;

        return frame;
  }
%}*/

%init %{
gnc_environment_setup();
qof_log_init();
qof_init();
qof_query_init();
gnc_module_system_init();
char * no_args[1] = { NULL };
gnc_engine_init(0, no_args);
gnc_prefs_init();
%}


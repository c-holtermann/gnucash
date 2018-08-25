%module(package="gnucash") gnucash_core_cc

%include <std_string.i>
%include "stdint.i"

/* rename and ignore for qofsession.hpp */
/* prevent Warning 314: 'from' is a python keyword, renaming to '_from' qofsession.hpp:118 */
%rename(_from) qof_instance_copy_data::from;
/* prevent qofsession.hpp:132: Warning 322: Redundant redeclaration of 'qof_session_get_backend' TODO: refine to only ignore redundancy*/
%ignore qof_session_get_backend;

/* renames and igonres for gnc-numeric.hpp */
/* just so that swig runs without warnings */
/* prevent Warning 503: Can't wrap 'operator ...' unless renamed to a valid identifier. */
%rename(__add__) operator +;
%rename(__sub__) operator -;
%rename(__mul__) operator *;
%rename(__div__) operator /;
%rename(__gt__) operator >;
%rename(__lt__) operator <;
/* make all these type aware variants accessible or ignore them ? */
%rename(_eq_GncNumeric_GncNumeric) operator ==(GncNumeric a, GncNumeric b);
%rename(_eq_GncNumeric_int64) operator ==(GncNumeric a, int64_t b);
%rename(_eq_int64_GncNumeric) operator ==(int64_t a, GncNumeric b);
%rename(__ne__) operator !=;
%rename(__ge__) operator >=;
%rename(__le__) operator <=;
%rename(operator_insert) operator <<;
%rename(operator_double) operator double;
%rename(operator_gnc_numeric) operator gnc_numeric;
/* prevent Warning 362: operator= ignored in lines 142 and 143 */
%ignore GncNumeric::operator=;
/* prevent Warning 509: in lines 140+141 */ 
%ignore GncNumeric::GncNumeric(GncNumeric &&);
%rename(__abs__) GncNumeric::abs;
/* prevent Warning 321: line 180 */
%rename(__reduce__) GncNumeric::reduce;
%rename(__cmp__) GncNumeric::cmp;
%rename(_cmp_GncNumeric_GncNumeric) cmp(GncNumeric a, GncNumeric b);
%rename(_cmp_GncNumeric_int64) cmp(GncNumeric a, int64_t b);
%rename(_cmp_int64_GncNumeric) cmp(int64_t a, GncNumeric b);

%{
  #include <string>
  #include "gnc-rational.hpp"
  #include "gnc-rational-rounding.hpp"
  #include "gnc-numeric.hpp"
  #include "qofsession.h"
  #include "qofsession.hpp"
  #include "qof-backend.hpp"
%}

%include <gnc-rational-rounding.hpp>
%include <gnc-numeric.hpp>

%ignore save_in_progress;
%ignore qof_session_get_book_id;
%include <qofsession.h>

%include <qof-backend.hpp>

%include <qofsession.hpp>

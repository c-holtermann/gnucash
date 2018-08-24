%module(package="gnucash") gnucash_core_cc

%include <std_string.i>

/* renames for qofsession.hpp */
/* prevent Warning 314: 'from' is a python keyword, renaming to '_from' qofsession.hpp:118 */
%rename(_from) qof_instance_copy_data::from;
/* prevent qofsession.hpp:132: Warning 322: Redundant redeclaration of 'qof_session_get_backend' TODO: refine to only ignore redundancy*/
%ignore qof_session_get_backend;

/* renames and igonres for gnc-numeric.hpp */
/* prevent Warning 503: Can't wrap 'operator ...' unless renamed to a valid identifier. */
%rename(operator_plus) operator +;
%rename(operator_minus) operator -;
%rename(operator_multiply) operator *;
%rename(operator_divide) operator /;
%rename(operator_greater) operator >;
%rename(operator_smaller) operator <;
%rename(operator_equals) operator ==;
%rename(operator_inequal) operator !=;
%rename(operator_greaterequal) operator >=;
%rename(operator_smallerequal) operator <=;
%rename(operator_insert) operator <<;
%rename(operator_double) operator double;
%rename(operator_gnc_numeric) operator gnc_numeric;
/* prevent Warning 362: operator= ignored in lines 142 and 143 */
%ignore GncNumeric::operator=;
/* prevent Warning 509: in lines 140+141 */ 
%ignore GncNumeric::GncNumeric(GncNumeric &&);

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

%module(package="gnucash") gnucash_core_cc

%include <std_string.i>
%include "stdint.i"

/* rename and ignore for qofsession.hpp */
/* prevent Warning 314: 'from' is a python keyword, renaming to '_from' qofsession.hpp:118 */
%rename(_from) qof_instance_copy_data::from;
/* prevent qofsession.hpp:132: Warning 322: Redundant redeclaration of 'qof_session_get_backend' TODO: refine to only ignore redundancy*/
%ignore qof_session_get_backend;

/* renames and ignores for gnc-numeric.hpp */
/* for the moment just so that swig runs without warnings */
/* TODO: go through all gnc-numeric.hpp and check what is good to wrap */
/* TODO: implement arithmetics etc. with GncNumeric */
/* TODO: implement arithmetics etc. with floats for convenience in python */
/* TODO: check what needs to implement on python side to have a solid arithmetic type */

/* GncNumeric is already the name for the python wrapper for gnc_numeric */
%rename(GncNumericCC) GncNumeric;

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
%rename(to_gnc_numeric) operator gnc_numeric;
/* prevent Warning 362: operator= ignored in lines 142 and 143 */
%ignore GncNumeric::operator=;
/* prevent Warning 509: in lines 140+141 */ 
%ignore GncNumeric::GncNumeric(GncNumeric &&);
%rename(__str__) GncNumeric::to_string;
%rename(__abs__) GncNumeric::abs;
/* prevent Warning 321: line 180 */
%rename(__reduce__) GncNumeric::reduce;
%rename(_cmp) GncNumeric::cmp;
%rename(_cmp_GncNumeric_GncNumeric) cmp(GncNumeric a, GncNumeric b);
%rename(_cmp_GncNumeric_int64) cmp(GncNumeric a, int64_t b);
%rename(_cmp_int64_GncNumeric) cmp(int64_t a, GncNumeric b);

%extend GncNumeric {
public:
                bool __eq__(GncNumeric b) {
                        return *self == b;
                }

                bool __eq__(int64_t b) {
                        return *self == b;
                }

                bool __ne__(GncNumeric b) {
                        return *self != b;
                }

                bool __ne__(int64_t b) {
                        return *self != b;
                }

                bool __lt__(GncNumeric b) {
                        return *self < b;
                }

                bool __lt__(int64_t b) {
                        return *self < b;
                }
                
                bool __gt__(GncNumeric b) {
                        return *self > b;
                }

                bool __gt__(int64_t b) {
                        return *self > b;
                }
                
                bool __le__(GncNumeric b) {
                        return *self <= b;
                }

                bool __le__(int64_t b) {
                        return *self <= b;
                }
                
                bool __ge__(GncNumeric b) {
                        return *self >= b;
                }

                bool __ge__(int64_t b) {
                        return *self >= b;
                }

                GncNumeric __add__(GncNumeric b) {
                        return *self + b;
                }

                GncNumeric __add__(int64_t b) {
                        return *self + b;
                }
                
                GncNumeric __sub__(GncNumeric b) {
                        return *self - b;
                }

                GncNumeric __sub__(int64_t b) {
                        return *self - b;
                }

                GncNumeric __mul__(GncNumeric b) {
                        return *self * b;
                }

                GncNumeric __mul__(int64_t b) {
                        return *self * b;
                }
                
                /* div is Python 2.0 only */
                GncNumeric __div__(GncNumeric b) {
                        return *self / b;
                }

                GncNumeric __div__(int64_t b) {
                        return *self / b;
                } /* div is Python 2.0 only */
        
                GncNumeric __truediv__(GncNumeric b) {
                        return *self / b;
                }

                GncNumeric __truediv__(int64_t b) {
                        return *self / b;
                }

                GncNumeric __floordiv__(GncNumeric b) {
                        return *self / b;
                }

                GncNumeric __floordiv__(int64_t b) {
                        return *self / b;
                }

                /* not implemented ?
                GncNumeric __mod__(GncNumeric b) {
                        return *self % b;
                }

                GncNumeric __mod__(int64_t b) {
                        return *self % b;
                }*/
       
                /* __repr__ shall show the same as __str__ */ 
                std::string __repr__() {
                        return self->to_string();
                }
};

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

%module(package="gnucash") gnucash_core_cc

%include <std_string.i>
%include "stdint.i"
%include <std_except.i>


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
/* TODO: to_decimal is broken when needs to round when shouldn't and tries to throw error 'std::domain_error', including std_except.i doesn't solve this*/

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
%rename(__float__) GncNumeric::operator double;
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

/* TODO: does it make sense to inline these ? */
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

/* TODO: join with gnc-numeric-stuff from above */
%template(convert_round_half_up) GncNumeric::convert<RoundType::half_up>;
%template(convert_round_never) GncNumeric::convert<RoundType::never>;
%template(convert_sigfigs_round_half_up) GncNumeric::convert_sigfigs<RoundType::half_up>;
%template(convert_sigfigs_round_never) GncNumeric::convert_sigfigs<RoundType::never>;

%extend GncNumeric {
public:
        int64_t __int__() {
                return self->convert<RoundType::half_up>(1);
        }

        double __round_digits__(int64_t ndigits) {
                return self->convert_sigfigs<RoundType::half_up>(ndigits);
        }

        int64_t __round_nodigits__() {
                return self->convert_sigfigs<RoundType::half_up>(1);
        }

        int64_t __trunc__() {
                return self->convert<RoundType::truncate>(1);
        }

        int64_t __floor__() {
                return self->convert<RoundType::floor>(1);
        }

        int64_t __ceil__() {
                return self->convert<RoundType::ceiling>(1);
        }
        
        %pythoncode %{
         __swig_getmethods__["denominator"] = denom
         __swig_getmethods__["numerator"] = num
         if _newclass: 
                 denominator = property(denom)
                 numerator = property(num)

        /* TODO: Should __round__ return an int if rounding leads to an int (with ndigits present) ? */
         def __round__(self, *args):
                if len(args) == 1:
                        return self.__round_digits__(args[0])
                else:
                        return self.__round_nodigits__()
        %}
}

%ignore save_in_progress;
%ignore qof_session_get_book_id;
%include <qofsession.h>

%include <qof-backend.hpp>

%include <qofsession.hpp>



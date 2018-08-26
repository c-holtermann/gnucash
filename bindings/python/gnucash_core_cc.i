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

%pythoncode %{
        from fractions import Fraction
        import numbers
        import gnucash
%}

/* TODO: does it make sense to inline some of these ? */
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

        GncNumeric __add_cc__(GncNumeric b) {
                return *self + b;
        }

        GncNumeric __add_cc__(int64_t b) {
                return *self + b;
        }
        
        GncNumeric __sub_cc__(GncNumeric b) {
                return *self - b;
        }

        GncNumeric __sub_cc__(int64_t b) {
                return *self - b;
        }

        GncNumeric __mul_cc__(GncNumeric b) {
                return *self * b;
        }

        GncNumeric __mul_cc__(int64_t b) {
                return *self * b;
        }
        
        /* div is Python 2.0 only */
        GncNumeric __div_cc__(GncNumeric b) {
                return *self / b;
        }

        GncNumeric __div_cc__(int64_t b) {
                return *self / b;
        } /* div is Python 2.0 only */

        GncNumeric __truediv_cc__(GncNumeric b) {
                return *self / b;
        }

        GncNumeric __truediv_cc__(int64_t b) {
                return *self / b;
        }

        GncNumeric __floordiv_cc__(GncNumeric b) {
                return *self / b;
        }

        GncNumeric __floordiv_cc__(int64_t b) {
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

         # TODO: Should __round__ return an int if rounding leads to an int representable value (with ndigits present) or always a float ?
         def __round__(self, *args):
                if len(args) == 1:
                        return self.__round_digits__(args[0])
                else:
                        return self.__round_nodigits__()

         def __add__(self, other):
                if isinstance(other, (GncNumericCC, int)):
                        return self.__add_cc__(other)
                elif type(other) == float:
                        return self.__add_cc__(GncNumericCC(other))
                else:
                        return NotImplemented

         # from https://docs.python.org/3/library/numbers.html#numbers.Integral
         # and https://github.com/python/cpython/blob/3.7/Lib/fractions.py
         def _operator_fallbacks(monomorphic_operator, fallback_operator):
            def forward(a, b):
                if isinstance(b, (int, GncNumericCC)):
                    return monomorphic_operator(a, b)
                elif isinstance(b, gnucash.GncNumeric):
                    return monomorphic_operator(a, GncNumericCC(b.num(), b.denom()))
                elif isinstance(b, Fraction):
                    return monomorphic_operator(a, GncNumericCC(b.numerator, b.denominator))
                elif isinstance(b, float):
                    return monomorphic_operator(a, GncNumericCC(b))
                elif isinstance(b, complex):
                    return fallback_operator(complex(a), b)
                else:
                    return NotImplemented
            forward.__name__ = '__' + fallback_operator.__name__ + '__'
            forward.__doc__ = monomorphic_operator.__doc__

            def reverse(b, a):
                if isinstance(a, Fraction):
                    return fallback_operator(a, Fraction(b.numerator, b.denominator))
                elif isinstance(a, numbers.Rational):
                    # Includes ints.
                    return monomorphic_operator(a, b)
                elif isinstance(a, gnucash.GncNumeric):
                    temp = monomorphic_operator(GncNumericCC(a.num(), a.denom()), b)
                    return gnucash.GncNumeric(temp.numerator, temp.denominator)
                elif isinstance(a, numbers.Real):
                    return fallback_operator(float(a), float(b)) 
                elif isinstance(a, numbers.Complex):
                    return fallback_operator(complex(a), complex(b))
                else:
                    return NotImplemented
            reverse.__name__ = '__r' + fallback_operator.__name__ + '__'
            reverse.__doc__ = monomorphic_operator.__doc__

            return forward, reverse

         import operator

         __add__, __radd__ = _operator_fallbacks(__add_cc__, operator.add)
         __iadd__ = __add__
         __sub__, __rsub__ = _operator_fallbacks(__sub_cc__, operator.sub)
         __isub__ = __sub__
         __mul__, __rmul__ = _operator_fallbacks(__mul_cc__, operator.mul)
         __imul__ = __mul__
         __truediv__, __rtruediv__ = _operator_fallbacks(__div_cc__, operator.truediv)
         __itruediv__ = __truediv__
         __floordiv__, __rfloordiv__ = _operator_fallbacks(__div_cc__, operator.floordiv)
        %}
}

%ignore save_in_progress;
%ignore qof_session_get_book_id;
%include <qofsession.h>

%include <qof-backend.hpp>

%include <qofsession.hpp>



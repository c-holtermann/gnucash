%module(package="gnucash") gnucash_core_cc

%{
  #include <string>
  #include "gnc-rational.hpp"
  #include "gnc-rational-rounding.hpp"
  #include "gnc-numeric.hpp"
  #include "qofsession.h"
  #include "qofsession.hpp"
%}

%include <std_string.i>

%include <gnc-rational-rounding.hpp>
%include <gnc-numeric.hpp>

%ignore save_in_progress;
%ignore qof_session_get_book_id;
%include <qofsession.h>

%include <qofsession.hpp>

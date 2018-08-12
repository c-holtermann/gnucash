%module(package="gnucash") gnucash_core_cc

%{
  #include <string>
  #include "gnc-numeric.hpp"
  #include "qofsession.h"
  #include "qofsession.hpp"
%}

/* %include <gnc-numeric.hpp> */

%ignore save_in_progress;
%ignore qof_session_get_book_id;
%include <qofsession.h>

%include <qofsession.hpp>

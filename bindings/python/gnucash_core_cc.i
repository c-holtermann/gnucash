%module(package="gnucash") gnucash_core_cc

%include <std_string.i>

%rename(_from) from; // qofsession:118 qof_instance_copy_data.from -> qof_instance_copy_data._from as from is reserved keyword in python

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

#! /usr/bin/env python3
#
# Adapted from:
#
# Backend to the console plugin.
# @author: Eitan Isaacson
# @organization: IBM Corporation
# @copyright: Copyright (c) 2007 IBM Corporation
# @license: BSD
#
# All rights reserved. This program and the accompanying materials are made 
# available under the terms of the BSD which accompanies this distribution, and 
# is available at U{http://www.opensource.org/licenses/bsd-license.php}
#

import os
import sys
import re
from io import StringIO
from pkg_resources import parse_version
try:
    import IPython
    from IPython import get_ipython
except Exception as e:
    raise "Error importing IPython (%s)" % str(e)


# ------------------------------------------------------------------ class Shell
class Shell:
    """ """

    def __init__(self,argv=None,user_ns=None,user_global_ns=None,
                 cin=None, cout=None,cerr=None, input_func=None):
        """ """
        io = IPython.utils.io
        if input_func:
            IPython.iplib.raw_input_original = input_func
        if cin:
            io.stdin = io.IOStream(cin)
        if cout:
            io.stdout = io.IOStream(cout)
        if cerr:
            io.stderr = io.IOStream(cerr)
        if argv is None:
            argv=[]
        io.raw_input = lambda x: None
        os.environ['TERM'] = 'dumb'
        excepthook = sys.excepthook
        self.IP = IPython.Shell.make_IPython(argv,
                                             user_ns=user_ns,
                                             user_global_ns=user_global_ns,
                                             embedded=True,
                                             shell_class=IPython.Shell.InteractiveShell)
        self.IP.system = lambda cmd: self.shell(self.IP.var_expand(cmd),
                                                header='IPython system call: ',
                                                verbose=self.IP.rc.system_verbose)
        # Get a hold of the public IPython API object and use it
        self.ip = get_ipython()
        self.ip.magic('colors LightBG')                
        sys.excepthook = excepthook
        self.iter_more = 0
        self.complete_sep =  re.compile('[\s\{\}\[\]\(\)]')


    def namespace(self):
        return self.IP.user_ns

    def eval(self, console):
        console.write ('\n')
        orig_stdout = sys.stdout
        sys.stdout = IPython.utils.io.stdout
        try:
            line = self.IP.raw_input(None, self.iter_more)
            if self.IP.autoindent:
                self.IP.readline_startup_hook(None)
        except KeyboardInterrupt:
            self.IP.write('\nKeyboardInterrupt\n')
            self.IP.resetbuffer()
            self.IP.outputcache.prompt_count -= 1
            if self.IP.autoindent:
                self.IP.indent_current_nsp = 0
            self.iter_more = 0
        except:
            self.IP.showtraceback()
        else:
            self.iter_more = self.IP.push(line)
            if (self.IP.SyntaxTB.last_syntax_error and self.IP.rc.autoedit_syntax):
                self.IP.edit_syntax_error()
        if self.iter_more:
            self.prompt = str(self.IP.outputcache.prompt2).strip()
            if self.IP.autoindent:
                self.IP.readline_startup_hook(self.IP.pre_readline)
        else:
            self.prompt = str(self.IP.outputcache.prompt1).strip()
        sys.stdout = orig_stdout

        # System output (if any)
        while True:
            try:
                buf = os.read(console.piperead, 256)
            except:
                break
            else:
                console.write (buf)
            if len(buf) < 256: break

        # Command output
        rv = console.cout.getvalue()
        if rv:
            rv = rv.strip('\n')
        console.write (rv)
        if rv:
            console.write ('\n')
        console.cout.truncate(0)
        console.prompt()

    def complete(self, line):
        split_line = self.complete_sep.split(line)
        possibilities = self.IP.complete(split_line[-1])
        if possibilities:
            common_prefix = os.path.commonprefix (possibilities)
            completed = line[:-len(split_line[-1])]+common_prefix
        else:
            completed = line
        return completed, possibilities

    def shell(self, cmd,verbose=0,debug=0,header=''):
        stat = 0
        if verbose or debug: print(header+cmd)
        if not debug:
            input, output = os.popen4(cmd)
            print(output.read())
            output.close()
            input.close()


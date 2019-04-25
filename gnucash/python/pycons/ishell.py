#! /usr/bin/env python3
#
# Adapted from:
#
# Backend to the console plugin.
# @author: Eitan Isaacson
# @organization: IBM Corporation
# @copyright: Copyright (c) 2007 IBM Corporation
# @license: BSD
# updates: https://dev.gajim.org/gajim/gajim/commit/c3eba4037e902280436fe5afd8df22e1289e1f33
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
            if parse_version(IPython.release.version) >= parse_version("1.2.1"):
                 IPython.terminal.interactiveshell.raw_input_original = input_func
            else:
                 IPython.frontend.terminal.interactiveshell.raw_input_original = input_func
        if cin:
            io.stdin = io.IOStream(cin)
        if cout:
            io.stdout = io.IOStream(cout)
        if cerr:
            io.stderr = io.IOStream(cerr)
        if argv is None:
            argv=[]
        io.raw_input = lambda x: None
        
        # self.term = IPython.genutils.IOTerm(cin=cin, cout=cout, cerr=cerr)
        
        os.environ['TERM'] = 'dumb'
        excepthook = sys.excepthook

        from traitlets.config import Config
        cfg = Config()
        cfg.InteractiveShell.colors = "Linux"

        old_stdout, old_stderr = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = io.stdout.stream, io.stderr.stream

        try:
          if parse_version(IPython.release.version) >= parse_version("1.2.1"):
            self.IP = IPython.terminal.embed.InteractiveShellEmbed(config=cfg, user_ns=user_ns)
          else:
            self.IP = IPython.frontend.terminal.embed.InteractiveShellEmbed.instance(\
                   config=cfg, user_ns=user_ns, user_global_ns=user_global_ns)
           
        except:
            print("ERR")

        sys.stdout, sys.stderr = old_stdout, old_stderr

        #self.IP = IPython.Shell.make_IPython(argv,
        #                                     user_ns=user_ns,
        #                                     user_global_ns=user_global_ns,
        #                                     embedded=True,
        #                                     shell_class=IPython.Shell.InteractiveShell)
        
        
        self.IP.system = lambda cmd: self.shell(self.IP.var_expand(cmd),
                                                header='IPython system call: ',
                                                #verbose=self.IP.rc.system_verbose,
                                                local_ns=user_ns)
        self.IP.raw_input = input_func
        
        # Get a hold of the public IPython API object and use it
        self.ip = self.IP.get_ipython()
        self.ip.magic('colors LightBG')                
        
        sys.excepthook = excepthook
        self.iter_more = 0
        self.complete_sep =  re.compile('[\s\{\}\[\]\(\)]')

    def namespace(self):
        return self.IP.user_ns

    def eval(self, console):
        console.write ('\n')
        # print("eval:")
        orig_stdout = sys.stdout
        if parse_version(IPython.release.version) <= parse_version("5.0"):
            sys.stdout = IPython.utils.io.stdout
            sys.stdin = IPython.utils.io.stdin
       
        #console.write("orig_stdout: "+str(orig_stdout)+'\n')
        #console.write("sys.stdout: "+str(sys.stdout)+'\n')

        orig_stdin = sys.stdin
        
        self.prompt = self.generatePrompt(self.iter_more)

        self.IP.hooks.pre_prompt_hook()
        if self.iter_more:
            try:
                self.prompt = self.generatePrompt(True)
            except:
                print("ERR - generatePrompt")
                self.IP.showtraceback()
            if self.IP.autoindent:
                self.IP.rl_do_indent = True

        try:
            line = self.IP.raw_input(self.prompt)
        except KeyboardInterrupt:
            self.IP.write('\nKeyboardInterrupt\n')
            self.IP.input_splitter.reset()
        except:
            import traceback
            self.IP.write('\nERR\n'+traceback.format_exc()+'\n')
            self.IP.showtraceback()
            self.IP.write('\n')
        else:
            # print("line:", line)
            self.IP.input_splitter.push(line)
            self.iter_more = self.IP.input_splitter.push_accepts_more()
            self.prompt = self.generatePrompt(self.iter_more)
            if (self.IP.SyntaxTB.last_syntax_error and self.IP.autoedit_syntax):
                self.IP.edit_syntax_error()
            if not self.iter_more:
                if parse_version(IPython.release.version) >= parse_version("2.0.0-dev"):
                    source_raw = self.IP.input_splitter.raw_reset()
                else:
                    source_raw = self.IP.input_splitter.source_raw_reset()[1]

                #source_raw = self.IP.input_splitter.source_raw
                # credits: https://github.com/ipython/ipython/blob/master/docs/source/whatsnew/version2.0.rst
                # print("source_raw:", source_raw)
                self.IP.run_cell(source_raw, store_history=True)
                self.IP.rl_do_indent = False
            else:
                # TODO: Auto-indent
                self.IP.rl_do_indent = True
                pass
            
        sys.stdout = orig_stdout
        sys.stdin = orig_stdin


        # System output (if any)
        while True:
            try:
                buf = os.read(console.piperead, 256)
            except:
                # print("error while reading console.piperead")
                # import traceback
                # self.IP.write('\nERR\n'+traceback.format_exc()+'\n')
                # self.IP.showtraceback()
                # self.IP.write('\n')
                break
            else:
                # print(buf)
                console.write (buf.decode('utf-8'))
            if len(buf) < 256: break

        
        # Command output
        rv = console.cout.getvalue()
        # print("console.cout.getvalue():", rv)
        
        if rv:
            rv = rv.strip('\n')
        console.write (rv)
        if rv:
            console.write ('\n')
        console.cout.truncate(0)
        console.prompt()

    def generatePrompt(self, is_continuation):
        '''
        Generate prompt depending on is_continuation value

        @param is_continuation
        @type is_continuation: boolean 

        @return: The prompt string representation
        @rtype: string

        '''

        # Backwards compatibility with ipython-0.11
        #
        ver = IPython.__version__
        if '0.11' in ver:
          prompt = self.IP.hooks.generate_prompt(is_continuation)
        elif parse_version(IPython.release.version) < parse_version("5.0.0"):
          if is_continuation:
            prompt = self.IP.prompt_manager.render('in2')
          else:
            prompt = self.IP.prompt_manager.render('in')
        else:
            # thanks to https://gitlab.gnome.org/GNOME/accerciser/commit/5a3242b4c7f5a5c844a20821881d68d1cabcae1e
            # TODO: update to IPython 5.x and later
            prompt = "In [%d]: " % self.IP.execution_count
        return prompt

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


#! /usr/bin/env python3
#
# Copyright (c) 2008, Nicolas Rougier
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the University of California, Berkeley nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE AUTHOR AND CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import sys
import re
import tempfile
import readline
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import Pango
import io
import pycons.shell as shell
#try:    
import pycons.ishell as ishell
#except: pass

ansi_colors =  {'0;30': '#2E3436',
                '0;31': '#CC0000',
                '0;32': '#4E9A06',
                '0;33': '#C4A000',
                '0;34': '#3465A4',
                '0;35': '#75507B',
                '0;36': '#06989A',
                '0;37': '#D3D7CF',
                '1;30': '#555753',
                '1;31': '#EF2929',
                '1;32': '#8AE234',
                '1;33': '#FCE94F',
                '1;34': '#729FCF',
                '1;35': '#AD7FA8',
                '1;36': '#34E2E2',
                '1;37': '#EEEEEC'}

# ------------------------------------------------------------- class ConsoleOut
class ConsoleOut:
    """
    A fake output file object.  It sends output to the console widget,
    and if asked for a file number, returns one set on instance creation
    """
    
    def __init__(self, console, fn=-1, style=None):
        self.fn = fn
        self.console = console
        self.style = style
    def close(self): pass
    flush = close
    def fileno(self):    return self.fn
    def isatty(self):    return False
    def read(self, a):   return ''
    def readline(self):  return ''
    def readlines(self): return []
    def write(self, s):
        self.console.write (s, self.style)
    def writelines(self, l):
        for s in l:
            self.console.write (s, self.style)
    def seek(self, a):   raise IOError(29, 'Illegal seek')
    def tell(self):      raise IOError(29, 'Illegal seek')
    truncate = tell


# -------------------------------------------------------------- class ConsoleIn
class ConsoleIn:
    """
    A fake input file object.  It receives input from a GTK TextView widget,
    and if asked for a file number, returns one set on instance creation
    """
    def __init__(self, console, fn=-1):
        self.fn = fn
        self.console = console
    def close(self): pass
    flush = close
    def fileno(self):    return self.fn
    def isatty(self):    return False
    def read(self, a):   return self.readline()
    def readline(self):
        self.console.input_mode = True
        buffer = self.console.buffer
        #console.write('\n')
        iter = buffer.get_iter_at_mark(buffer.get_insert())
        buffer.move_mark (buffer.get_mark('linestart'), iter)
        while self.console.input_mode:
            #while Gtk.events_pending():
            Gtk.main_iteration()
        s = self.console.input
        self.console.input = ''
        return s+'\n'
    def readlines(self): return []
    def write(self, s):  return None
    def writelines(self, l): return None
    def seek(self, a):   raise IOError(29, 'Illegal seek')
    def tell(self):      raise IOError(29, 'Illegal seek')
    truncate = tell


# ---------------------------------------------------------------- class Console
class Console (Gtk.ScrolledWindow):
    """ GTK python console """

    def __init__(self, argv=[], shelltype='python', banner=[],
                 filename=None, size=100):

        """ Console interface building + initialization"""

        # GTK interface
        self.do_quit = False
        GObject.GObject.__init__(self)
        self.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.set_shadow_type (Gtk.ShadowType.NONE)
        self.set_border_width(0)
        self.view = Gtk.TextView()
        self.view.modify_font (Pango.FontDescription("Mono 10"))
        self.view.set_editable (True)
        self.view.set_wrap_mode(True)
        self.view.set_left_margin(0)
        self.view.set_right_margin(0)
        self.buffer = self.view.get_buffer()
        self.buffer.create_tag ('title',
                                indent = 2,
                                weight=Pango.Weight.BOLD,
                                foreground='blue',
                                font='Mono 12')
        self.buffer.create_tag ('subtitle',
                                indent = 2,
                                foreground='blue',
                                font='Mono 8')
        self.buffer.create_tag ('output',
                                foreground = 'blue',
                                font='Mono 10')
        self.buffer.create_tag ('error',
                                foreground='red',
                                style=Pango.Style.OBLIQUE,
                                font='Mono 10')
        self.buffer.create_tag ('prompt',
                                foreground='blue',
                                weight=Pango.Weight.BOLD,
                                font='Mono 10')
        self.buffer.create_tag('0')
        self.color_pat = re.compile('\x01?\x1b\[(.*?)m\x02?')
        self.color_pat_simple = re.compile('([01]);([34])([0-7]).*')
        self.color_pat_8bit = re.compile('([01]);([34])[8];5;([0-7]*).*')
        self.control_pat = re.compile('\x01?\x1b\[[\x30-\x3f]*[\x20-\x2f0-7;:]+h\x02?')
        for code in ansi_colors:
            self.buffer.create_tag(code,
                                   foreground=ansi_colors[code],
                                   weight=700)
        for text, style in banner:
            self.write (text, style)
        iter = self.buffer.get_iter_at_mark(self.buffer.get_insert())
        self.buffer.create_mark ('linestart', iter, True)
        self.view.add_events(Gdk.EventMask.KEY_PRESS_MASK)
        self.view.connect ('key-press-event', self.key_press_event)
        self.add(self.view)
        self.show_all()
        self.killbuffer = None

        # Console stuff
        self.argv = argv
        self.history_init(filename, size)
        self.cout = io.StringIO()
        self.cout.truncate(0)

        if shelltype=='ipython':
            self.shell = ishell.Shell(argv,locals(),globals(),
                                cout=self.cout, cerr=self.cout,
                                input_func=self.raw_input)
        else:
            self.shell = shell.Shell(locals(),globals())
        self.interrupt = False
        self.input_mode = False
        self.input = None
        self.stdout = ConsoleOut (self, sys.stdout.fileno(), 'output')
        self.stdout_bak = self.stdout
        self.stderr = ConsoleOut (self, sys.stderr.fileno(), 'error')
        self.stderr_bak = self.stderr
        self.stdin  = ConsoleIn  (self, sys.stdin.fileno())

        # Create a named pipe for system stdout/stderr redirection
        self.fifoname = tempfile.mktemp()
        if not os.path.exists (self.fifoname):
            os.mkfifo (self.fifoname)
        self.piperead  = os.open (self.fifoname, os.O_RDONLY | os.O_NONBLOCK)
        self.pipewrite = os.open (self.fifoname, os.O_WRONLY | os.O_NONBLOCK)
        self.shell.eval(self)
        self.cout.truncate(0)

    def history_init(self, filename, size):
        self.history_file = filename
        self.history_size = size
        if filename and os.path.exists(filename):
            readline.read_history_file(filename)
        readline.set_history_length(size)
        self.history_reset()

    def history_save(self):
        if self.history_file:
            readline.write_history_file(self.history_file)

    def history_add(self, item):
        if len(item):
            readline.add_history (item)
        self.history_reset()

    def history_reset(self):
        self.history_index = readline.get_current_history_length()+1

    def history_next(self):
        self.history_index += 1
        if self.history_index <= readline.get_current_history_length():
            return '' or readline.get_history_item (self.history_index)
        self.history_index = readline.get_current_history_length()+1
        return ''

    def history_prev(self):
        if self.history_index > 1:
            self.history_index -= 1
        else:
            self.history_index = 1
        return '' or readline.get_history_item (self.history_index)

    def raw_input(self, prompt=''):
        if self.interrupt:
            self.interrupt = False
            raise KeyboardInterrupt
        return self.last_line()

    def grab_focus (self):
        """ Give focus to the TextView """

        self.view.grab_focus()

    def write (self, text, style=None):
        """ Write text using given style (if any) """
        print("write")
        
        control_patterns = re.findall(self.control_pat, text)
        if control_patterns:
            # print("remove control patterns: "+str(control_patterns))
            text = re.sub(self.control_pat, '', text) # remove control patterns
        
        segments = self.color_pat.split(text)
        segment = segments.pop(0)
        start,end = self.buffer.get_bounds()
        if style==None:
            self.buffer.insert(end, segment)
        else:
            self.buffer.insert_with_tags_by_name(end, segment, style)
        if segments:
            ansi_tags = self.color_pat.findall(text)
            for tag in ansi_tags:
                i = segments.index(tag)
                
                #print('\ntag: "'+tag+", text: '"+segments[i+1]+"'")
                #print("simple color:", self.color_pat_simple.match(tag))
                
                if self.color_pat_8bit.match(tag):
                    
                    #print("8bit color:", self.color_pat_8bit.findall(tag))
                    p1, fgbg, color = self.color_pat_8bit.findall(tag)[0]
                    
                    color_int_raw = int(color)
                    #print(color_int_raw)
                    if color_int_raw > 15:
                        color_int = color_int_raw - 16
                        r6 = color_int // 36
                        r = r6 / 6
                        g6 = (color_int % 36) // 6
                        g = g6 / 6
                        b6 = (color_int % 6)
                        b = b6 / 6
                        #print(r,g,b)
                    
                        colorRGBA = Gdk.RGBA(r,g,b,1)

                        #print(colorRGBA)

                        try:
                            end_iter = self.buffer.get_end_iter()
                            tag_temp_name = 'rgba%0.2X%0.2X%0.2X%0.2X' % (int(r*0xFF),int(g*0xFF),int(b*0xFF),int(1.0*0xFF)) 
                            tag_temp = self.buffer.get_tag_table().lookup(tag_temp_name)
                            if not tag_temp:
                              tag_temp = self.buffer.create_tag (tag_temp_name, foreground_rgba=colorRGBA)
                            self.buffer.insert_with_tags(end_iter,segments[i+1], tag_temp)
                        except:
                            import traceback
                            traceback.print_exc()
                    
                    
                    elif color_int_raw >= 0:
                        if color_int_raw < 8:
                            color_code_ansi = "0;3"+str(color_int_raw)
                        else:
                            color_code_ansi = "1;3"+str(color_int_raw-8)
                    
                        #print(color_code_ansi)

                        try:
                            self.buffer.insert_with_tags_by_name(self.buffer.get_end_iter(),
                                                                segments[i+1], color_code_ansi)
                        except:
                            import traceback
                            traceback.print_exc()
                    else:
                        pass # illegal color code

                #try:
                #    self.buffer.insert_with_tags_by_name(self.buffer.get_end_iter(),
                #                                            segments[i+1], tag)
                #except:
                #    import traceback
                #    traceback.print_exc()
                segments.pop(i)
        self.view.scroll_mark_onscreen(self.buffer.get_insert())

    def overwrite (self, text, style=None):
        """ Overwrite text after prompt with text """

        mark = self.buffer.get_mark('linestart')
        start = self.buffer.get_iter_at_mark(mark)
        end = self.buffer.get_end_iter()
        self.buffer.delete (start,end)
        self.write (text, style)

    def last_line (self):
        """ Get last line (without prompt) """
        
        mark = self.buffer.get_mark('linestart')
        start = self.buffer.get_iter_at_mark(mark)
        end = self.buffer.get_end_iter()
        return self.buffer.get_text (start,end,True)


    def prompt (self, style=None):
        """ Display prompt """

        iter = self.buffer.get_end_iter()
        self.buffer.place_cursor (iter)
        self.write (self.shell.prompt, style)
        iter = self.buffer.get_iter_at_mark(self.buffer.get_insert())
        self.buffer.move_mark (self.buffer.get_mark('linestart'), iter)
        self.history_reset()
        self.view.scroll_mark_onscreen(self.buffer.get_insert())
        while Gtk.events_pending():
            Gtk.main_iteration()

    def key_press_event (self, widget, event):
        """ Handle key press event """

        keyname = Gdk.keyval_name (event.keyval)

        # New command
        if keyname in ['Return', 'KP_Enter']:
            line = self.last_line()
            self.history_add (line)
            if self.input_mode:
                self.input_mode = False
                self.input = self.last_line()
                self.write('\n')
            else:
                self.execute()
            return True

        # Prevent cursor to go back past prompt
        elif keyname in ['Left', 'BackSpace']:
            mark = self.buffer.get_mark('linestart')
            linestart = self.buffer.get_iter_at_mark(mark)
            iter = self.buffer.get_iter_at_mark(self.buffer.get_insert())
            if iter.compare(linestart) <= 0:
                return True

        elif keyname == 'Right':
            return False
        
        # Next history item
        elif keyname == 'Down':
            self.overwrite (self.history_next())
            return True

        # Previous history item
        elif keyname == 'Up':
            self.overwrite (self.history_prev())
            return True

        # Move cursor just after prompt
        elif keyname == 'Home':
            mark = self.buffer.get_mark('linestart')
            linestart = self.buffer.get_iter_at_mark(mark)
            self.buffer.place_cursor (linestart)
            return True

        # Completion if line not empty
        elif keyname == 'Tab':
            line = self.last_line()
            if not line.strip():
                return False
            completed, possibilities = self.shell.complete(line)
            if len(possibilities) > 1:
                slice = line
                self.write('\n')
                for symbol in possibilities:
                    self.write(symbol+'\n')
                self.prompt('prompt')
            self.overwrite(completed or slice)
            return True

        # Controls
        elif event.get_state() & Gdk.ModifierType.CONTROL_MASK:
            if keyname in ['a','A']:
                mark = self.buffer.get_mark('linestart')
                linestart = self.buffer.get_iter_at_mark(mark)
                self.buffer.place_cursor (linestart)
                return True
            elif keyname in ['e','E']:
                end = self.buffer.get_end_iter()
                self.buffer.place_cursor (end)
                return True
            elif keyname in ['k','K']:
                start = self.buffer.get_iter_at_mark (self.buffer.get_insert())
                end = self.buffer.get_end_iter()
                self.killbuffer = self.buffer.get_text(start,end)
                self.buffer.delete(start,end)
                return True
            elif keyname in ['y','Y']:
                if self.killbuffer:
                    iter = self.buffer.get_iter_at_mark (self.buffer.get_insert())
                    self.buffer.insert(iter, self.killbuffer)
                return True
            elif keyname in ['l', 'L']:
                start = self.buffer.get_start_iter()
                end = self.buffer.get_end_iter()
                end.backward_sentence_start()
                self.buffer.delete (start,end)
            elif keyname in ['d', 'D']:
                if not len(self.last_line().strip()):
                    self.quit()

        # Editing before prompt is forbidden
        else:
            mark = self.buffer.get_mark('linestart')
            linestart = self.buffer.get_iter_at_mark(mark)
            iter = self.buffer.get_iter_at_mark(self.buffer.get_insert())
            if iter.compare(linestart) < 0:
                iter = self.buffer.get_end_iter()
                self.buffer.place_cursor (iter)
        return False


    def execute (self):
        # Python stdout, stderr, stdin redirection
        sys.stdout, self.stdout = self.stdout, sys.stdout
        sys.stderr, self.stderr = self.stderr, sys.stderr
        sys.stdin,  self.stdin  = self.stdin,  sys.stdin

        # System stdout, stderr redirection
        sys_stdout = os.dup(1)
        sys_stderr = os.dup(2)
        os.dup2 (self.pipewrite, 1)
        os.dup2 (self.pipewrite, 2)

        self.shell.eval(self)
        self.view.scroll_mark_onscreen(self.buffer.get_insert())
        while Gtk.events_pending():
            Gtk.main_iteration()

        # Get system output and remove system redirection
        os.dup2 (sys_stdout, 1)
        os.dup2 (sys_stderr, 2)
        os.close (sys_stdout)
        os.close (sys_stderr)

        # Remove python redirection
        sys.stdout, self.stdout = self.stdout, sys.stdout
        sys.stderr, self.stderr = self.stderr, sys.stderr
        sys.stdin,  self.stdin  = self.stdin,  sys.stdin


    def quit(self):
        """ Quit console """

        self.history_save()
        try:
            os.close (self.piperead)
            os.close (self.pipewrite)
        except:
            pass
        if os.path.exists (self.fifoname):
            os.remove (self.fifoname)
        self.do_quit = True

#!/usr/bin/env python
from __future__ import print_function
##########################################################################
#	USAGE: import general
#   DESCRIPTION: Functions for common tasks (e.g. opening files with
#   exception handling built in)
#   Created by Jennifer M Shelton
##########################################################################
import sys
import os
import logging as log
import errno
def print_no_newline(to_print):
    '''
        Print a statement without a new line in either python 2.7+ or python 3.3+
        '''
    print(to_print , end='')
def convert_to_full(path):
    '''
        Returns absolute path from a relative path.
    '''
    full_path = os.path.expanduser(path) # only works on '~'
    full_path2 = os.path.abspath(full_path) # works on path relative to the
    # current working directory
    return(full_path2)
def open_file(file_name):
    '''
        Returns opened (for reading) file object or kills program and relays 
        error from running the open function as a log message. If error is of
        unexpected type returns content of the error message but attempts
        to keep runnning.
    '''
    full_path2=convert_to_full(file_name)
    if sys.version_info > (3, 0): # For python3.3+ ...
        try:
            input = open(full_path2, 'r')
        except IOError as e:
            log.error('"%(e)s"' % locals()) # Print Input/output error
            sys.exit(0) # Kill program
        except:
            log.error('caught: %s' % sys.exc_info()[0]) # Print general error
    else: # For python2.7+ convert all newlines to standard \n to be safe
        try:
            input = open(full_path2, 'rU')
        except IOError as e:
            log.error('"%(e)s"' % locals()) # Print Input/output error
            sys.exit(0) # Kill program
        except:
            log.error('caught: %s' % sys.exc_info()[0]) # Print general error
    return(input)
def open_write_file(file_name):
    '''
        Returns opened (for writing) file object or kills program and relays
        error from running the open function as a message. If error is of
        unexpected type returns content of the error message but attempts
        to keep runnning.
    '''
    full_path2=convert_to_full(file_name)
    try:
        output = open(full_path2, 'w')
    except IOError as e:
        log.error('"%(e)s"' % locals()) # Print Input/output error
        sys.exit(0) # Kill program
    except:
        log.error('caught: %s' % sys.exc_info()[0]) # Print general error
    return(output)

def parse_filename(file_name):
    '''
        Returns path (with no trailing slash), basename and extension for filenames.
    '''
    full_path2=convert_to_full(file_name)
    (path_and_basename,ext)=os.path.splitext(full_path2) # ext begins with
    # the last '.'
    path=os.path.dirname(path_and_basename) # has no trailing slash
    basename=os.path.basename(path_and_basename)
    return(path,basename,ext)
def path_check(path):
    '''
        Throw fatal error if path doesn't exist, otherwise return the boolean value True.
    '''
    if not (os.path.isdir(path)):
        log.error('Error %(path)s does not exist, exiting.' % locals())
        sys.exit(0)
    else:
        return(True)
def mk_out_sub_directory(path):
    '''
        Create directory (run after testing the existence of the 
        parent directory). Block only warns if output directory 
        already exists. Returns the boolean value True or False.
    '''
    try:
        os.mkdir(path)
        return(True)
    except OSError as e:
        log.warning('%(e)s' % locals())
        if e.errno == errno.EEXIST:
            return(True)
        else:
            return(False)
    except:
        log.error('caught: %s' % sys.exc_info()[0]) # Print general error
        pass
        return(False)

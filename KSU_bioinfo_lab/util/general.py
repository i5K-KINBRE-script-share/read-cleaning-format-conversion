#!/usr/bin/env python3
##########################################################################
#	USAGE: import general
#   DESCRIPTION: Functions for common tasks (e.g. opening files with
#   exception handling built in)
#   Created by Jennifer M Shelton
##########################################################################
import sys
import os
import logging as log
def convert_to_full(path):
    '''
        Returns full path from a partial path
    '''
    full_path = os.path.expanduser(path) # only works on '~'
    full_path2 = os.path.abspath(full_path) # works on path relative to the
    # current working directory
    return(full_path2)
def open_file(file):
    '''
        Returns opened (for reading) file object or kills program and relays 
        error from running the open function as a message.
    '''
    full_path2=convert_to_full(file)
    try:
        input = open(full_path2, 'r')
    except IOError as e:
        log.error('"%(e)s"' % locals()) # Print Input/output error
        sys.exit(0) # Kill program
    except:
        log.error('caught: %s' % sys.exc_info()[0]) # Print general error
        pass
    return(input)
def open_write_file(file):
    '''
        Returns opened (for writing) file object or kills program and relays
        error from running the open function as a message.
        '''
    full_path2=convert_to_full(file)
    try:
        input = open(full_path2, 'w')
    except IOError as e:
        log.error('"%(e)s"' % locals()) # Print Input/output error
        sys.exit(0) # Kill program
    except:
        log.error('caught: %s' % sys.exc_info()[0]) # Print general error
        pass
    return(input)

def parse_filename(file):
    '''
        Returns path, basename and extension for filenames.
    '''
    full_path2=convert_to_full(file)
    (path_and_basename,ext)=os.path.splitext(full_path2) # ext begins with '.'
    path=os.path.dirname(path_and_basename) # has no trailing slash
    basename=os.path.basename(path_and_basename)
    return(path,basename,ext)
def path_check(path):
    if not (os.path.isdir(path)):
        log.error('Error %(path)s does not exist, exiting.' % locals())
        sys.exit(0)
    else:
        return()
def mk_out_sub_directory(path):
    '''
        Create directory (run after testing the existence of the 
        parent directory). Block only warns if output directory 
        already exists.
    '''
    try:
        os.mkdir(path)
    except OSError as e:
        log.warning('%(e)s' % locals())
        pass
    except:
        log.error('caught: %s' % sys.exc_info()[0]) # Print general error
        pass

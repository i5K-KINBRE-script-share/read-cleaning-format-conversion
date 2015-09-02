#!/usr/bin/env python3
##########################################################################
#	USAGE: import fasta_o_matic
#   DESCRIPTION: Functions for common FASTA file quality control tasks (e.g.
#   checking that sequences are wrapped and/or making sure final newline
#   character is present)
#   Created by Jennifer M Shelton
##########################################################################
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
util_dir = os.path.abspath(parent_dir + '/../util')
sys.path.append(util_dir)
import re
import logging as log
import general
import textwrap
import argparse
import test
from os.path import expanduser
##########################################################################
##############                  Custom classes                ############
##########################################################################
class dev_colors:
    '''
        Fonts to indicate when script is under development
    '''
    WARNING = '\033[0;95m'
    BACKGROUND = '\033[10;44m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
##########################################################################
##############                  Custom functions              ############
##########################################################################
def color_errors_warnings(f_text):
    '''
        Print magenta notice when script is under development
    '''
    print(dev_colors.WARNING + dev_colors.BOLD + dev_colors.BACKGROUND +
          f_text + dev_colors.ENDC)
##########################################################################
##############         Print informative message              ############
##########################################################################
def doc():
    '''
        Print standard information about script.
    '''
    log.info('###########################################################')
    log.info('#  fasta_o_matic.py Version 1.1.1                         #')
    log.info('#                                                         #')
    log.info('#  Created by Jennifer M Shelton 7/16/15                  #')
    log.info('#  github.com/i5K-KINBRE-script-share/Irys-scaffolding    #')
    log.info('#  python3 clean_illumina.py --help # for usage/options   #')
    log.info('###########################################################')
#color_errors_warnings('       Warning: Script currently under development!!       ')
# uncomment line above for development versions
# fasta_o_matic.py Version 1.1.0
#
# Added an optional potentially fatal, potentially non-fatal test for header uniqueness. Now default QC steps are 'wrap new_line unique' instead of 'wrap new_line header_whitespace'.
# fasta_o_matic.py Version 1.1.1
#
# Now returns final FASTA filename without a new line at the end when called from the commandline. This should make the FASTA name easier for downstream scripts to use.

##########################################################################
##############                   Unit Tests                  ############
##########################################################################
def test_reformatting(out_test_dir):
    out_test_dir = os.path.expanduser(out_test_dir)
    test_dir = out_test_dir + '/tmp'
    if (os.path.isdir(out_test_dir)): # Warn if output directory already exists
        log.disable(log.NOTSET) # flip logging back on
        log.warning('Your output directory already exists. Your output directory may already contain output from Fasta-O-Matic in %(out_test_dir)s.' % locals())
        log.disable(log.ERROR) # disable most log output again
    else:
        assert general.mk_out_sub_directory(out_test_dir), 'Failed to create output directory. Check that your output directory path.'
    assert general.mk_out_sub_directory(test_dir), 'Failed to create output sub-directory for Unit testing. Check that your output directory exists and can be written to.'
    assert (test.test_all(test_dir)), 'Failed to reformat when all three steps were called'
    assert test.test_newline(test_dir), 'Failed to reformat when only newline and header reformatting was used'
    assert test.test_wrapping(test_dir), 'Failed to reformat when only wrapping and header reformatting was used'
    assert test.test_unique(test_dir), 'Failed to reformat or die when only testing uniqueness validation and/or reformatting for headers'
    os.rmdir(test_dir)
#######################################
# Check for last new line
#######################################
def check_new_line(fasta_file_name):
    '''
        Returns True if the last line in a FASTA file ends in the 
        standard new line character ('\\n'). Returns False if not.
        Test also fails if the sequence lines ends in the less common
        '\\r' character.
    '''
    if sys.version_info > (3, 0):
        infile = open(fasta_file_name, 'r',  newline='') # Python3 will read
    # all newlines as \n so we open without converting them to test
    else:
        infile = open(fasta_file_name, 'r')
    last_char=''
    for line in infile:
        last_char = line[-1] # grab the last character
    infile.close()
    if last_char == '\n': # test the final last character
        return(True)
    else:
        return(False)
#######################################
# Correct for missing or non-canonical
# newlines
#######################################
def fix_new_line(fasta_file_name, qc_set_func, checked_qc_set_func, out_dir=None):
    '''
        Strips any new line character ('\\n' or '\\r') from each line in
        file and ends each line (including the last line) with a new 
        line character ('\\n').
    '''
    suffix = '_ended.fasta'
    if 'header_whitespace' in qc_set_func:
        suffix = '_ended_h.fasta' # make suffix match QC steps taken
    (out_path,out_basename,out_ext)=general.parse_filename(fasta_file_name)
    if out_dir is not None:
        out_path = out_dir # switch to user specified output directory
    file_with_new_line = out_path + '/' +  out_basename + suffix
    if sys.version_info > (3, 0):
        broken_fasta=general.open_file(fasta_file_name)
    else:
        broken_fasta = open(fasta_file_name, 'rU')
    fixed_fasta=general.open_write_file(file_with_new_line)
    header_pattern = re.compile('^>.*')
    header = ''
    for line in broken_fasta:
        line=line.rstrip()
        if header_pattern.match(line):
            header = line
            if 'header_whitespace' in qc_set_func:
                header = re.sub('\s+', '_', header)
            line = header
        fixed_fasta.write(line + '\n')
    fixed_fasta.close()
    broken_fasta.close()
    remove_set = set(['new_line','header_whitespace']) # Remove both qc steps
    # becuase they will be corrected in the final FASTA file
    qc_set_func = qc_set_func.difference(remove_set) # skip finished repairs
    checked_remove_set = set(['new_line'])
    checked_qc_set_func = checked_qc_set_func.difference(checked_remove_set) # skip finished checks
    return(file_with_new_line, qc_set_func, checked_qc_set_func)
#######################################
# Check that FASTA is wrapped
#######################################
def check_wrap(fasta_file_name):
    '''
        Returns True if the none of the sequence lines in a FASTA file 
        exceed 80 characters (this should be true if the FASTA file is 
        wrapped). Returns False if one or more line of sequence
        exceeds 80 characters. Wrapped file is saved with the suffix 
        '_wrap.fasta'.

    '''
    header_pattern = re.compile('^>.*')
    infile = general.open_file(fasta_file_name)
    lengths = []
    lengths_OK = False

    for line in infile:
        line = line.rstrip()
        # Check if all but last line are equal length
        if header_pattern.match(line):
            if len(lengths) > 2: # If multiple lines remain to compare
                lengths_OK = compare_lengths(lengths)
                if not lengths_OK:
                    return False
            lengths = []
        # Append to list and check if all sequence lines are < 80
        else:
            if len(line) > 80: # exit when you hit a sequence line > 80
                return False
            seq_length = len(line)
            lengths.append(seq_length)

    # One last set to evaluate after you fall off the end of the loop
    if len(lengths) > 2:
        lengths_OK = compare_lengths(lengths)
    
    return lengths_OK

def compare_lengths(lengths):
    '''
    Compare length of >= 2 lines
    '''
    assert len(lengths) > 2, "I need at least two full-length lines to compare"
    wrap_length = lengths[0]
    lengths.pop()
    
    for seq_line in lengths:    
        if seq_line != wrap_length:
            return(False)
    return(True)
#######################################
# Wrap an unwrapped or improperly
# wrapped FASTA
#######################################
def fix_wrap(fasta_file_name, qc_set_func, checked_qc_set_func, out_dir=None):
    '''
        Wraps text in a FASTA file so that no line of sequence has more
        than 60 bases. Wrapped file is saved with the suffix '_wrap.fasta'.
    '''
    suffix = '_wrap.fasta'
    if 'header_whitespace' in qc_set_func:
        suffix = '_wrap_h.fasta'
    (out_path,out_basename,out_ext)=general.parse_filename(fasta_file_name)
    if out_dir is not None:
        out_path = out_dir # switch to user specified output directory
    file_with_wrapping = out_path + '/' + out_basename + suffix
    fixed_fasta=general.open_write_file(file_with_wrapping)
    header_pattern = re.compile('^>.*')
    infile = general.open_file(fasta_file_name)
    dna    = ''
    for line in infile:
        line = line.rstrip()
        if header_pattern.match(line): # Print headers immediately to new file
            header = line
            if 'header_whitespace' in qc_set_func:
                header = re.sub('\s+', '_', header)
            if dna:
                fixed_fasta.write(dna + '\n') # print remaining sequence
                # before header
            fixed_fasta.write(header + '\n')
            dna = '' # Reset DNA
        else: # if the line is sequence data dump sequence as fast as it is
            # long enough to wrap
            dna = dna + line
            while len(dna) > 59: # Wrap sequence lines after
                # 60 bases
                wrap_line = dna[0:60]
                dna = dna[60:len(dna)]
                fixed_fasta.write(wrap_line + '\n')
    # Catch the last record
    else: # For end of file
        if dna:
            fixed_fasta.write(dna + '\n') # print remaining sequence
        # before header
    fixed_fasta.close()
    infile.close()
    remove_set = set(['wrap','new_line','header_whitespace']) # Remove all three qc steps
    # becuase all will be corrected in the final FASTA file
    qc_set_func = qc_set_func.difference(remove_set) # skip finished repairs
    checked_remove_set = set(['wrap'])
    checked_qc_set_func = checked_qc_set_func.difference(checked_remove_set) # skip finished checks
    return(file_with_wrapping, qc_set_func, checked_qc_set_func)

#######################################
# Check for white space in FASTA
# headers
#######################################
def check_headers(fasta_file_name):
    '''
        Check if FASTA headers contain white spaces that break Trimmomatic and 
        some other bioinfo tools. Return True if header has spaces. Returns 
        False if header has no spaces.
    '''
    header_pattern = re.compile('^>.*')
    infile = general.open_file(fasta_file_name)
    for line in infile:
        line = line.rstrip()
        if header_pattern.match(line):
            if re.match('.*\s.*', line):
                return(False)
    return(True)
#######################################
# Replace white space in FASTA
# headers
#######################################
def fix_headers(fasta_file_name, qc_set_func, checked_qc_set_func, out_dir=None):
    '''
        Remove white spaces from the headers of a FASTA file. Fixed FASTA file
        is saved with the suffix '_h.fasta'.
    '''
    (out_path,out_basename,out_ext)=general.parse_filename(fasta_file_name)
    if out_dir is not None:
        out_path = out_dir # switch to user specified output directory
    file_with_header = out_path + '/' +  out_basename + '_h.fasta'
    broken_fasta=general.open_file(fasta_file_name)
    fixed_fasta=general.open_write_file(file_with_header)
    header_pattern = re.compile('^>.*')
    header = ''
    for line in broken_fasta:
        line=line.rstrip()
        if header_pattern.match(line):
            header = line
            header = re.sub('\s+', '_', header)
            line = header
        fixed_fasta.write(line + '\n')
    fixed_fasta.close()
    broken_fasta.close()
    remove_set = set(['header_whitespace']) # Remove qc step becuase it will be corrected
    # in the final FASTA file
    qc_set_func = qc_set_func.difference(remove_set) # skip finished repairs
    checked_qc_set_func = checked_qc_set_func.difference(remove_set) # skip finished checks
    return(file_with_header, qc_set_func, checked_qc_set_func)
#######################################
# Check for that the file starts with
# at least a '>'
#######################################
def check_header_pattern(fasta_file_name):
    '''
        Check if FASTA file begins with a '>'. Returns True if the first line
        is begins with a '>'. Returns False if the file starts with any other 
        character.
    '''
    header_pattern = re.compile('^>.*')
    infile = general.open_file(fasta_file_name)
    first_line = infile.readline()
    infile.close()
    if header_pattern.match(first_line):
        return(True)
    else:
        return(False)
#######################################
# Check for non-IUPAC characters in
# sequence lines
#######################################
def check_iupac(fasta_file_name):
    '''
        Check if FASTA file contains non-IUPAC characters in sequence lines. 
        Returns false if non-IUPAC characters are found and True if non are 
        found.
    '''
    iupac_set = set(['a' , 'b' , 'c' , 'd' , 'e' , 'f' , 'g' , 'h' , 'i' , 'k' , 'l' , 'm' , 'n' , 'o' , 'p' , 'q' , 'r' , 's' , 't' , 'u' , 'v' , 'w' , 'x' , 'y' , 'A' , 'B' , 'C' , 'D' , 'E' , 'F' , 'G' , 'H' , 'I' , 'K' , 'L' , 'M' , 'N' , 'O', 'P' , 'Q' , 'R' , 'S' , 'T' , 'U' , 'V' , 'W' , 'X' , 'Y' , '-' , '*'])
    header_pattern = re.compile('^>.*')
    infile = general.open_file(fasta_file_name)
    for line in infile:
        if not header_pattern.match(line):
            line = line.rstrip()
            for char in line:
                if not char in iupac_set: # check each character against IUPAC set
                    log.error('\tError: %(char)s in sequence line' % locals())
                    return(False)
    return(True)
#######################################
# Check if header first words are
# unique in entire FASTA
#######################################
def check_unique(fasta_file_name):
    '''
        Check if FASTA headers have unique first words. Returns True if header
        first words are unique. Returns False if header first words are not and 
        cannot be made unique automatically.
        '''
    first_word_set = set()
    header_pattern = re.compile('^>.*')
    infile = general.open_file(fasta_file_name)
    for line in infile:
        line = line.rstrip()
        if header_pattern.match(line):
            if re.match('^>(\S+)',line): # grab first word in description
                word = re.match('^>(\S+)',line) # grab first word in description
                current_word = word.group(1)
                if not current_word in first_word_set:
                    first_word_set.add(current_word)
                else:
                    return(False) # you have seen this first word before!
            else:
                return(False) # Blank headers can't pass a test for uniqueness
    return(True)

#######################################
# Main function runs quality checking
# and filtering based on a
# user-defined list of quality checks
#######################################

def main():
    '''
        For a given FASTA file function runs all qc steps listed in the
        list of steps.
        
        USAGE: python fasta_o_matic.py [-h] [-v] [-q] [-c] -f FILE -s STEPS
        
        QC STEPS:
        
        unique - Checks if FASTA headers have unique first words or can be made unique automatically. May save altered file with suffix '_h.fasta'.
        
        new_line - Checks if the last line in a FASTA file ends in the
        standard new line character ('\\n') and will also fail if the sequence 
        lines end in the less common '\\r' character. Reformatted files are 
        saved with the '_ended.fasta' suffix.
        
        wrap - Checks if the sequence lines in a FASTA file exceed 80 characters and if all the wrapped lines are the same length (this should be true if the FASTA file is  wrapped). Wrapped file is saved with the suffix
        '_wrap.fasta'.
        
        header_whitespace - Remove white spaces from the headers of a FASTA file.
        Fixed FASTA file is saved with the suffix '_h.fasta'.
    '''
    ######################################################################
    ############        Get commandline arguments             ############
    ######################################################################
    parser = argparse.ArgumentParser(
                                     description='DESCRIPTION: Script runs quality checking and filtering \
                                     based on a user-defined list of quality \
                                     checks. Command-line options that may be \
                                     omitted (i.e. are NOT required) are shown \
                                     in square brackets.\
                                     \
                                     QC STEPS:\
                                     \
                                     unique -- checks if FASTA headers have unique\
                                     first words or can be made unique \
                                     automatically. May save altered file with \
                                     suffix \'_h.fasta\'.\
                                     \
                                     new_line -- checks if the last line in a FASTA file ends in the standard new line \
                                     character (\'\\n\') and will also fail if \
                                     the sequence lines end in the less common \
                                     \'\\r\' character. Reformatted files are \
                                     saved with the \'_ended.fasta\' suffix.\
                                     \
                                     wrap -- checks if the sequence lines in a \
                                     FASTA file exceed 80 characters and if all \
                                     the wrapped lines are the same length \
                                     (this should be true if the FASTA file is \
                                     wrapped). Wrapped file is saved with the \
                                     suffix \'_wrap.fasta\'.\
                                     \
                                     header_whitespace -- remove white spaces \
                                     from the headers of a FASTA file. Fixed \
                                     FASTA file is saved with the suffix \
                                     \'_h.fasta\'.')
    parser.add_argument('-v', '--verbose', action='store_true',
                     dest='verbose', help='Runs reporting status updates',
                     default=True)
    parser.add_argument('-q', '--quiet', action='store_false',
                     dest='verbose', help='Does not report status updates')
    parser.add_argument('-c', '--colorized',
                     help='Colorizes log reports. Use only if printing \
                     output to screen.',action='store_true',dest='colorized')
    parser.add_argument('-f', '--fasta', dest='fasta_file_name',
                     help='This is the the full path (path and filename) of \
                     the user provided FASTA file.', required=True)
    parser.add_argument('-s', '--qc_steps', nargs='+', dest='steps',
                     help='List of QC steps to  perform on FASTA file \
                     options are wrap, new_line, header_whitespace, unique \
                     (default= -s wrap new_line unique).',
                     default=['wrap','new_line','unique'],
                     required=False)
    parser.add_argument('-o', '--out_dir', dest='out_dir',
                        help='Output directory for any repaired FASTA created (no trailing slash).', default=None,required=False)
    args = parser.parse_args()
    if args.verbose:
        log.basicConfig(format='%(levelname)s:  %(message)s', level=log.DEBUG)
        doc()
        log.info('Output is verbose. Run with -q, --quiet flag to suppress full output.')
    else:
        log.basicConfig(format='%(levelname)s: %(message)s')
    if args.colorized:
        import Colorer
    log.info('#######################################')
    log.info('# Unit testing...')
    log.info('#######################################')
    log.disable(log.CRITICAL)
    (out_path,out_basename,out_ext)=general.parse_filename(args.fasta_file_name)
    if args.out_dir is not None:
        out_path = args.out_dir # switch to user specified output directory
    test_reformatting(out_path)
    log.disable(log.NOTSET)
    log.info('#######################################')
    log.info('# Done unit testing.')
    log.info('#######################################')
    # Run reformatting
    final_fasta_file_name = run_steps(args.fasta_file_name, args.steps, args.out_dir)
    return(final_fasta_file_name)

def run_steps(fasta_file_name, steps, out_dir):
    '''
        For a given FASTA file function runs all qc steps listed in the
        list of steps.
        USAGE: fasta_o_matic.run_steps('/usr/me/test.fasta',
        ['wrap', 'new_line','header_whitespace'], '/Users/jennifer_shelton/out_fasta_o_matic')
    '''
    log.info('#######################################')
    log.info('# Running Fasta_O_Matic...')
    log.info('#######################################')
    original_file = fasta_file_name
    # First check for fatal errors:
    log.info('Checking for fatal errors...')
    if check_header_pattern(fasta_file_name):
        log.info('\tFirst header: good')
    else:
        log.error('\tFile may not be in FASTA format because it does not begin with > for file %(fasta_file_name)s' % locals()) # Print Input/output error
        sys.exit(0) # Kill program
    if check_iupac(fasta_file_name):
        log.info('\tSequence characters: good')
    else:
        log.error('\tFile may not be in FASTA format because sequence lines include non-IUPAC characters for file %(fasta_file_name)s' % locals())
        sys.exit(0) # Kill program
    qc_set=set(steps)
    checked_qc_set=set(steps)
    log.info('Done checking for fatal errors.')
    # Next check for non-fatal errors:
    log.info('Checking for non-fatal errors...')
#    print(qc_set)
    if 'wrap' in qc_set:
        log.info('Running FASTA wrapping QC...')
        if check_wrap(fasta_file_name):
            log.info('\tWrap: good')
            remove_set = set(['wrap'])
            qc_set = qc_set.difference(remove_set) # skip wrap fix in furture
            checked_qc_set = checked_qc_set.difference(remove_set) # skip wrap
            # check in furture
        else:
#            print(qc_set)
            log.warning('\tWrap: bad. Correcting sequence wrap now...')
            (file_with_wrapping, qc_set, checked_qc_set) = fix_wrap(fasta_file_name, qc_set, checked_qc_set, out_dir)
#            print(qc_set)
            if not file_with_wrapping == fasta_file_name:
                if not fasta_file_name == original_file: # NEVER DELETE THE ORIGINAL FILE
                    os.remove(fasta_file_name)
            fasta_file_name = file_with_wrapping
        log.info('Done with FASTA wrapping QC.')
    if 'new_line' in qc_set:
        log.info('Running FASTA new line QC...')
        if check_new_line(fasta_file_name):
            log.info('\tNew_line: good')
            remove_set = set(['new_line'])
            qc_set = qc_set.difference(remove_set) # skip new_line fix in
            # furture
            checked_qc_set = checked_qc_set.difference(remove_set) # skip
            # new_line check in furture
        else:
            log.warning('\tNew_line: bad. Correcting FASTA now...')
            (new_file, qc_set, checked_qc_set) = fix_new_line(fasta_file_name, qc_set, checked_qc_set, out_dir)
            if not new_file == fasta_file_name:
                if not fasta_file_name == original_file: # NEVER DELETE THE ORIGINAL FILE
                    os.remove(fasta_file_name)
            fasta_file_name = new_file
#            log.info(fasta_file_name)
        log.info('Done with FASTA new line QC.')
    if 'unique' in qc_set:
        log.info('Checking FASTA header uniqueness...')
        if check_unique(fasta_file_name):
            log.info('\tHeader uniqueness: good')
            remove_set = set(['unique'])
            qc_set = qc_set.difference(remove_set) # skip header fix in
            # furture
            checked_qc_set = checked_qc_set.difference(remove_set) # skip
            # header check in furture
        else: # attempt to remove header whitespace (in case that makes first words unique)
            qc_set_header = set(['header_whitespace'])
            (headers_whitespace, qc_set_header, checked_qc_set) = fix_headers(fasta_file_name, qc_set_header, checked_qc_set, out_dir)
            if check_unique(headers_whitespace): # check first word uniqueness again
                log.warning('\tHeader whitespace impact on uniqueness: bad. Correcting FASTA now...')
                fasta_file_name = headers_whitespace
                remove_set = set(['header_whitespace'])
                qc_set = qc_set.difference(remove_set) # skip header fix in
                # furture
                checked_qc_set = checked_qc_set.difference(remove_set) # skip
                # header check in furture
            else: # if all uniqueness tests fail die
                os.remove(headers_whitespace)
                log.error('\tFirst words in FASTA file header/desciption lines were not unique and could not be made unique automatically for file %(fasta_file_name)s' % locals())
                sys.exit(0) # Kill program
    if 'header_whitespace' in qc_set:
        log.info('Running FASTA header whitespace QC...')
        if check_headers(fasta_file_name):
            log.info('\tHeader whitespace: good')
            remove_set = set(['header_whitespace'])
            qc_set = qc_set.difference(remove_set) # skip header fix in
            # furture
            checked_qc_set = checked_qc_set.difference(remove_set) # skip
            # header check in furture
        else:
            log.warning('\tHeader whitespace: bad. Correcting FASTA now...')
            (headers_whitespace, qc_set, checked_qc_set) = fix_headers(fasta_file_name, qc_set, checked_qc_set, out_dir)
            fasta_file_name = headers_whitespace
        log.info('Done with FASTA header whitespace QC.')
#    print(checked_qc_set)
    if checked_qc_set:
        log.info('Checking QC steps skipped after they were corrected in previous step...')
        if 'wrap' in checked_qc_set:
            if check_wrap(original_file):
                log.info('\tWrap: good')
            else:
                log.warning('\tWrap: bad')
        if 'new_line' in checked_qc_set:
            if check_new_line(original_file):
                log.info('\tNew_line: good')
            else:
                log.warning('\tNew_line: bad')
        if 'header_whitespace' in checked_qc_set:
            if check_headers(original_file):
                log.info('\tHeader whitespace: good')
            else:
                log.warning('\tHeader whitespace: bad')
    log.info('Done checking for non-fatal errors.')
    log.info('#######################################')
    log.info('# Done with Fasta_O_Matic.')
    log.info('#######################################')
    return(fasta_file_name)

##########################################################################
#####       Execute main unless script is simply imported     ############
#####                for individual functions                 ############
##########################################################################
if __name__ == '__main__':
    final_fasta_file_name = main()
    sys.stdout.write(final_fasta_file_name)


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
    print('###########################################################')
    print('#  fasta_o_matic.py Version 1.0.0                         #')
    print('#                                                         #')
    print('#  Created by Jennifer M Shelton 7/16/15                  #')
    print('#  github.com/i5K-KINBRE-script-share/Irys-scaffolding    #')
    print('#  python3 clean_illumina.py --help # for usage/options   #')
    print('###########################################################')
#color_errors_warnings('       Warning: Script currently under development!!       ')
# uncomment line above for development versions
#######################################
# Check for last new line
#######################################
def check_new_line(file):
    '''
        Returns True if the last line in a FASTA file ends in the 
        standard new line character ('\\n'). Returns False if not.
        Test also fails if the sequence lines ends in the less common
        '\\r' character.
    '''
    infile = general.open_file(file)
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
def fix_new_line(file, header_whitespace=False, out_dir=None):
    '''
        Strips any new line character ('\\n' or '\\r') from each line in
        file and ends each line (including the last line) with a new 
        line character ('\\n').
    '''
    suffix = '_ended.fasta'
    if header_whitespace:
        suffix = '_ended_h.fasta' # make suffix match QC steps taken
    (out_path,out_basename,out_ext)=general.parse_filename(file)
    if out_dir is not None:
        out_path = out_dir # switch to user specified output directory
    file_with_new_line = out_path + '/' +  out_basename + suffix
    broken_fasta=general.open_file(file)
    fixed_fasta=general.open_write_file(file_with_new_line)
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
    return(file_with_new_line)
#######################################
# Check that FASTA is wrapped
#######################################
def check_wrap(file):
    '''
        Returns True if the none of the sequence lines in a FASTA file 
        exceed 80 characters (this should be true if the FASTA file is 
        wrapped). Returns False if one or more line of sequence
        exceeds 80 characters. Wrapped file is saved with the suffix 
        '_wrap.fasta'.

    '''
    header_pattern = re.compile('^>.*')
    infile = general.open_file(file)
    lengths = []
    wrap_length = None
    for line in infile:
        line = line.rstrip()
        # Check if all but last line are equal length
        if header_pattern.match(line):
            if len(lengths) > 2: # If multiple lines remain to compare
                if wrap_length is None:
                    wrap_length = lengths[0] # initialize wrapping length
                lengths.pop() # Remove the last sequence line
                for seq_line in lengths:
                    if seq_line != wrap_length:
                        return(False) #Exit when you hit mismatched wrapped lines
            lengths = []
        # Check if all sequence lines are < 80
        if not header_pattern.match(line):
            if len(line) > 80: # exit when you hit a sequence line > 80
                return(False)
            seq_length = len(line)
            lengths.append(seq_length)
    else: # For end of file
        if len(lengths) > 2: # If multiple lines remain to compare
            if wrap_length is None:
                wrap_length = lengths[0] # initialize wrapping length
                lengths.pop() # Remove the last sequence line
                for seq_line in lengths:
                    if seq_line != wrap_length:
                        return(False) #Exit when you hit mismatched wrapped lines
    return(True)
#######################################
# Wrap an unwrapped or improperly
# wrapped FASTA
#######################################
def fix_wrap(file, header_whitespace=False, out_dir=None):
    '''
        Wraps text in a FASTA file so that no line of sequence has more 
        than 60 bases. Wrapped file is saved with the suffix '_wrap.fasta'.
    '''
    suffix = '_wrap.fasta'
    if header_whitespace:
        suffix = '_wrap_h.fasta'
    (out_path,out_basename,out_ext)=general.parse_filename(file)
    if out_dir is not None:
        out_path = out_dir # switch to user specified output directory
    file_with_wrapping = out_path + '/' + out_basename + suffix
    fixed_fasta=general.open_write_file(file_with_wrapping)
    header_pattern = re.compile('^>.*')
    infile = general.open_file(file)
    dna = ''
    header = ''
    for line in infile:
        line = line.rstrip()
        if header_pattern.match(line):
            if not dna == '': # skip the first (empty record)
                fixed_fasta.write(header + '\n')
                wrap = textwrap.fill(dna,60) # Wrap sequence lines after
                    # 60 bases
                fixed_fasta.write(wrap + '\n')
            header = line
            if header_whitespace:
                header = re.sub('\s+', '_', header) # Gets rid of
                    # whitespace in the headers
            new_dna = next(infile)
            new_dna = new_dna.rstrip()
            dna = new_dna
        else:
            dna = dna + line
    else: # For end of file
        fixed_fasta.write(header + '\n')
        wrap = textwrap.fill(dna,60) # Wrap sequence lines after
        # 60 bases
        fixed_fasta.write(wrap + '\n')
    fixed_fasta.close()
    infile.close()
    return(file_with_wrapping)
#######################################
# Check for white space in FASTA
# headers
#######################################
def check_headers(file):
    '''
        Check if FASTA headers contain white spaces that break Trimmomatic and 
        some other bioinfo tools. Return True if header has spaces. Returns 
        False if header has no spaces.
    '''
    header_pattern = re.compile('^>.*')
    infile = general.open_file(file)
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
def fix_headers(file, out_dir=None):
    '''
        Remove white spaces that break Trimmomatic and some other bioinfo tools 
        from the headers of a FASTA file. Fixed FASTA file is saved with the 
        suffix '_h.fasta'.
    '''
    (out_path,out_basename,out_ext)=general.parse_filename(file)
    if out_dir is not None:
        out_path = out_dir # switch to user specified output directory
    file_with_header = out_path + '/' +  out_basename + '_h.fasta'
    broken_fasta=general.open_file(file)
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
    return(file_with_header)
#######################################
# Check for that the file starts with
# at least a '>'
#######################################
def check_header_pattern(file):
    '''
        Check if FASTA file begins with a '>'. Returns True if the first line
        is begins with a '>'. Returns False if the file starts with any other 
        character.
    '''
    header_pattern = re.compile('^>.*')
    infile = general.open_file(file)
    first_line = infile.readline()
    infile.close()
    if header_pattern.match(first_line):
        return(True)
    else:
        return(False)

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
    '''
    ######################################################################
    ############        Get commandline arguments             ############
    ######################################################################
    parser = argparse.ArgumentParser(
                                     description='DESCRIPTION: Script runs quality checking and filtering \
                                     based on a user-defined list of quality \
                                     checks. Command-line options that may be \
                                     omitted (i.e. are NOT required) are shown \
                                     in square brackets.')
    parser.add_argument('-v', '--verbose', action='store_true',
                     dest='verbose', help='Runs reporting status updates',
                     default=True)
    parser.add_argument('-q', '--quiet', action='store_false',
                     dest='verbose', help='Does not report status updates')
    parser.add_argument('-c', '--colorized',
                     help='Colorizes log reports. Use only if printing \
                     output to screen.',action='store_true',dest='colorized')
    parser.add_argument('-f', '--fasta', dest='file',
                     help='This is the the full path (path and filename) of \
                     the user provided FASTA file.', required=True)
    parser.add_argument('-s', '--qc_steps', nargs='+', dest='steps',
                     help='List of QC steps to  perform on FASTA file \
                     (default= -s wrap new_line header_whitespace).',
                     default=['wrap','new_line','header_whitespace'],
                     required=False)
    parser.add_argument('-o', '--out_dir', dest='out_dir',
                        help='Output directory for any repaired FASTA created (no trailing slash).', default=None,required=False)
    args = parser.parse_args()
    if args.colorized:
        import Colorer
    if args.verbose:
        doc()
        log.basicConfig(format='%(levelname)s:  %(message)s', level=log.DEBUG)
        log.info('Output is verbose. Run with -q, --quiet flag to suppress full output.')
    else:
        log.basicConfig(format='%(levelname)s: %(message)s')

    run_steps(args.file, args.steps, args.out_dir)

def run_steps(file, steps, out_dir):
    '''
        For a given FASTA file function runs all qc steps listed in the
        list of steps.
        USAGE: fasta_o_matic.run_steps'/usr/me/test.fasta',
        ['wrap', 'new_line','header_whitespace'])
    '''
    log.info('#######################################')
    log.info('# Running Fasta_O_Matic...')
    log.info('#######################################')
    original_file = file
    # First check for fatal errors:
    log.info('Checking for fatal errors...')
    if check_header_pattern(file):
        log.info('\tFirst header: good')
    else:
        log.error('\tFile may not be in FASTA format because it does not begin with > for file %(file)s' % locals()) # Print Input/output error
        sys.exit(0) # Kill program
    qc_set=set(steps)
    if 'header_whitespace' in qc_set:
        header_whitespace = True
    else:
        header_whitespace = False
    log.info('Done checking for fatal errors.')
    # Next check for non-fatal errors:
    log.info('Checking for non-fatal errors...')
    print(qc_set)
    if 'wrap' in qc_set:
        log.info('Running FASTA wrapping QC...')
        if check_wrap(file):
            log.info('\tWrap: good')
        else:
            log.warning('\tWrap: bad. Correcting sequence wrap now...')
            if header_whitespace:
                log.info('\tAny white space in headers will be replaced with')
                log.info('\t\'-\' while correcting sequence wrap now...')
            file_with_wrapping = fix_wrap(file, header_whitespace, out_dir)
            if not file_with_wrapping == file:
                if not file == original_file: # NEVER DELETE THE ORIGINAL FILE
                    os.remove(file)
            file = file_with_wrapping
            if 'new_line' in qc_set: # If file was wrapped you can skip new
                # line checks
                log.info('\tSkipping check for proper new line characters ')
                log.info('\tbecause when file was wrapped line endings were ')
                log.info('\tset correctly.')
                remove_set = set(['new_line'])
                qc_set = qc_set.difference(remove_set) # skip newline fix in
                # furture
                header_whitespace = False #if headers were fixed skip in future
        log.info('Done with FASTA wrapping QC.')
    if 'new_line' in qc_set:
        log.info('Running FASTA new line QC...')
        # If the FASTA file has been wrapped then the new line
        # characters have already been corrected so skip new_line
        # correction.
        new_line_passed = check_new_line(file)
        if sys.version_info > (3, 0):
            log.warning('Python3 will read all newlines as \\n we will replace newlines to be safe.')
        elif new_line_passed:
            log.info('\tNew_line: good')
        if sys.version_info > (3, 0) or not new_line_passed:
            log.warning('\tNew_line: may be bad. Correcting FASTA now...')
            if header_whitespace:
                log.info('''\tAny white space in headers will be replaced 
                    with \'-\' while correcting new lines now...''')
            new_file = fix_new_line(file, header_whitespace, out_dir)
            if not new_file == file:
                if not file == original_file: # NEVER DELETE THE ORIGINAL FILE
                    os.remove(file)
            file = new_file
            header_whitespace = False # if headers were fixed skip in future
            log.info(file)
    if header_whitespace:
        if check_headers(file):
            log.info('\tHeader whitespace: good')
        else:
            log.warning('\tHeader whitespace: bad. Correcting FASTA now...')
            headers_whitespace = fix_headers(file, out_dir)
            log.info(headers_whitespace)
            file = headers_whitespace
    log.info('Done with FASTA new line QC.')
    log.info('Done checking for non-fatal errors.')
    log.info('#######################################')
    log.info('# Done with Fasta_O_Matic.')
    log.info('#######################################')
    return(file)

##########################################################################
#####       Execute main unless script is simply imported     ############
#####                for individual functions                 ############
##########################################################################
if __name__ == '__main__':
    main()

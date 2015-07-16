#!/usr/bin/env python3
##########################################################################
#	USAGE: import fasta_qc
#   DESCRIPTION: Functions for common FASTA file quality control tasks (e.g.
#   checking that sequences are wrapped and/or making sure final newline
#   character is present)
#   Created by Jennifer M Shelton
##########################################################################
import re
import logging as log
import general
import textwrap
import os
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
def fix_new_line(file, header_whitespace=False):
    '''
        Strips any new line character ('\\n' or '\\r') from each line in
        file and ends each line (including the last line) with a new 
        line character ('\\n').
    '''
    suffix = '_ended.fasta'
    if header_whitespace:
        suffix = '_ended_h.fasta'
    (out_path,out_basename,out_ext)=general.parse_filename(file)
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
    for line in infile:
        line = line.rstrip()
        if not header_pattern.match(line):
            if len(line) > 80:
                return(False)
    return(True)
#######################################
# Wrap an unwrapped or improperly
# wrapped FASTA
#######################################
def fix_wrap(file, header_whitespace=False):
    '''
        Wraps text in a FASTA file so that no line of sequence has more 
        than 60 bases. Wrapped file is saved with the suffix '_wrap.fasta'.
    '''
    suffix = '_wrap.fasta'
    if header_whitespace:
        suffix = '_wrap_h.fasta'
    (out_path,out_basename,out_ext)=general.parse_filename(file)
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
    fixed_fasta.close()
    infile.close()
    return(file_with_wrapping)
#######################################
# Find/replace white space in FASTA
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
def fix_headers(file):
    '''
        Remove white spaces that break Trimmomatic and some other bioinfo tools 
        from the headers of a FASTA file. Fixed FASTA file is saved with the 
        suffix '_h.fasta'.
    '''
    (out_path,out_basename,out_ext)=general.parse_filename(file)
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
# Runs quality checking and filtering
# based on a user-defined list of
# quality checks
#######################################
def main(file,steps):
    '''
        For a given FASTA file function runs all qc steps listed in the
        set of steps. 
        USAGE: fasta_qc.main('/usr/me/test.fasta',['wrap', 'new_line','header_whitespace'])
    '''
    log.info('#######################################')
    log.info('# Running FASTA QC...')
    log.info('#######################################')
    original_file = file
    qc_set=set(steps)
    if 'header_whitespace' in qc_set:
        header_whitespace = True
    else:
        header_whitespace = False
    if 'wrap' in qc_set:
        log.info('Running FASTA wrapping QC...')
        if check_wrap(file):
            log.info('\tWrap: good')
        else:
            log.info('\tWrap: bad')
            file_with_wrapping = fix_wrap(file, header_whitespace)
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
        if check_new_line(file):
            log.info('\tNew_line: good')
        else:
            log.info('\tNew_line: bad')
            new_file = fix_new_line(file, header_whitespace)
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
            log.info('\tHeader whitespace: bad')
            headers_whitespace = fix_headers(file)
            log.info(headers_whitespace)
            file = headers_whitespace
    log.info('Done with FASTA new line QC.')
    log.info('#######################################')
    log.info('# Done with FASTA QC.')
    log.info('#######################################')
    return(file)

##########################################################################
#####       Execute main unless script is simply imported     ############
#####                for individual functions                 ############
##########################################################################
if __name__ == '__main__':
    main(file,steps)

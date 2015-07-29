#!/usr/bin/env python
##########################################################################
#       USAGE: import fasta_clean
#   DESCRIPTION: Makes sure a FASTA file is formatted in the way we expect
#                with wrapped sequence lines, unix newline characters and
#                whitespace removed from the headers
##########################################################################
import os
import sys
import re
import argparse
from Bio import SeqIO

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
util_dir   = os.path.abspath(parent_dir + '/../util')
sys.path.append(util_dir)
import general

def doc():
    '''
        Print standard information about script.
    '''
    print('###########################################################')
    print('#  fasta_clean.py Version 0.0.1                           #')
    print('       Warning: Script currently under development!!      #')
    print('       This script was designed to test parsing files     #') 
    print('       with BioPython. It has not been tested to          #')
    print('       reformat FASTA files yet!!                         #')
    print('###########################################################')

# Assume the file is broken and make a new one with 
# standardized formatting.
def fix_fasta_file(file, out_dir=None):
    '''
        Passes a file through biopython SeqIO to remove common
        formatting issues like '\r' characters and unwrapped sequences.
        The new file is saved with the suffix '_clean.fasta'.
    '''

    # Give up early if the file does not look like fasta
    assert check_header_pattern(file), "Sorry, " + str(file) + " does not look like FASTA to me"

    suffix = '_clean.fa';
    (out_path,out_basename,out_ext) = general.parse_filename(file)
    if out_dir is not None:
        os.system("mkdir -p "+out_dir);
        out_path = out_dir

    fixed_file = out_path + '/' + out_basename + suffix
    out_handle = general.open_write_file(fixed_file)
    fasta_in  = SeqIO.parse(file,'fasta');

    # Iterate through the records to remove white-space
    # from the ID line
    new_records = []
    for record in fasta_in:
        header = re.sub('\s+','_',record.description)
        record.id = header
        record.name = header
        record.description = ''
        new_records.append(record)

    written = SeqIO.write(new_records, out_handle,'fasta')

    print str(written) + ' sequence records stored in ' + fixed_file

    return(fixed_file)

#######################################
# Check that the file starts with
# at least a '>'
#######################################
def check_header_pattern(file):
    '''
        Check if FASTA file begins with a '>'. Returns True if the first line
        begins with a '>'. Returns False if the file starts with any other                                                     
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

def main():
    '''
        For a given FASTA file function runs all qc steps listed in the
        list of steps.
        USAGE: python fasta_massager.py [-o] -f FILE
    '''
    ######################################################################
    ############        Get commandline arguments             ############
    ######################################################################
    parser = argparse.ArgumentParser(
                                     description='DESCRIPTION: Script massaged FASTA a little bit \
                                     Command-line options that may be \
                                     omitted (i.e. are NOT required) are shown \
                                     in square brackets.')

    parser.add_argument('-f', '--fasta', 
                        dest='file',
                        help='This is the the full path (path and filename) of \
                        the user provided FASTA file.', 
                        required=True)

    parser.add_argument('-o', '--out_dir', 
                        dest='out_dir',
                        help='Output directory for any repaired FASTA created (no trailing slash).', 
                        default=None,
                        required=False)
    args = parser.parse_args()

    fix_fasta_file(args.file,args.out_dir)

if __name__ == '__main__':
    main()

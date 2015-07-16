#!/usr/bin/env python3
##########################################################################
#	USAGE: python3 clean_illumina.py [options]
#   DESCRIPTION: Summarize counts of all four DNA bases.
#   Created by Jennifer M Shelton
##########################################################################
import argparse
import logging as log
import os
import trimmomatic_template
import general
import fasta-o-matic
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
    print('#  clean_illumina.py Version 1.0.0                        #')
    print('#                                                         #')
    print('#  Created by Jennifer M Shelton 6/28/15                  #')
    print('#  github.com/i5K-KINBRE-script-share/Irys-scaffolding    #')
    print('#  python3 clean_illumina.py --help # for usage/options   #')
    print('###########################################################')
color_errors_warnings('       Warning: Script currently under development!!       ')
##########################################################################
##############                  Main function                 ############
##########################################################################
def main():
    '''
        Run full script as opposed to individual script functions.
    '''
    ######################################################################
    ############        Get commandline arguments             ############
    ######################################################################
    parser = argparse.ArgumentParser(
    description='DESCRIPTION: Summarize counts of all four DNA bases. \
                                     Command-line options that may be omitted \
                                     (i.e. are NOT required) are shown in \
                                     square brackets.')
    parser.add_argument('-v', '--verbose', action='store_true',
    dest='verbose', help='Runs reporting status updates',
    default=True)
    parser.add_argument('-q', '--quiet', action='store_false',
                     dest='verbose', help='Does not report status updates')
    parser.add_argument('-c', '--colorized',
                     help='Colorizes log reports. Use only if printing \
                     output to screen.',action='store_true',dest='colorized')
    parser.add_argument('-r', '--read_list', dest='read_list',
                        help='This is the the full path (path and filename) of \
                        the user provided list of read files. The file should \
                        be tab separated with the first read file, then the \
                        second read file (see example_read_list_PE.tab). If a \
                        sample has multiple fastq files for R1 and R2 separate \
                        these with commas (see example_read_list_PE_multi.tab).\
                        For single end reads each line should be a path \
                        to a fastq file. For single end reads each line should \
                        be a path to a fastq file (see example_read_list_SE.tab\
                        )', required=True)
    parser.add_argument('-p', '--project', dest='project',
                     help='The project id. This will be used to name output \
                        (default=project).', default='project', required=False)
    parser.add_argument('-a', '--adapter', dest='adapter',
                        help='The adapter fasta file. This will be used to \
                        clean reads',default='/homes/bioinfo_software/Trimmomatic-0.33/adapters/TruSeq3-PE-2.fa', required=False)
    parser.add_argument('-s', '--single_end', action='store_true', dest='single',
                        help='If your reads are single end use this flag. \
                        Without it the script assumes reads are paired end. \
                        Also skip the second column (the reverse fastq files) \
                        when making your read list', required=False,
                        default=False)
    parser.add_argument('-x', '--convert_header', action='store_true',
                        dest='convert_header', help='If the illumina headers \
                        do not end in /1 or /2 use this parameter to indicat \
                        that headers need to be converted. Check your headers \
                        by typing "head FASTA_FULL_PATH" and read more about \
                        illumina headers at \
                        http://en.wikipedia.org/wiki/Fastq#Illumina_sequence_identifiers.',
                        default=False, required=False)
    parser.add_argument('-m', '--min_read_length', dest='min_read_length',
                        help='The minimum read length in bp. (Default = 90).',
                        required=False, default=90)
    parser.add_argument('-o', '--out', dest='out',
                        help='Output directory (Default=$HOME)', required=False,
                        default='~')
    parser.add_argument('-d', '--dna', dest='sequence', help='DNA sequence to \
                        summarize', default='TATGAAGGGCGATGAATGCTATCTGTCCTGTAGAATTATAGAATCGACTACGTTGGGGAACTAATGGACCAGACAACTCGCTTTGACTGACGTAGACGGCGTGTTGT',
                        required=False)
    args = parser.parse_args()
    if args.colorized:
        import Colorer
    if args.verbose:
        doc()
        log.basicConfig(format='%(levelname)s:  %(message)s', level=log.DEBUG)
        log.info('Output is verbose. Run with -q, --quiet flag to suppress full output.')
    else:
        log.basicConfig(format='%(levelname)s: %(message)s')
    ######################################################################
    ############      Call custom functions with arguments     ###########
    ######################################################################
    # Get list of read FASTQ files
    #######################################
    print(args.read_list, args.single, args.min_read_length)
    (forwards,reverses) = trimmomatic_template.parse_file(args.read_list,
                                                          args.single)
    #######################################
    # Sanity check read FASTQ files
    #######################################
    index = 0
    for fastq in forwards:
        f_opened_file=general.open_file(forwards[index])
        f_opened_file.close()
        forwards[index] = general.convert_to_full(forwards[index])
        if not args.single:
            r_opened_file=general.open_file(reverses[index])
            r_opened_file.close()
            reverses[index] = general.convert_to_full(reverses[index])
        index += 1
    #######################################
    # Make output directory
    #######################################
    (out_path,out_basename,out_ext)=general.parse_filename(args.out)
    out_dir=out_path + '/' + out_basename
    general.path_check(out_dir) # Sanity check directory
    out_dir= out_dir + '/' + args.project # final out directory is 'project_id'
    general.mk_out_sub_directory(out_dir)
    general.mk_out_sub_directory(out_dir + '/scripts')
    general.mk_out_sub_directory(out_dir + '/qsubs')
    #######################################
    # Write trimmomatic script
    #######################################
    convert=' | awk \'{if (NR % 4 == 1) {split($1, arr, \":\"); printf \"%s_%s:%s:%s:%s:%s#0/%s\\n\", arr[1], arr[3], arr[4], arr[5], arr[6], arr[7], substr($2, 1, 1), $0} else if (NR % 4 == 3){print \"+\"} else {print $0} }\' > '
    qsub_script = general.open_write_file(out_dir + '/qsubs/qsub_trimmomatic.sh')
    qsub_script.write('#!/bin/bash\n')
    index=0
    args.adapter = fasta-o-matic.run_steps(args.adapter,['wrap', 'new_line','header_whitespace'])
    for fastq in forwards:
        (f_path,f_basename,f_ext)=general.parse_filename(forwards[index])
        qsub_script.write('qsub -l mem=4G,h_rt=6:00:00 -pe single 16 '+ out_dir
                          + '/scripts/run_trimmomatic_' + f_basename + '.sh\n' )
        if not args.single:
            (r_path,r_basename,r_ext)=general.parse_filename(reverses[index])
        trim_script = general.open_write_file(out_dir
                                              + '/scripts/run_trimmomatic_'
                                              + f_basename + '.sh')
        trim_script.write('#!/bin/bash\n')
        # Convert headers
        if args.convert_header:
            trim_script.write('# Convert headers:\n')
            new_forward_fastq = out_dir + '/' + f_basename + '_h.fastq'
            trim_script.write('cat ' + forwards[index] + convert
                              + new_forward_fastq + '\n')
            forwards[index] = new_forward_fastq
            if not args.single:
                new_reverse_fastq = out_dir + '/' + r_basename + '_h.fastq'
                trim_script.write('cat ' + reverses[index] + convert
                                  + new_reverse_fastq + '\n')
                reverses[index] = new_reverse_fastq
        # Trim sequences
        trim_script.write('# Clean reads:\n')
        if not args.single:
            trim_script.write(trimmomatic_template.trim_template(
                                                                 forwards[index],
                                                                 reverses[index],
                                                                 args.adapter,
                                                                 out_dir))
        else:
            trim_script.write(trimmomatic_template.trim_template_single(forwards[index]))
            # Section in progress... (Remember to point to a SE adapter fasta file
            # by default)
        trim_script.close()
        index += 1
    qsub_script.close()
#    log.info("This should be verbose.")
#    log.warning("This is a warning.")
#    log.error("This is an error.")

##########################################################################
#####       Execute main unless script is simply imported     ############
#####                individual for functions                 ############
##########################################################################
if __name__ == '__main__':
    main()
    log.info('Done')
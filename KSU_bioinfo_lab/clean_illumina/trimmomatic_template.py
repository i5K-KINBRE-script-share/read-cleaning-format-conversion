#!/usr/bin/env python3
# Notes:
### Either max info OR sliding window
#strict=
#ILLUMINACLIP:${ADAPTERS}:2:30:12:1:true LEADING:3 MAXINFO:40:0.8 MINLEN:90
#relaxed=
#ILLUMINACLIP:${ADAPTERS}:2:30:12:1:true LEADING:3 MAXINFO:40:0.2 MINLEN:90
##########################################################################
#	USAGE: import trimmomatic_template
#   DESCRIPTION: Templates for running trimmomatic on Illumina read.
#   Created by Jennifer M Shelton
##########################################################################
import sys
import logging as log
import os
import re
import general
path_to_trimmomatic='/homes/bioinfo_software/Trimmomatic-0.33/trimmomatic-0.33.jar'
##########################################################################
##############                  Custom functions              ############
##########################################################################
def parse_file(read_list_file, single):
    '''
        Parse input read_list file. Check that it has the correct number of tab
        delimited columns and get list of forwards and/or reverses.
    '''
    forwards=[]
    reverses=[]
    input = general.open_file(read_list_file)
    if single:
        for line in input:
            forwards = (re.split(',', line))
        return(forwards,False)
    else:
        try:
            for line in input:
                line = (line.rstrip())
                if line:
                    (forward,reverse) = (re.split('\s+', line))
                    forwards = (re.split(',', forward))
                    reverses = (re.split(',', reverse))
            if not len(forwards) == len(reverses):
                log.error('Exiting because the number of forward read FASTQ files does not equal the number of reverse read FASTQ files. This may indicate that your read list is not properly formatted. It could indicate that you should use the -s --single flag to for single end Illumina reads or make sure to separate you comma separated list of forward and reverse reads with a single tab in your plain text read_list file.')
                sys.exit(0)
            else:
                return(forwards,reverses)
        except ValueError as e:
            log.error('"%(e)s... Use the -s --single flag to indicate single end Illumina reads or make sure to separate you comma separated list of foward and reverse reads with a single tab in your plain text read_list file."' % locals())
            sys.exit(0)
    input.close()
def trim_template(forward,reverse,adapter_fasta,baseout_fastq):
    '''
        Template for paired end scripts
    '''
    # ADAPTERS = TruSeq3-PE.fa for first dataset, or TruSeq-3-PE-2.fa for second dataset, or TruSeq-3-SE.fa to force 'simple mode' only (Supplementary table 2)
    # SW = sliding window quality cutoff, values from 2-35 were tested
    # S = stringency for maximum information mode, values from 0.1-0.9 (with 0.1 increments), 0.91-0.99 (with 0.01 increments) and 0.991 to 0999 (with 0.001 increments) were tested
    code='java -jar ' + path_to_trimmomatic + ' PE -threads 16 -phred33 ' + forward + ' ' + reverse + ' -baseout ' + baseout_fastq + ' ILLUMINACLIP:' + adapter_fasta + ':2:30:12:1:true LEADING:3 MAXINFO:40:0.8 MINLEN:90\n'
    return(code)
def trim_template_single(forward):
    '''
        Template for single end scripts
    '''
    code='java -jar ' + path_to_trimmomatic + ' SE -threads 16 -phred33 ' + forward + '\n'
    return(code)


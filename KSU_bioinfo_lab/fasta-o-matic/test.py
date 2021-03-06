#!/usr/bin/env python3
##########################################################################
#	USAGE: import test
#   DESCRIPTION: Tests for fasta_o_matic
#   Created by Jennifer M Shelton
##########################################################################
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
util_dir = os.path.abspath(parent_dir + '/../util')
sys.path.append(util_dir)
import logging as log
import general
import re
import fasta_o_matic
#######################################
# Correct values
#######################################
missing_last_new_line_fixed = [14, 3]
carriage_return_fixed = [4, 1]
unwrapped_fixed = [14, 3]
miswrapped_fixed = [15, 3]
first_word_not_unique = [14, 3]
header_not_unique = [9, 3]
#######################################
# Generic functions
#######################################
def get_count(fasta_file_name):
    '''
        Takes a FASTA file path and returns the number of lines and the
        number of sequences.
    '''
    newline_pattern = re.compile('.*\n')
    header_pattern = re.compile('^>.*')
    line_count = 0
    header_count = 0
    if sys.version_info > (3, 0): # Open without automatically converting
        # newlines to standard Unix newlines for python3.3+
        fasta_file = open(fasta_file_name, 'r',  newline='')
    else:
        fasta_file = general.open_file(fasta_file_name)
    for line in fasta_file:
        if newline_pattern.match(line):
            line_count = line_count + 1
        line = line.rstrip()
        if header_pattern.match(line):
            header_count = header_count + 1
    fasta_file.close()
    return(line_count,header_count)

def main_test(input_fasta, steps, fixed_name, out_dir, should_change=True):
    '''
        Compares number of lines and sequences from two ordered lists to test
        for equality.
    '''
    ####################################
    # Enable line below when developing
    ####################################
#    log.critical('# quick test ' + input_fasta + '...') # Enable when developing
    # missing last new_line test
    fasta_1_file_name = parent_dir + '/fasta/' + input_fasta
    if should_change: # if the job changed the fasta check that it did the
        # right change
        post_fasta_1_file_name = fasta_o_matic.run_steps(fasta_1_file_name, steps, out_dir) # reformat FASTA file
        (post_line_count,post_seq_count) = get_count(post_fasta_1_file_name)
        correct = fixed_name
        tbd = [post_line_count,post_seq_count]
        if correct == tbd:
            if not fasta_1_file_name == post_fasta_1_file_name: # NEVER DELETE THE ORIGINAL SAMPLE FILE
                os.remove(post_fasta_1_file_name)
            return(True)
        else:
            return(False)
    else: #check that the test finds a fatal error and returns a system exit
        try:
            post_fasta_1_file_name = fasta_o_matic.run_steps(fasta_1_file_name, steps, out_dir) # reformat FASTA file
        except SystemExit:
            return(True)
        else:
            return(False)
#######################################
# Check results of groups of
# reformatting job types
#######################################
def test_newline(out_dir):
    '''
        Test specifically FASTA files with broken newlines
    '''
    # missing last new_line test
    input_fasta = 'missing_last_new_line.fa'
    steps = ['new_line']
    fixed_name = missing_last_new_line_fixed
    if not main_test(input_fasta, steps, fixed_name, out_dir):
        return(False)
    # carriage return test
    input_fasta = 'carriage_return.fa'
    steps = ['new_line','header_whitespace']
    fixed_name = carriage_return_fixed
    if not main_test(input_fasta, steps, fixed_name, out_dir):
        return(False)
    # carriage return test2
    input_fasta = 'carriage_return.fa'
    steps = ['new_line']
    fixed_name = carriage_return_fixed
    if not main_test(input_fasta, steps, fixed_name, out_dir):
        return(False)
    return(True)

def test_wrapping(out_dir):
    '''
        Test specifically FASTA files with broken wrapping
    '''
    # miswrapped test
    input_fasta = 'miswrapped.fa'
    steps = ['wrap','header_whitespace']
    fixed_name = miswrapped_fixed
    if not main_test(input_fasta, steps, fixed_name, out_dir):
        return(False)
    # unwrapped test
    input_fasta = 'unwrapped.fa'
    steps = ['wrap']
    fixed_name = unwrapped_fixed
    if not main_test(input_fasta, steps, fixed_name, out_dir):
        return(False)
    return(True)
def test_unique(out_dir):
    '''
        Test specifically FASTA files header uniqueness issue
    '''
    # header_not_unique test.
    input_fasta = 'header_not_unique.fa'
    steps = ['unique']
    fixed_name = header_not_unique
    if not main_test(input_fasta, steps, fixed_name, out_dir, should_change=False):
        return(False)
    # first_word_not_unique test.
    input_fasta = 'first_word_not_unique.fa'
    steps = ['unique']
    fixed_name = first_word_not_unique
    if not main_test(input_fasta, steps, fixed_name, out_dir):
        return(False)
    return(True)
def test_all(out_dir):
    '''
        Test specifically FASTA files with either broken newlines or 
        broken wrapping using all three cleaning steps.
    '''
    # missing last new_line test ALL
    input_fasta = 'missing_last_new_line.fa'
    steps = ['new_line','wrap','header_whitespace', 'unique']
    fixed_name = missing_last_new_line_fixed
    if not main_test(input_fasta, steps, fixed_name, out_dir):
        return(False)
    # carriage return test ALL
    input_fasta = 'carriage_return.fa'
    steps = ['new_line','wrap','header_whitespace', 'unique']
    fixed_name = carriage_return_fixed
    if not main_test(input_fasta, steps, fixed_name, out_dir):
        return(False)
    # miswrapped test ALL
    input_fasta = 'miswrapped.fa'
    steps = ['new_line','wrap','header_whitespace', 'unique']
    fixed_name = miswrapped_fixed
    if not main_test(input_fasta, steps, fixed_name, out_dir):
        return(False)
    # unwrapped test ALL
    input_fasta = 'unwrapped.fa'
    steps = ['new_line','wrap','header_whitespace', 'unique']
    fixed_name = unwrapped_fixed
    if not main_test(input_fasta, steps, fixed_name, out_dir):
        return(False)

    return(True)

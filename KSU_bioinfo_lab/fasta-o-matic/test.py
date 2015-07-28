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

import general
import re
import fasta_o_matic

missing_last_new_line_fixed = [14,3]
carriage_return_fixed = [4,1]
unwrapped_fixed = [14,3]
miswrapped_fixed = [15, 3]
def get_count(fasta_file_name):
    '''
        Takes a FASTA file path and returns the number of lines and the
        number of sequences.
    '''
    newline_pattern = re.compile('.*\n')
    header_pattern = re.compile('^>.*')
    line_count = 0
    header_count = 0
    if sys.version_info > (3, 0):
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
def check_count(correct,tbd):
    '''
        Compares number of lines and sequences from to ordered lists to test 
        for equality.
    '''
    if correct == tbd:
        print('Is true!')
    else:
        print('Is false')

input_fasta = 'missing_last_new_line.fa'
steps = ['new_line','header_whitespace']
fixed_name = missing_last_new_line_fixed

def main_test(input_fasta, steps, fixed_name, out_dir):
    # missing last new_line test
    fasta_1_file_name = parent_dir + '/fasta/' + input_fasta
    (pre_line_count,pre_seq_count) = get_count(fasta_1_file_name)
    post_fasta_1_file_name = fasta_o_matic.run_steps(fasta_1_file_name, steps, out_dir)
    (post_line_count,post_seq_count) = get_count(post_fasta_1_file_name)
    print('# quick test ' + input_fasta)
    check_count(fixed_name, [post_line_count,post_seq_count])

def test_newline(out_dir):
    # missing last new_line test
    input_fasta = 'missing_last_new_line.fa'
    steps = ['new_line','header_whitespace']
    fixed_name = missing_last_new_line_fixed
    main_test(input_fasta, steps, fixed_name, out_dir)
    # carriage return test
    input_fasta = 'carriage_return.fa'
    steps = ['new_line','header_whitespace']
    fixed_name = carriage_return_fixed
    main_test(input_fasta, steps, fixed_name, out_dir)
    # carriage return test2
    input_fasta = 'carriage_return.fa'
    steps = ['new_line']
    fixed_name = carriage_return_fixed
    main_test(input_fasta, steps, fixed_name, out_dir)
    # carriage return test3
    input_fasta = 'carriage_return.fa'
    steps = ['wrap']
    fixed_name = carriage_return_fixed
    main_test(input_fasta, steps, fixed_name, out_dir)

def test_wrapping(out_dir):
    # miswrapped test
    input_fasta = 'miswrapped.fa'
    steps = ['wrap','header_whitespace']
    fixed_name = miswrapped_fixed
    main_test(input_fasta, steps, fixed_name, out_dir)
    # unwrapped test
    input_fasta = 'unwrapped.fa'
    steps = ['wrap']
    fixed_name = unwrapped_fixed
    main_test(input_fasta, steps, fixed_name, out_dir)

def test_all(out_dir):
    # missing last new_line test ALL
    input_fasta = 'missing_last_new_line.fa'
    steps = ['new_line','wrap','header_whitespace']
    fixed_name = missing_last_new_line_fixed
    main_test(input_fasta, steps, fixed_name, out_dir)
    
    # carriage return test ALL
    input_fasta = 'carriage_return.fa'
    steps = ['new_line','wrap','header_whitespace']
    fixed_name = carriage_return_fixed
    main_test(input_fasta, steps, fixed_name, out_dir)
    
    # miswrapped test ALL
    input_fasta = 'miswrapped.fa'
    steps = ['new_line','wrap','header_whitespace']
    fixed_name = miswrapped_fixed
    main_test(input_fasta, steps, fixed_name, out_dir)
    
    # unwrapped test ALL
    input_fasta = 'unwrapped.fa'
    steps = ['new_line','wrap','header_whitespace']
    fixed_name = unwrapped_fixed
    main_test(input_fasta, steps, fixed_name, out_dir)
    


# Line 31 only works with absolute paths (or at least paths without ~)
# test.test_all('/Users/jennifer_shelton/out_stanford_swc')
# test.test_newline('/Users/jennifer_shelton/out_stanford_swc')
# test.test_wrapping('/Users/jennifer_shelton/out_stanford_swc')


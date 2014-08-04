#!/usr/bin/perl
###############################################################################
#   
#	USAGE: perl convert_headers.pl
# Illumina header conversion (the code on line 27 is from  http://www.freelists.org/post/mira_talk/Metagenome-assembly,4)
#
#  Created by jennifer shelton
#
###############################################################################
use strict;
use warnings;
# use File::Basename; # enable manipulating of the full path
# use List::Util qw(max);
# use List::Util qw(sum);
# use Bio::SeqIO;
# use Bio::Seq;
# use Bio::DB::Fasta;
###############################################################################
##############                Initialize variables           ##################
###############################################################################
# my $dirname = dirname(__FILE__);
use File::Basename; # enable manipulating of the full path
my $read_file = $ARGV[0];
my (${filename}, ${directories}, ${suffix}) = fileparse($read_file,'\..*'); # break appart filenames

print  "#######################################################################\n############ Convert headers of illumina paired-end data ##############\n#######################################################################\n";
print "cat $read_file | awk \'{if (NR % 4 == 1) {split(\$1, arr, \":\"); printf \"%s_%s:%s:%s:%s:%s#0/%s\\n\", arr[1], arr[3], arr[4], arr[5], arr[6], arr[7], substr(\$2, 1, 1), \$0} else if (NR % 4 == 3){print \"+\"} else {print \$0} }\' > ${directories}${filename}_header.fastq\n";

###############################################################################
##############                      Run                      ##################
###############################################################################

print "done\n";


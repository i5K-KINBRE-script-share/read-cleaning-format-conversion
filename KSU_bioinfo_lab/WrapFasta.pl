#!/usr/bin/perl
###############################################################################
#   
#	USAGE: perl WrapFasta.pl [options]
#
#  Created by jennifer shelton
#
###############################################################################
use strict;
use warnings;
use File::Basename; # enable manipulating of the full path
# use List::Util qw(max);
# use List::Util qw(sum);
use Bio::SeqIO;
use Bio::Seq;
#use Bio::DB::Fasta;
use Getopt::Long;
use Pod::Usage;
###############################################################################
##############         Print informative message             ##################
###############################################################################
print "###########################################################\n";
print "#  WrapFasta.pl                                           #\n";
print "#                                                         #\n";
print "#  Created by Jennifer Shelton 04/21/14                   #\n";
print "#  https://github.com/i5K-KINBRE-script-share             #\n";
print "#  perl WrapFasta.pl -help # for usage/options            #\n";
print "#  perl WrapFasta.pl -man # for more details              #\n";
print "###########################################################\n";
###############################################################################
##############                get arguments                  ##################
###############################################################################
my $fasta;

my $man = 0;
my $help = 0;
GetOptions (
			  'help|?' => \$help, 
			  'man' => \$man,
			  'f|fasta:s' => \$fasta
              )  
or pod2usage(2);
pod2usage(1) if $help;
pod2usage(-exitstatus => 0, -verbose => 2) if $man;
# my $dirname = dirname(__FILE__);
###############################################################################
##############                        run                       ###############
###############################################################################
open (FASTA, '<', $fasta) or die "can't open $fasta !\n";
my (${filename}, ${directories}, ${suffix}) = fileparse($fasta,'\..*'); # break appart filenames
my $out = "${directories}${filename}_wrapped.fasta";
my $seq_out = Bio::SeqIO->new('-file' => ">$out",'-format' => 'fasta');
my $header;
$/=">";
while (<FASTA>)
{
    my ($header,@seq)=split/\n/;
    my $seq=join '', @seq;
    $seq =~ s/>//g; ## removed the > used as record separator
    $header =~ s/ //g; ## removed white space in headers because bioperl doesn't allow it in headers
	if ($header =~ />/){next}; ## skip blank first record
    my $seq_obj = Bio::Seq->new( -display_id => $header, -seq => $seq);
    $seq_out->write_seq($seq_obj);
    
}


print "done\n";
###############################################################################
##############                  Documentation                   ###############
###############################################################################
## style adapted from http://www.perlmonks.org/?node_id=489861 
__END__

=head1 NAME

WrapFasta.pl - a scripts that wraps lines of fasta file without wrapped sequences or with inconsistently wrapped sequences. NCBI recommends that FASTA sequences be wrapped and BioPerl requires this however not all tools create wrapped FASTA files. Your reformatted fasta file will start with the original filename and end with "_wrapped.fasta".

=head1 USAGE

perl WrapFasta.pl [options]

 Documentation options:
   -help    brief help message
   -man	    full documentation
 Required options:
   -f	     fasta file without wrapped sequences or with inconsistently wrapped sequences
   
=head1 OPTIONS

=over 8

=item B<-help>

Print a brief help message and exits.

=item B<-man>

Prints the more detailed manual page with output details and examples and exits.


=item B<-f, --fasta>

The fullpath for the fasta file without wrapped sequences or with inconsistently wrapped sequences. Wrapping sequence is recommended by NCBI for fasta format. Some programs will return errors if this is not done properly. Here are a couple examples of this type of error:
 
 "Each line of the fasta entry must be the same length except the last."
 
 "Each line of the qual file must be less than 65,536 characters."
 
If you are receiving a similar error from a program you are trying to run WrapFasta.pl will create a reformatted fasta file from your improperly wrapped file.

=back

=head1 DESCRIPTION

B<OUTPUT DETAILS:>

Your reformatted fasta file will start with the original filename and end with "_wrapped.fasta".


=cut

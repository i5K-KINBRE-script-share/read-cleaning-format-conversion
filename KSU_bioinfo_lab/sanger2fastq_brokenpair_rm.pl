#!/usr/bin/perl
use strict;
use warnings;
use File::Basename; # enable maipulating of the full path
############################################################################
#
# USAGE: sanger2fastq_brokenpair_rm.pl 
# Script output unbroken pairs and singletons, sequences with more than two template_ids in the anc file are removed
#
#
############################################################################

my (%header_hash,%key_hash,%extra_hash,%single_hash,@row,@timeData,$fastq,$fastqs);
my ($key,$value,$index,$file_out,$insert_size,$insert_sd,$template_id,$ti,$trace_end,$trace_name);
#my $outfile1= "/homes/bioinfo/Tcas/jobs/clean_list2.txt";
#my $outfile2= "/homes/bioinfo/Tcas/jobs/singles_list.txt";


######## list all files I am interested in #########
###my @files=`ls /homes/bioinfo/Tcas/sanger_reads/tribolium_castaneum_R*_bp_*.fastq`;
my @files=qw(/homes/bioinfo/Tcas/sanger_reads/anc.tribolium_castaneum.003 /homes/bioinfo/Tcas/sanger_reads/anc.tribolium_castaneum.002 /homes/bioinfo/Tcas/sanger_reads/anc.tribolium_castaneum.001); # default directory
################# find and count all template ids ##############
foreach(@files)
{
    open(IN_ANC,"<$_") or die $!; 	# you need to request a warning because we are opening with "open" not BioPerl
    my $count=0;
    while(<IN_ANC>)
    {
        if ($count==0) {$count++,next;}
        @row= split("\cI");
        #        ($insert_size,$insert_sd,$template_id,$ti,$trace_end,$trace_name)=($row[26],$row[27],$row[56],$row[57],$row[59],$row[61]); #file 4
        ($insert_size,$insert_sd,$template_id,$ti,$trace_end,$trace_name)=($row[29],$row[30],$row[53],$row[54],$row[56],$row[58]); #file 1-3
        if (!$header_hash{$template_id})
        {
            $header_hash{$template_id}=0;
        }
        $header_hash{$template_id}=$header_hash{$template_id}+1;
    }
}
@timeData = localtime(time);
print "stage 1: loop though anc partially done @timeData\n";

################# find and count all template ids ##############
open(IN_ANC,"</homes/bioinfo/Tcas/sanger_reads/anc.tribolium_castaneum.004") or die $!; 	# you need to request a warning because we are opening with "open" not BioPerl
while(<IN_ANC>)
{
    @row= split("\cI");
    ($insert_size,$insert_sd,$template_id,$ti,$trace_end,$trace_name)=($row[26],$row[27],$row[56],$row[57],$row[59],$row[61]); #file 4
    if(!$header_hash{$template_id})
    {
        $header_hash{$template_id}=0;
    }
    $header_hash{$template_id}=$header_hash{$template_id}+1;
}

@timeData = localtime(time);
print "stage 1: loop though anc done @timeData\n";

############ Id singles and duplicates ###############
foreach my $key ( keys %header_hash )
{
    my $temp_id_count=$header_hash{$key}; ### make histogram
    if(!$key_hash{$temp_id_count})
    {
        $key_hash{$temp_id_count}=0;
    }
    $key_hash{$temp_id_count}=$key_hash{$temp_id_count}+1;
    print "$key: $key_hash{$temp_id_count}\n";
    if ($header_hash{$key} != 2) ### id single and duplicates
    {
        $extra_hash{$key}=1;
    }
    else
    {
        $extra_hash{$key}=0;
    }
    if ($header_hash{$key} == 1)
    {
        $single_hash{$key}=1;
    }
    else
    {
        $single_hash{$key}=0;
    }
    
}
############## Print histogram ##################
foreach my $key ( keys %key_hash )
{
    print "$key : $key_hash{$key} \n";
}
############## print to single or dup files ###################
my @outfiles=`ls /homes/bioinfo/Tcas/sanger_reads/Trib_cast_R*00`; # default directory
foreach(@outfiles)
{
    chomp;
    s/\n//;
    open (OLD_FASTQ,'<', "$_") or die "Couldn't open $_: $!";
    #    my $filenames="${_}_good.fastq";
    open my $fastqs, '>>', "${_}_good.fastq" or die "Couldn't open ${_}_good.fastq: $!";
    #    my $filename="${_}_singles.fastq";
    open my $fastq, '>>', "${_}_singles.fastq" or die "Couldn't open ${_}_singles.fastq: $!";
    
    my $counter=0;
    $/ = "\@Template"; ##### set record seperator
    while (<OLD_FASTQ>) ##### loop through the FASTQ
    {
        if ($counter == 0){$counter=1;next;}
        else
        {
            if (/_id=.*_Insert_size/)
            {
                
                /_id=(.*)_Insert_size/; ### capture from ###    @Template_id=TBMAP0314_Insert_size=3500_Insert_sd=1500#/1
                if ($1)
                {
                    if ($extra_hash{$1}==0)
                    {
                        print  $fastqs "\@Template"; ### add back start of header
                        s/\@Template//g;
                        print  $fastqs "$_";
                    }
                    if ($single_hash{$1}==1)
                    {
                        print $fastq "\@Template";
                        s/\@Template//g;
                        print $fastq "$_";
                    }
                }
            }
        }
    }
}
@timeData = localtime(time);
print "stage 2: loop though fastq partially done @timeData\n";

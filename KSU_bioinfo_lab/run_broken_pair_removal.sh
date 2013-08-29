#!/bin/sh

#  run_broken_pair_removal.sh
#  USAGE: run_broken_pair_removal.sh [filenames_minus_1.fastq or _2.fastq]
#
#  Created by jennifer shelton on 8/7/13.

mkdir ~/job_logs_broken_pairs
##################  define variables #################################################

for fullpath in "$@"
do
filename="${fullpath##*/}"                      # Strip longest match of */ from start
dir="${fullpath:0:${#fullpath} - ${#filename}}" # Substring from 0 thru pos of filename
base="${filename%.[^.]*}"                       # Strip shortest match of . plus at least one non-dot char from end
ext="${filename:${#base} + 1}"                  # Substring from len of base thru end
if [[ -z "$base" && -n "$ext" ]]; then          # If we have an extension and no base, it's really the base
base=".$ext"
ext=""
fi

######################  begin  #################################################
cd ${dir}
mkdir ~/jobs_${filename}
echo "#!/bin/sh" > ~/jobs_${filename}/broken_pairs-h_${filename}.sh
echo "cd ${dir}" >> ~/jobs_${filename}/broken_pairs-h_${filename}.sh

#echo "## script converts to pre CASAVA 1.8 format for MIRA found from http://www.freelists.org/post/mira_talk/Metagenome-assembly,4 ##" >> ~/jobs_${filename}/broken_pairs-h_${filename}.sh
echo "cat ${filename}_1.fastq "'| awk '\''{if (NR % 4 == 1) {split($1, arr, ":"); printf "%s_%s:%s:%s:%s:%s#0/%s\n", arr[1], arr[3], arr[4], arr[5], arr[6], arr[7], substr($2, 1, 1), $0} else if (NR % 4 == 3){print "+"} else {print $0} }'\'''" > ${filename}_1_h.fastq" >> ~/jobs_${filename}/broken_pairs-h_${filename}.sh
echo "cat ${filename}_2.fastq "'| awk '\''{if (NR % 4 == 1) {split($1, arr, ":"); printf "%s_%s:%s:%s:%s:%s#0/%s\n", arr[1], arr[3], arr[4], arr[5], arr[6], arr[7], substr($2, 1, 1), $0} else if (NR % 4 == 3){print "+"} else {print $0} }'\'''" > ${filename}_2_h.fastq" >> ~/jobs_${filename}/broken_pairs-h_${filename}.sh

echo "######################  Remove broken pairs #################################################" >> ~/jobs_${filename}/broken_pairs-h_${filename}.sh

echo "CMD=\"perl /homes/sheltonj/abjc/scripts/broken_pair_removal.pl ${filename}_1_h.fastq ${filename}_2_h.fastq ${filename}_1_h_bp.fastq ${filename}_2_h_bp.fastq\"" >> ~/jobs_${filename}/broken_pairs-h_${filename}.sh


echo "echo \"\$CMD\" > ~/job_logs_broken_pairs/\$JOB_ID.cmd" >> ~/jobs_${filename}/broken_pairs-h_${filename}.sh
echo "echo \"broken_pairs_${filename}\" > ~/job_logs_broken_pairs/\$JOB_ID.data_in" >> ~/jobs_${filename}/broken_pairs-h_${filename}.sh
echo "echo \"broken_pairs\" > ~/job_logs_broken_pairs/\$JOB_ID.ref_in" >> ~/jobs_${filename}/broken_pairs-h_${filename}.sh
echo "eval \$CMD" >> ~/jobs_${filename}/broken_pairs-h_${filename}.sh
echo "cp /homes/sheltonj/durrettt/jobs_logs/stats.sh ~/job_logs_broken_pairs/" >> ~/jobs_${filename}/broken_pairs-h_${filename}.sh
echo "cd ~/job_logs_broken_pairs" >> ~/jobs_${filename}/broken_pairs-h_${filename}.sh
echo "bash ~/job_logs_broken_pairs/stats.sh" >> ~/jobs_${filename}/broken_pairs-h_${filename}.sh

echo "qsub -l h_rt=72:00:00,mem=10G -e ~/job_logs_broken_pairs -o ~/job_logs_broken_pairs -N clean_${base} ~/jobs_${filename}/broken_pairs-h_${filename}.sh" >> ${dir}broken_pairs-h_clean_jobs.txt


done

# bash /homes/bioinfo/Tcas/Clean_reads_for_assembly.sh /homes/bioinfo/Tcas/Tribolium20kb /homes/bioinfo/Tcas/Tribolium3kb /homes/bioinfo/Tcas/Tribolium8kb

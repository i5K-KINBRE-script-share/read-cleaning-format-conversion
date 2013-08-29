#!/bin/sh

#  run_prinseq.sh
#  USAGE: bash run_prinseq.sh [filenames_minus_R1_001_h.fastq or _R2_001_h.fastq]
#
#  Created by jennifer shelton on 4/8/13.
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
mkdir ~/job_logs_${filename}
echo "#!/bin/sh" > ~/jobs_${filename}/clean_prinseq-h_${filename}.sh
echo "cd ${dir}" >> ~/jobs_${filename}/clean_prinseq-h_${filename}.sh

#echo "## script converts to pre CASAVA 1.8 format for MIRA found from http://www.freelists.org/post/mira_talk/Metagenome-assembly,4 ##" >> ~/jobs_${filename}/clean_prinseq-h_${filename}.sh
echo "cat ${filename}_1.fastq "'| awk '\''{if (NR % 4 == 1) {split($1, arr, ":"); printf "%s_%s:%s:%s:%s:%s#0/%s\n", arr[1], arr[3], arr[4], arr[5], arr[6], arr[7], substr($2, 1, 1), $0} else if (NR % 4 == 3){print "+"} else {print $0} }'\'''" > ${filename}_1_h.fastq" >> ~/jobs_${filename}/clean_prinseq-h_${filename}.sh
echo "cat ${filename}_2.fastq "'| awk '\''{if (NR % 4 == 1) {split($1, arr, ":"); printf "%s_%s:%s:%s:%s:%s#0/%s\n", arr[1], arr[3], arr[4], arr[5], arr[6], arr[7], substr($2, 1, 1), $0} else if (NR % 4 == 3){print "+"} else {print $0} }'\'''" > ${filename}_2_h.fastq" >> ~/jobs_${filename}/clean_prinseq-h_${filename}.sh

echo "######################  Clean with Prinseq #################################################" >> ~/jobs_${filename}/clean_prinseq-h_${filename}.sh

echo "CMD=\"perl /homes/sheltonj/abjc/prinseq-lite-0.20.3/prinseq-lite.pl -verbose -fastq ${filename}_1_h.fastq -fastq2 ${filename}_2_h.fastq -min_len 90 -min_qual_mean 25 -trim_qual_type mean -trim_qual_rule lt -trim_qual_window 2 -trim_qual_step 1 -derep 1 -trim_qual_left 20 -trim_qual_right 20 -ns_max_p 1 -trim_ns_left 5 -trim_ns_right 5 -lc_method entropy -lc_threshold 70 -out_format 3  -no_qual_header -log ${filename}_paired.log\"" >> ~/jobs_${filename}/clean_prinseq-h_${filename}.sh


echo "echo \"\$CMD\" > ~/job_logs_${filename}/\$JOB_ID.cmd" >> ~/jobs_${filename}/clean_prinseq-h_${filename}.sh
echo "echo \"clean_prinseq_${filename}\" > ~/job_logs_${filename}/\$JOB_ID.data_in" >> ~/jobs_${filename}/clean_prinseq-h_${filename}.sh
echo "echo \"clean_prinseq\" > ~/job_logs_${filename}/\$JOB_ID.ref_in" >> ~/jobs_${filename}/clean_prinseq-h_${filename}.sh
echo "eval \$CMD" >> ~/jobs_${filename}/clean_prinseq-h_${filename}.sh
echo "cp /homes/sheltonj/durrettt/jobs_logs/stats.sh ~/job_logs_${filename}/" >> ~/jobs_${filename}/clean_prinseq-h_${filename}.sh
echo "cd ~/job_logs_${filename}" >> ~/jobs_${filename}/clean_prinseq-h_${filename}.sh
echo "bash ~/job_logs_${filename}/stats.sh" >> ~/jobs_${filename}/clean_prinseq-h_${filename}.sh

echo "qsub -l h_rt=24:00:00,mem=100G -e ~/job_logs_${filename} -o ~/job_logs_${filename} -N clean_${base} ~/jobs_${filename}/clean_prinseq-h_${filename}.sh" >> ${dir}clean_prinseq-h_clean_jobs.txt


done

# bash /homes/bioinfo/Tcas/Clean_reads_for_assembly.sh /homes/bioinfo/Tcas/Tribolium20kb /homes/bioinfo/Tcas/Tribolium3kb /homes/bioinfo/Tcas/Tribolium8kb
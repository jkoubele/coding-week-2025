#!/bin/bash


input_folder="/data/public/jkoubele/coding-week-2025/cluster_usage/data/GSE147319"
output_folder="/data/public/jkoubele/coding-week-2025/cluster_usage/output/GSE147319"

docker_image_path="/data/public/jkoubele/coding-week-2025/cluster_usage/custom_bioconductor.tar"
script_folder="/data/public/jkoubele/coding-week-2025/cluster_usage/scripts"
slurm_log_folder="/data/public/jkoubele/coding-week-2025/cluster_usage/slurm_logs"

for sub_folder in "$input_folder"/*; do
  sample_name=$(basename "$sub_folder")
  echo "Submitting sample $sample_name"
  sbatch --output="$slurm_log_folder"/%j_%x.log \
  --error="$slurm_log_folder"/%j_%x.err \
  /data/public/jkoubele/coding-week-2025/cluster_usage/single_cell_processing_job.sh \
  -i "$sub_folder" \
  -o "$output_folder"/"$sample_name" \
  -d "$docker_image_path" \
  -s "$script_folder"
done
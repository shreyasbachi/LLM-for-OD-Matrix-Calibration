#!/usr/bin/bash
#SBATCH --job-name=od_link_change                 # Name of your job
#SBATCH --mail-user=sbachira@asu.edu              # Replace with your email
#SBATCH --mail-type=ALL                           # Notifications for BEGIN, END, FAIL, etc.
#SBATCH --cpus-per-task=8                         # Number of CPU cores per task
#SBATCH -N 1                                      # Number of nodes
#SBATCH --mem=10G                                 # Memory required for the job
#SBATCH -t 2-00:00:00                             # Max time of 7 days (adjust as needed)
#SBATCH -p general                                # Partition name (default: general)
#SBATCH -q public                                 # QoS (default: public)
#SBATCH --output=/home/sbachira/llm_od/results/logs/od_link.log # Output file for job logs
#SBATCH --error=/home/sbachira/llm_od/results/logs/od_link.err
#SBATCH --get-user-env                            # Import the user's environment

# Navigate to the directory where your script is located
cd /home/sbachira/llm_od

# Activate the Conda environment
source activate openti

export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

export PATH=$HOME/.local/wine-build/bin:$PATH

#export HF_HOME=$SCRATCH/huggingface
#source ~/.bashrc

#echo "Using Hugging Face cache directory: $HF_HOME"

# Run your Python script with separate logs for standard output and error
python3 -u /home/sbachira/llm_od/pipeline/od_link.py > results/logs/od_link.log 2> results/logs/od_link.err

# Print the current date and time for record-keeping
date
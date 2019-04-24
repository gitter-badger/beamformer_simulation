#!/bin/bash

# Make sure to request only the resources you really need to avoid cueing
#SBATCH -t 10:00
#SBATCH --mem-per-cpu=4G
#SBATCH -n 1

# Do the analysis for each subject. This should correspond with the SUBJECTS
# variable below.
#SBATCH --array=1-2

# Find the current subject
SUBJECT=${SUBJECTS[$SLURM_ARRAY_TASK_ID - 1]}

# Location to write the logfile to
LOG_FILE=logs/simulate_raw-$SLURM_ARRAY_TASK_ID.log

# Load the python environment
module load anaconda3
module load mesa

# Tell BLAS to only use a single thread
export OMP_NUM_THREADS=1

# Start a virtual framebuffer to render things to
Xvfb :99 -screen 0 1400x900x24 -ac +extension GLX +render -noreset &
export DISPLAY=:99.0

# Run the script
srun -o $LOG_FILE python ../simulate_raw.py -v $SLURM_ARRAY_TASK_ID -n 1

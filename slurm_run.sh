#!/bin/bash
#SBATCH -J purification
#SBATCH -o %j.out
#SBATCH -e %j.err
#SBATCH -p CPU-Small
#SBATCH -N 1
#SBATCH -n 40
#SBATCH --time=120:00:00

module load python/3.8.8

if [ $SLURM_SUBMIT_DIR ]
then 
    cd $SLURM_SUBMIT_DIR
fi

declare -a pids

for i in {001..15}; do
    python bosonic_main.py 0.003 0.$i
    pids+=($!)
done

wait "${pids[@]}"


#!/bin/bash
 
#SBATCH --job-name=4jym_monomer
#SBATCH --auks=yes
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=100000
#SBATCH --nodes=1
#SBATCH --nodelist=slurm-gpu-04
#SBATCH --error=namd_error_%j.log


. /etc/profile.d/modules.sh
module load cuda-toolkit
module load mpich
module load gcc

namd="/filer/projekte/pymol_course/dynamics/NAMD_3.0b7_Linux-x86_64-multicore-CUDA/"

equi_prefix="step4_equilibration"
prod_prefix="step5_production"
prod_step="step5"


srun ${namd}/charmrun ${namd}/namd3 +p${SLURM_CPUS_PER_TASK} ${equi_prefix}.inp > ${equi_prefix}.out

cnt=1
cntmax=10

while [ $cnt -le $cntmax ]; do
    if [ $cnt -eq 1 ]; then
        outputname="${prod_step}_${cnt}"
        sed "s/${prod_prefix}/${outputname}/" ${prod_prefix}.inp > ${prod_step}_run.inp
    else
        cntprev=$((cnt - 1))
        inputname="${prod_step}_${cntprev}"
        outputname="${prod_step}_${cnt}"
        sed "s/${equi_prefix}/${inputname}/" ${prod_prefix}.inp | \
            sed "s/${prod_prefix}/${outputname}/" > ${prod_step}_run.inp
    fi
    
    srun ${namd}/charmrun  ${namd}/namd3 +p${SLURM_CPUS_PER_TASK} ${prod_step}_run.inp > ${outputname}.out

    cnt=$((cnt + 1))
done


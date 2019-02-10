#!/bin/bash
#SBATCH -t 0-05:00:00
#SBATCH -p gpu
#SBATCH -o log/1024_Eu_1
cd ..
python train.py --ngf 32 --ndf 32 --niter 125 --niter_decay 25 --name 1024_Eu_1 --dataroot ../../image_standardization_t7505/1024c_3d --model unpaired_revgan3d --which_model_netG edsr5_1 --dataset_mode unaligned --input_nc 1 --output_nc 1 --gpu_ids 0 --display_id -1 --serial_batches 2>&1 >> log/1024_Eu_1.log 
wait

conda create --prefix /home/coder/envs/3dgs -y

conda activate /home/coder/envs/3dgs

conda env update --file environment.yml --prune

conda install conda-forge::colmap -y
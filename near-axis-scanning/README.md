# near-axis-scanning

# Compiling QSC
Documenting some tips/tricks when compiling QSC on Stellar


Run the following commands:
module load gcc/4.8.5
module load openblas/0.3.x
module load cmake/pppl/3.24.2
module load gcc-toolset/10

Next, run these commands. You may need to install in a different order as there are prerequisites for these.
module load openmpi/gcc-toolset-10/4.1.0
module load hdf5/gcc/openmpi-4.1.0/1.10.6
module load netcdf/gcc/hdf5-1.10.6/4.7.4

Next, from within the qsc/ directory, run 'cmake .'

Run './clean_cmake' before compiling. This is especially needed when making any changes to the modules. Doing this can easily resolve errors, though its not exactly clear why. Could be due to  cmake using cached versions of the modules instead of the updated ones? Not sure...

Finally, run 'make'. This should work.


# Setting up DESC
Based on the DESC Docs. Ensure that DESC is installed with CPU+GPU support by executing the following:

module load cudatoolkit/11.7
module load anaconda3/2022.5

CONDA_OVERRIDE_CUDA="11.2" conda create --name desc-env jax "jaxlib==0.4.1=cuda112*" -c conda-forge
conda activate desc-env

The next steps are better summarized on the DESC page.
https://desc-docs.readthedocs.io/en/stable/installation.html

For most normal setups after initial installation just run the following:
module load cudatoolkit/11.7
module load anaconda3/2022.5
conda activate desc-env


# Setting up REGCOIL
module load gcc/4.8.5 
module load openblas/0.3.x
module load cmake/pppl/3.24.2
module load gcc-toolset/10
module load openmpi/gcc-toolset-10/4.1.0
module load hdf5/gcc/openmpi-4.1.0/1.10.6
module load netcdf/gcc/hdf5-1.10.6/4.7.4
module load intel/2022.2.0

Theres currently a problem in the REGCOIL library such that the Stellar cluster is not identified during compilation. This causes an error because specific flags are needed when compiling REGCOIL on the cluster. Go into the toplevel Makefile and change line 71 (where the hostname is checked to determine which cluster is being run on ). Change the checked hostname from 'stellar' to 'stellar-intel.princeton.edu'. Ensure there are no quotes and no spaces added like so:

else ifeq ($(HOSTNAME),stellar-intel.princeton.edu)

Next, to run the tests we need to modify the job command (time needs to be set in the srun command) so go into the REGCOIL folder, open the toplevel Makefile and edit line 81 to add in a runtime of 5 minutes so the enviornmental variable looks like this:

REGCOIL_COMMAND_TO_SUBMIT_JOB = srun -N 1 -n 1 -c 8 -q debug --mem 8G -t 00:05:00

This specifically sets the variable in the case we are on the STELLAR cluster, and the variable is used to issue commands in the tests after compilation during the 'make test' command.




So the chain is:
QSC -> DESC -> BNORM -> REGCOIL -> EVAL



# Checklist
- Get QSC compiled and working (DONE - Passes All Tests)
- Run QSC to generate a database of 10,000 random samples (Not Done)
- Integrate QSC with Python to perform a scan that saves passing configurations to file (Not Done)
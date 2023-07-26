# near-axis-scanning


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




# Checklist
- Get QSC compiled and working (DONE - Passes All Tests)
- Run QSC to generate a database of 10,000 random samples (Not Done)
- Integrate QSC with Python to perform a scan that saves passing configurations to file (Not Done)
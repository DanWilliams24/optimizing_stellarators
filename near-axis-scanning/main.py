# must have installed pyQsc with `pip install qsc` in order to use this!
import subprocess
from qsc import Qsc
import netCDF4 as nc
from qsc_config import QSConfig
import numpy as np
import matplotlib.pyplot as plt
from desc import set_device
# need to do this before importing other DESC stuff so JAX initializes properly
try:
    set_device("gpu")
except subprocess.CalledProcessError:
    print("No GPU Found. Using CPU instead")


from desc.equilibrium import Equilibrium
from desc.objectives import get_fixed_boundary_constraints
from desc.plotting import (
    plot_comparison,
    plot_fsa,
    plot_section,
    plot_surfaces,
    plot_qs_error,
)
'''
TODO - Implement code to call QSC and wrap output in format parse-able by DESC via PyQSC
TODO - Need to exec C++ QSC code to do scans from python - use os
TODO - need to compile REGCOIL and run tests with a generated vmec file from DESC
TODO - test creating a scan, loading a eq from said scan into desc, optimize, then port through regcoil
TODO - AUTOMATE FULL framework
'''
FILENAME = "qsc_in.random_scan_small"
OUTPUT_LOCATION = "/home/dw1978/optimizing_stellarators/near-axis-scanning/qsc/examples/"

def do_scan(config):
    FILENAME = "qsc_in.random_scan_small"
    config.write_input_file(f"{FILENAME}_new")
    test = subprocess.run(["xqsc", f"{FILENAME}_new"])
    print("Scan Completed. The exit code was: %d" % test.returncode)
#takes 2.02 min on CPU to optimize 1 eq (two slow)
#takes 53 sec on a GPU to optimize 1 eq (better but still too slow)


def main():
    """
    config = QSConfig(FILENAME)
     #modify scan based on some hidden knowledge
    config["max_seconds"] = 5

    # lets now do a scan for N seconds
    do_scan(config)

    # next read in the netcdf file reporting scan results as a Dataframe?

    #See if python is equipped to handle multi configuration scan object
    qsc_eq = Qsc.from_cxx("qsc_out.random_scan_small_new.nc")


    """
    from desc.vmec import VMECIO

    qsc_eq = Qsc.from_paper("precise QA")
    ntheta = 75
    r = 0.35
    desc_eq = Equilibrium.from_near_axis(
        qsc_eq,  # the Qsc equilibrium object
        r=r,  # the finite radius (m) at which to evaluate the Qsc surface to use as the DESC boundary
        L=8,  # DESC radial resolution
        M=8,  # DESC poloidal resolution
        N=8,  # DESC toroidal resolution
        ntheta=ntheta,
    )
    eq_fit = desc_eq.copy()  # copy so we can see the original Qsc surfaces later

    # get the fixed-boundary constraints, which include also fixing the pressure and fixing the current profile (iota=False flag means fix current)
    constraints = get_fixed_boundary_constraints(iota=False)
    print(constraints)

    # solve the equilibrium
    desc_eq.solve(
        verbose=3,
        ftol=1e-2,
        objective="force",
        maxiter=100,
        xtol=1e-6,
        constraints=constraints,
    )

    # Save equilibrium as .h5 file
    VMECIO.save(eq, "./SOLOVEV_output.nc")
    

    '''
    So for the framework, we generate configurations with QSC, then we solve EQ with DESC

    This will produce a VMEC file given to BNORM via a different shell env. Finally, we load REGCOIL AND COMPUTE 
    '''

    

if __name__ == "__main__":
    main()

import subprocess
import desc
import time
from datetime import datetime
from qsc import Qsc
import numpy as np
import matplotlib.pyplot as plt
from desc import set_device
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

import desc.io  # used for loading and saving data
# used to save equilibrium objects as VMEC-formatted .nc files
from desc.vmec import VMECIO
'''
Given a NEAR AXIS Expansion QSC input file, this program will run xqsc, convert the output to VMEC (via DESC?)
 and then move it through BNORM and REGCOIL.

 This experiment will test
  - Whether QSC -> REGCOIL process can be done autonomously
  - How quickly such a framework computes for 1 configuration
  - Whether this approach is scalable enough for direct application to an Optomitrist Algorithm vs a scan



  Methodology. One can treat this program as a abstract state machine where states are:
    Near Axis Solve -> DESC to VMEC -> BNORM Field Calculation -> REGCOIL Execution

'''



def get_timestamp():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %I:%M:%S")
    timestamp = dt_string.replace("/", "_").replace(" ", "_").replace(":", "_")
    return timestamp


# Given a QSC input file, run the QSC executable and return the name of the output file
def near_axis_solve(qsc_input_file):
    
    test = subprocess.run(["xqsc", f"{qsc_input_file}"])
    print("Scan Completed. The exit code was: %d" % test.returncode)
    
    return f"qsc_out.{qsc_input_file.replace('qsc_in.', '')}.nc"


# Given a QSC output file, use PyQSC to convert to DESC equillibrium, solve that equilibrium from the magnetic axis, 
# then output the solved Equillbrium
def convert_to_desc_eq(qsc_output_file):
    qsc_eq = Qsc.from_cxx(qsc_output_file)
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

    #does the equilibrium still need to be solved if already optimized through QSC?

    #===============================================================================#
    # get the fixed-boundary constraints, which include also fixing the pressure and 
    # fixing the current profile (iota=False flag means fix current)
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
    #===============================================================================#
    return desc_eq

# Given a DESC Equillibrium, output the solved Equillbrium as a VMEC file
def convert_to_vmec(desc_eq):
    timestamp = get_timestamp()
    output_name = f"./SOLOVEV_output_{timestamp}.nc"
    VMECIO.save(desc_eq, output_name)
    #We now have a file SOLOVEV_output.nc which is the equivalent Equilibrium solution in the VMEC coordinates and data format.
    return output_name

def calculate_bnorm(bnorm_input):
    pass

def main():
    pass



if __name__ == "__main__":
    main()

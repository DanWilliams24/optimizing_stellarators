# must have installed pyQsc with `pip install qsc` in order to use this!
from qsc import Qsc
import numpy as np
import matplotlib.pyplot as plt
from desc import set_device
# need to do this before importing other DESC stuff so JAX initializes properly
set_device("gpu")
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


def do_scan(parameters):
    pass

#takes 2.02 min on CPU to optimize 1 eq (two slow)
#takes 53 sec on a GPU to optimize 1 eq (better but still too slow)


def main():
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
    desc_eq.save("DESC_from_NAE_precise_QA_output.h5")


if __name__ == "__main__":
    main()
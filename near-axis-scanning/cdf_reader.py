import subprocess
from qsc import Qsc
import netCDF4 as nc
import numpy as np
import pandas as pd


class CDFReader:
    def __init__(self, filename) -> None:
        self.filename = filename
        self.data = nc.Dataset(self.filename)
        self.template_eq = {

        }
        self.eqs = []
        #print("Variables:")
        #print([self.data.dimensions[x].size for x in self.data.variables.keys()])
        #nfp = self.data['nfp']
        #print(f"nfp: {nfp[:]}")
        print(self.data['n_scan'])

    def get_eqs():
        arrays = []
        non_scalar_arrays = reader.get_non_scalar_arrays()



    def print_variables(self):
        print("Variables:")
        for variable in self.data.variables.keys():
            print(variable)

    def print_dimensions(self):
        print("Dimensions:")
        for dimension in self.data.dimensions.keys():
            print(f"{dimension}: {self.data.dimensions[dimension].size}")

    def get_non_scalar_arrays(self):
        non_scalar_arrays = {}
        for variable in self.data.variables.keys():
            if not self.data.variables[variable].shape:  # Check if the variable is non-scalar
                continue
            non_scalar_arrays[variable] = self.data.variables[variable][:]
        return non_scalar_arrays

    def close(self):
        self.data.close()

if __name__ == "__main__":
    reader = None
    try:
        reader = CDFReader("qsc_out.random_scan_small_new.nc")
        eqs = []
        col_names = []
        #reader.print_variables()
        non_scalar_arrays = reader.get_non_scalar_arrays()
        for variable, data in non_scalar_arrays.items():
            print(variable, type(data), type(data[0]), len(data))
            if(len(data) == 12138):
                if variable not in ["scan_R0c","scan_R0s","scan_Z0c", "scan_Z0s"]:
                    col_names.append(variable.replace("scan_", ""))
                    print(f"adding {variable}")
                    eqs.append(list(data))
        
        eqs = np.asarray(eqs)
        print(eqs.shape)
        print(eqs.T.shape)

        #compute the transpose so that each row represents one equillibrium
        eqillibrium_scan_data = pd.DataFrame(eqs.T, columns=col_names)

        print(eqillibrium_scan_data)
        print(eqillibrium_scan_data.describe())
        print(eqillibrium_scan_data.columns)
        #reader.print_dimensions()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        reader.close()
    '''
    #columns_oi = 
    eqs =[]
    for variable, data in non_scalar_arrays.items():
        print(variable, type(data), len(data))
        #print(f"\nArray: {variable}")
        #print(len(data))
        #print(type(data))
        if(len(data) == 12138):
            #print(data)
            if(type(list(data)[0]) != float):
                pass
            eqs.append(list(data)[0])

    #print(eqs)
    
    eqs = np.asarray(eqs)
    #print(eqs.shape)
    eqs = eqs.T
    #print(eqs.T)

    '''
    




'''

the possible input parameters to pyQSC are:

rc: the cosine components of the axis radial component

zs: the sine components of the axis vertical component

rs: the sine components of the axis radial component

zc: the cosine components of the axis vertical component

nfp: the number of field periods

etabar: a scalar that specifies the strength of the first order magnetic field modulus
scan_eta_bar

sigma0: the value of the function sigma at phi=0, which is 0 for stellarator-symmetry
scan_sigma0

B0: the strength of the magnetic field on-axis

I2: the second derivative of the current with respect to the radial variable r

sG: sign of the Boozer function G

spsi: sign of the toroidal flux function Psi

nphi: toroidal resolution specifying the number of points in a grid along the axis

B2s: a scalar that specifies the strength of the sine component of the second order magnetic field modulus, 0 for stellarator-symmetry
scan_B2s

B2c: a scalar that specifies the strength of the cosine component of the second order magnetic field modulus
scan_B2c

p2: the second derivative of the pressure with respect to the radial variable r, usually negative
scan_p2

order: a string that specifies the order of the expansion, “r1”, “r2” or “r3”. For “r3” only the X3c1, Y3c1 and Y3s1 components are calculated (see section 3 of [LandremanSengupta2019])

stel = Qsc(rc=[1, 0.155, 0.0102], zs=[0, 0.154, 0.0111], nfp=2, etabar=0.64, order='r2', B2c=-0.00322)'''
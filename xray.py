import os, numpy
from scipy.interpolate import UnivariateSpline

datapath=os.path.join(os.path.dirname(os.path.abspath(__file__)),"transmission_data")

class Transmission():
    def __init__(self, name, energies, absorption_lengths_um, density=1.0):
        self.name=name
        self.energies=numpy.array(energies)
        self.absorption_lengths_um=absorption_lengths_um
        self.density=density
        
    def transmission(self, energies, length_um=1, density=None):
        if density is None: density = self.density
        length_um = length_um*density/float(self.density)
        return numpy.exp(-length_um/numpy.interp(energies, self.energies, self.absorption_lengths_um))
        
class Optic():
    def __init__(self, name, energies, transmission_data, solid_angle=1):
        self.name=name
        self.energies=numpy.array(energies)
        self.transmission_data=transmission_data
        self.solid_angle=solid_angle
        
    def transmission(self, energies, solid_angle=None):
        if solid_angle is None: solid_angle=self.solid_angle
        transmission_data = self.transmission_data*solid_angle/self.solid_angle
        return numpy.interp(energies, self.energies, transmission_data)
        
def read_transmission_files():
    datapath=os.path.join(os.path.dirname(os.path.abspath(__file__)),"transmission_data")
    dirList=os.listdir(datapath)
    transmission_dict={}
    for fname in dirList:
        if '.txt' not in fname:continue
        data = numpy.loadtxt(os.path.join(datapath,fname))
        name=fname[0:-4]
        transmission_dict[name]=Transmission(name, data[:,0], data[:,1])
    return transmission_dict

def read_optic_files():
    datapath=os.path.join(os.path.dirname(os.path.abspath(__file__)),"optic_data")
    dirList=os.listdir(datapath)
    optic_dict={}
    for fname in dirList:
        if '.txt' not in fname:continue
        data = numpy.loadtxt(os.path.join(datapath,fname))
        name=fname[0:-4]
        optic_dict[name]=Optic(name, data[:,0], data[:,1])
    return optic_dict

def plasma_source_spectrum(energies, N0, T):
    """ energy, array of energies in eV 
    N0 photons/(eV steradian shot),
    T characteristic energy/temperature (eV) """
    return N0*numpy.exp(-energies/T)

def materials_transmission(energies, materials_thickness):
    flux = numpy.ones_like(energies)
    for material,thickness in materials_thickness.iteritems():
        flux*=materials[material].transmission(energies, thickness)
    return flux

def source_optic_materials(N0,T, optic_name, materials_thickness, solid_angle=None, energies = None):
    optic = optics[optic_name]
    if energies is None: energies = optic.energies
    return plasma_source_spectrum(energies, N0, T)*optic.transmission(energies, solid_angle)*materials_transmission(energies, materials_thickness)

materials=read_transmission_files()
optics=read_optic_files()
        
            

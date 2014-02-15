import os, numpy
from scipy.interpolate import UnivariateSpline

datapath=os.path.join(os.path.dirname(os.path.abspath(__file__)),"transmission_data")

class Material():
    def __init__(self, name, energies, absorption_lengths_um, density=1.0):
        self.name=name
        self.energies=numpy.array(energies)
        self.absorption_lengths_um=absorption_lengths_um
        self.density=density
        
    def transmission(self, energies, length_um=1, density=None):
        if density is None: density = self.density
        length_um = length_um*density/float(self.density)
        return numpy.exp(-length_um/numpy.interp(energies, self.energies, self.absorption_lengths_um))
    
    def absorbtion(self, energies, length_um=1, density=None):
        return 1-self.transmission(energies, length_um, density)
        
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
    
class PlasmaSource():
    def __init__(self, name, e_pulse, N0, T):
        self.name=name
        self.e_pulse=e_pulse
        self.N0=N0
        self.T=T
    
    def spectrum(self, energies, e_pulse):
        N0 = numpy.interp(e_pulse, self.e_pulse, self.N0)
        T =  numpy.interp(e_pulse, self.e_pulse, self.T)
        return N0*numpy.exp(-numpy.array(energies)/T)
    
#    def spectrum(self, energies, e_pulse):
#        N0 = numpy.interp(e_pulse, self.e_pulse, self.N0)
#        T =  numpy.interp(e_pulse, self.e_pulse, self.T)
#        T2=T*0.5
#        return numpy.exp(6000/T-6000/T2)*N0*numpy.exp(-numpy.array(energies)/T)*(energies>6000)+N0*numpy.exp(-numpy.array(energies)/T2)*(energies<6000)
            
def read_material_files():
    datapath=os.path.join(os.path.dirname(os.path.abspath(__file__)),"transmission_data")
    dirList=os.listdir(datapath)
    material_dict={}
    for fname in dirList:
        if '.txt' not in fname:continue
        data = numpy.loadtxt(os.path.join(datapath,fname))
        name=fname[0:-4]
        material_dict[name]=Material(name, data[:,0], data[:,1])
    return material_dict

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

def read_source_files():
    datapath=os.path.join(os.path.dirname(os.path.abspath(__file__)),"source_data")
    dirList=os.listdir(datapath)
    source_dict={}
    for fname in dirList:
        if '.txt' not in fname:continue
        data = numpy.loadtxt(os.path.join(datapath,fname))
        name=fname[0:-4]
        source_dict[name]=PlasmaSource(name, data[:,0], data[:,1], data[:,2])
    return source_dict    


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

def source_optic_materials(e_pulse, optic_name, materials_thickness, solid_angle=None, energies = None, source_name = "water_jet_2013"):
    optic = optics[optic_name]
    if energies is None: energies = optic.energies
    return sources[source_name].spectrum(energies, e_pulse)*optic.transmission(energies, solid_angle)*materials_transmission(energies, materials_thickness)

def source_optic_materials_absorber(e_pulse, optic_name, materials_thickness, solid_angle=None, energies = None, absorber_material='Bi', absober_length_um=2, source_name = "water_jet_2013"):
    return materials[absorber_material].absorbtion(energies, absober_length_um)*source_optic_materials(e_pulse, optic_name, materials_thickness, solid_angle, energies, source_name)
    
materials=read_material_files()
optics=read_optic_files()
sources=read_source_files()
        
            

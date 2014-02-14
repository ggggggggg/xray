import xray, numpy, pylab

# put materials and thickness in microns in m dictionary
m={}
m['Air']=1e5
m['Kapton']=25*4
m['Al']=10

N0 = 1
T = 2000 #K


pylab.figure()
for optic_name, optic in xray.optics.iteritems():
    energies = numpy.linspace(optic.energies[0], optic.energies[-1])
    flux = xray.source_optic_materials(N0,T, optic_name, m, energies=energies)
    pylab.plot(energies,flux,label=optic_name)
pylab.xlabel('energy (eV)')
pylab.ylabel('flux (arb)')
pylab.legend()
pylab.xlim(3000,25000)


#pylab.figure()
#for name, material in xray.materials.iteritems():
#    pylab.plot(material.energies, material.transmission(material.energies), label=material.name)
#pylab.legend()
pylab.figure()
energies=numpy.linspace(1000,30000,100)
pylab.plot(energies, xray.materials_transmission(energies, m))
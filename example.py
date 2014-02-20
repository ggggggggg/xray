import xray, numpy, pylab

# put materials and thickness in microns in m dictionary
m={}
m['Air']=2e5
m['Kapton']=25*8
m['Al']=20
m['Water']=120
m['Fe']=0.4

e_pulse = {"XOSpolycapillary_1":3.2,"XOSpolycapillary_2":4.125}

pylab.figure()
for optic_name, optic in xray.optics.iteritems():
    energies = numpy.linspace(optic.energies[0], optic.energies[-1],1000)
    flux = xray.source_optic_materials_absorber(e_pulse[optic_name], optic_name, m, energies=energies, absorber_length_um=2)
    pylab.plot(energies,flux,label="%s, %d mJ"%(optic_name, e_pulse[optic_name]))
pylab.xlabel('energy (eV)')
pylab.ylabel('flux (arb)')
pylab.legend()
pylab.xlim(3000,15000)
pylab.title(repr(m))
pylab.minorticks_on()
pylab.grid()
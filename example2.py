import xray, numpy, pylab


data = numpy.loadtxt("other_data/20130605_iron_tris_15eVbins_p_pulse_average_120pixels.spectrum")
energies = data[:,0]
counts = data[:,1]

optic_ratio = xray.optics["XOSpolycapillary_2"].transmission(energies)/xray.optics["XOSpolycapillary_1"].transmission(energies)

e_pulse_ratio = xray.sources['water_jet_2013'].spectrum(energies, 5.45)/xray.sources['water_jet_2013'].spectrum(energies, 3.2)

counts2 = counts*optic_ratio*e_pulse_ratio

i1=460
i2=490
pylab.figure()
pylab.plot(energies, counts, label='XOS1')
pylab.plot(energies, counts2, label='XOS2')
pylab.xlabel('energy (eV)')
pylab.ylabel('flux (arb)')
pylab.legend()
pylab.xlim(0,25000)
pylab.minorticks_on()
pylab.grid()
pylab.title('frac counts in energy [%d,%d], XOS1 %0.3f, XOS2 %0.3f'%(energies[i1],energies[i2], counts[i1:i2].sum()/counts.sum(), counts2[i1:i2].sum()/counts2.sum()))

print("XOS1 %d, XOS2 %d, %0.2f"%(counts.sum(), counts2.sum(), counts.sum()/counts2.sum()))




data = numpy.loadtxt("other_data/1500x80um jet.spectrum")
energies = data[:,0]
counts = data[:,1]

optic_ratio = xray.optics["XOSpolycapillary_2"].transmission(energies)/xray.optics["XOSpolycapillary_1"].transmission(energies)

e_pulse_ratio = xray.sources['water_jet_2013'].spectrum(energies, 4.75)/xray.sources['water_jet_2013'].spectrum(energies, 3.2)

counts2 = counts*optic_ratio*e_pulse_ratio

i1=260
i2=290
pylab.figure()
pylab.plot(energies, counts, label='XOS1')
pylab.plot(energies, counts2, label='XOS2')
pylab.xlabel('energy (eV)')
pylab.ylabel('flux (arb)')
pylab.legend()
pylab.xlim(0,25000)
pylab.minorticks_on()
pylab.grid()
pylab.title('frac counts in energy [%d,%d], XOS1 %0.3f, XOS2 %0.3f'%(energies[i1],energies[i2], counts[i1:i2].sum()/counts.sum(), counts2[i1:i2].sum()/counts2.sum()))

print("XOS1 %d, XOS2 %d, %0.2f"%(counts.sum(), counts2.sum(), counts.sum()/counts2.sum()))
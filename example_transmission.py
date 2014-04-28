import xray, numpy, pylab

# put materials and thickness in microns in m dictionary
m={}
m['Cr']=12
m['Fe']=0.4
energies = numpy.arange(50,24950,100)
transmission = xray.materials_transmission(energies, m)

import kwant
# For plotting
from matplotlib import pyplot
import numpy as np


# Lattice constant
a=1
# Hopping parameter
t=1.0
# Magnetic field
B= 1*10**(-3)

Sav=np.zeros((2,2))

sys = kwant.Builder()
sqlat = kwant.lattice.square(a)

## Construct the rectangle for the Sinai billiard ###
def sinai(position):
    (x, y) = position
    return (0 <= x < 200 and 0 <= y < 200)
	
sys[sqlat.shape(sinai, (0, 0))] = 4
sys[sqlat.neighbors()] = -1	

	
def hopx(site1, site2, B):
        # The magnetic field is controlled by the parameter B
        y = site1.pos[1]
        return -t * np.exp(-1j * B * y)       

sys[sqlat.shape(sinai, (0, 0))] = 4 * t 
    # hoppings in x-direction
sys[kwant.builder.HoppingKind((1, 0), sqlat, sqlat)] = hopx
    # hoppings in y-directions
sys[kwant.builder.HoppingKind((0, 1), sqlat, sqlat)] = -t


### Cut the corner of the rectangle to create the Sinai billiard ###

def in_hole(site):
    (x, y) = site.pos / a - (0, 0)  # position relative to centre
    return x**2/100**2+y**2/125**2< 1
for site in filter(in_hole, list(sys.sites())):
    del sys[site]  

#kwant.plot(sys)

# Attach the leads
lead_symmetry = kwant.TranslationalSymmetry([1,0])
for start, end in [(100,105)]:                      ## [m] Edivan, o intervalo antigo era [95,110]
	lead = kwant.Builder(lead_symmetry)
	lead[(sqlat(0, y) for y in range(start, end))] = 4
	lead[sqlat.neighbors()] =-1
	sys.attach_lead(lead)

lead_symmetry = kwant.TranslationalSymmetry([0,1])  ## [n]O potencial esta aqui 
for start, end in [(95,100)]:
 	lead = kwant.Builder(lead_symmetry)
 	lead[(sqlat(x, 0) for x in range(start, end))] = 4
 	lead[sqlat.neighbors()] =-1	
	
	
sys.attach_lead(lead)
sys = sys.finalized()

# Plot the system
kwant.plot(sys)



# Check the dimension of S-matrix for the lowest and highest energy values
print("Lower:")
smat=kwant.smatrix(sys,0.4,[B]) 
print(smat)
    
print("Upper:")
smat=kwant.smatrix(sys,0.6,[B])
print(smat)


outF = open("cond.dat", "w")

# Run the loop over the energy range (generating 2500 conductance values)   
for i in range(2500):
	print(i)
	enr=0.4 + 8.e-5*i
	smat=kwant.smatrix(sys, enr, [B])
	#Ps=kwant.physics.two_terminal_shotnoise(smat) # Calcula o Ruído de Disparo
	sm=smat.data
	Sav=Sav+sm

	cond=smat.transmission(1, 0) # Calcula a condutância

#   Write energy and conductance values in the file    
	outF.write("%s \n" %(str(cond))) ### Aqui, no lugar de "cond" vc deve colocar "Ps" no caso do Ruído.
outF.close()


Sav=Sav/2500
St=Sav.getH()
print("Average S-matrix:")
print(Sav)

#compute_conductance(sys, enr_init, enr_fin,fluxes=[0])

#local_dos = kwant.ldos(sys, energy=.6)

#from matplotlib import pyplot
#pyplot.plot(energies, conductances)
#pyplot.show()
#kwant.plotter.map(sys, local_dos, num_lead_cells=10)


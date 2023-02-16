import kwant
from matplotlib import pyplot
import numpy as np


# Lattice constant
a=1
#Hopping parameter
t=1.0
#Magnetic field
B= 1* 10**(-3)
#Largura e Comprimento da Região central
L=290

W=110

#Potencial
V= 2.3 * 10 **(-1)
w=4

Sav=np.zeros((2,2))                                     ## Matriz 2x2 com n=1 e m=1

print(V)          

def stadium(position):
    x,y = position
    x= max(abs(x)-180,0)
    return x**2+ y**2 < 110**2  and 0<=x< L and 0<=y<W

def fita (position):                                    # Posição da Barreira (Fita)
    (x,y)=position
    return ( 98 <= x < 108 and 110 <= y <110+w)

sys = kwant.Builder()
sqlat = kwant.lattice.square(a)
sys [sqlat.shape(stadium,(0,0))] = 4
sys[sqlat.shape(fita,(98,110))]=4 + V                   # Aqui, você declara a Barreira (Fita)
sys [sqlat.neighbors()] = -1

#kwant.plot(sys)

def hopx(site1, site2, B):
    #O parametro B controla o campo magnético
    y = site1.pos[1]
    return -t * np.exp(-1j * B * y)

sys [sqlat.shape(stadium,(0,0))] = 4 * t

    # hoppins in x - direction
sys[kwant.builder.HoppingKind((1,0), sqlat,sqlat)]= hopx
    # hoppins in y - direction
sys[kwant.builder.HoppingKind((0,1), sqlat,sqlat)]= - t


#Corte o o semi - stadium para criar o quarto do Bilhar de Stadium
def in_hole(site):
    x, y = site.pos/a-(0,0)   # position relative to centre
    #x= max(abs(x)-10,0)
    return -L <=x<0  and  0 <=y<110

for site in filter(in_hole, list(sys.sites())):
    del sys[site]

#kwant.plot(sys)

# Anexando os Leads.

lead_symmetry=kwant.TranslationalSymmetry([0,1])        # [n] guia com o  potencial.
for start, end in [(98,108)]:
    lead=kwant.Builder(lead_symmetry)
    lead[(sqlat(x,0)for x in range (start,end))]= 4
    lead[sqlat.neighbors()]= -1
    sys.attach_lead(lead)

    #sys.attach_lead(lead.reversed())

#sys.attach_lead(lead)
lead_symmetry=kwant.TranslationalSymmetry([0,-1])       # [m] guia ideal.
for start, end in [(203,223)]:
    lead=kwant.Builder(lead_symmetry)
    lead[(sqlat(x,0)for x in range (start,end))]= 4
    lead[sqlat.neighbors()]= -1
    sys.attach_lead(lead)



sys=sys.finalized()

kwant.plot(sys)


# Check the dimension of S-matrix for the lowest and highest energy values 
print("Lower:")
smat=kwant.smatrix(sys,0.4,[B]) 
print(smat)
    
print("Upper:")
smat=kwant.smatrix(sys,0.6,[B])
print(smat)



outF = open("cond.dat", "w")            # Aqui, você renomeia seu arquivo como desejar.


# Run the loop over the energy range (generating 2500 conductance values)   
for i in range(2500):
	print(i)
	enr=0.4 + 8.e-5*i
	smat=kwant.smatrix(sys, enr, [B])
	#Ps=kwant.physics.two_terminal_shotnoise(smat)      # Aqui, você habilita para calcular a Potencia do Ruido
	#sm=smat.data                                       ##  Descomente se deseja calcular a média da matriz
	#Sav=Sav+sm                                         ##  Descomente se deseja calcular a média da matriz

	cond=smat.transmission(1, 0)

#   Write energy and conductance values in the file    
	outF.write("%s \n" %(str(Ps)))
outF.close()

#Sav=Sav/2500                   ##  Descomente se deseja calcular a média da matriz
#St=Sav.getH()                  ##  Descomente se deseja calcular a média da matriz
#print("Average S-matrix:")     ##  Descomente se deseja calcular a média da matriz
#print(Sav)                     ##  Descomente se deseja calcular a média da matriz




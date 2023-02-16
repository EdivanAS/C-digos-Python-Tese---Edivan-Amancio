import kwant
from matplotlib import pyplot
import numpy as np


# Lattice constant
a=1
#Hopping parameter
t=1.0
#Magnetic field
B=0#1*10**(-3)
#Largura e Comprimento da Região central
L=290

W=110

Sav=np.zeros((2,2))

print(B)          

def stadium(position):
    x,y = position
    x= max(abs(x)-180,0)
    return x**2+ y**2 < 110**2  and 0<=x< L and 0<=y<W


sys = kwant.Builder()
sqlat = kwant.lattice.square(a)
sys [sqlat.shape(stadium,(0,0))] = 4
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

lead_symmetry=kwant.TranslationalSymmetry([0,1]) # suporta n canais
for start, end in [(95,100)]: 
    lead=kwant.Builder(lead_symmetry)
    lead[(sqlat(x,0)for x in range (start,end))]= 4
    lead[sqlat.neighbors()]= -1
    sys.attach_lead(lead)

    #sys.attach_lead(lead.reversed())

#sys.attach_lead(lead)
lead_symmetry=kwant.TranslationalSymmetry([0,-1])
for start, end in [(200,205)]:                      # suporta m canais
    lead=kwant.Builder(lead_symmetry)
    lead[(sqlat(x,0)for x in range (start,end))]= 4
    lead[sqlat.neighbors()]= -1
    sys.attach_lead(lead)



sys=sys.finalized()

kwant.plot(sys)


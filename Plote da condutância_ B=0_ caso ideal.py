## Graficos - Stadium , Sinai e RMT

## Metodo - Edivan - arquivo (.dat) ##

import numpy as np
import matplotlib.pyplot as plt
import math
sqrt=np.lib.scimath.sqrt
#plt.style.use('ggplot')
#from numpy import loadtxt

### ---- Eq. (3.18)---- Disertação --- n = 1, m = 1,2,3 ---- beta = 1 ###

def P(g,a,b):
      g1=np.array([i for i in g if a<=i<=b])
      f1=beta/2 * m * g **[(beta*m/2)-1]
      return f1
beta=1
m=3
a=0.00001
b=1
g = np.linspace(a,b,10000)                                  # Note que aqui, temos 10000 realizações.

def plot_hist(dat = ''):                                    # Aqui, refere-se ao cálculo das distribuições da condutância.
  arquivo = open(dat,'r').readlines()           
  dados   = [float(i[:-2]) for i in arquivo] 
  altura, largura = np.histogram(dados, density = True)
  centro = (largura[:-1] + largura[1:])/2.0
  return [centro, altura]


x, y   = plot_hist('gSn1m3Tudo.dat')      # Aqui você chama a simulação  de g do Sinai
x1, y1 = plot_hist('gEn1m3Tudo.dat')      # Aqui voce chama a simulação de g do Estádio.
plt.figure(figsize = (5, 5))
plt.plot(g, P(g,a,b),color='black',lw=2)#, label = 'TMA')
plt.plot(x1, y1, 'o', color='red',markersize=np.sqrt(100))#, label='Estádio')
plt.plot(x, y, 's',markersize=np.sqrt(100))#, label='Sinai')
plt.xlabel(r'$g$', fontsize = 22)
plt.ylabel(r'$F^{(1)}_g(g)$', fontsize =22 )
plt.legend(title=r' $n=1,m=3$',title_fontsize = 20, fontsize=18)
plt.yticks(np.arange(0,2.5,0.5))
plt.xlim([0, 1.01])
plt.ylim([0, 2.0])
plt.tick_params(labelsize=17)
plt.show()


### ----- Função de Heaviside ----###

def H(x,alfa=1.0):
    h=np.heaviside(x,alfa)
    return h


### ------ (Eq. 3.19)----- Dissertação ---- beta= 1 --- ###

def F_19(g,a,b):
       
    g1= np.array([i for i in g if a<= i <=b])
    K=sqrt((g1-1)**1).real
    f1=(3/2)*(g1-2 * K * H(g1-1))

    return f1

a=0
b=2
g= np.linspace(0,b,10000)

def plot_hist(dat = ''):
  arquivo = open(dat,'r').readlines()           
  dados   = [float(i[:-2]) for i in arquivo] 
  altura, largura = np.histogram(dados, density = True)
  centro = (largura[:-1] + largura[1:])/2.0
  return [centro, altura]


x, y   = plot_hist('gSn2m2Tudo.dat')
x1, y1 = plot_hist('gE1n2m2NOVO.dat')
plt.figure(figsize = (5,5))
plt.plot(g, F_19(g,a,b), lw = 2, color='black')#, label ='($ n=2, m=2$)')
plt.plot(x1, y1, 'o', markersize=np.sqrt(100),color='red')
plt.plot(x, y, 's',markersize=np.sqrt(100))
plt.xlabel(r'$g$', fontsize = 22)
plt.ylabel(r'$F^{(1)}_g(g)$', fontsize = 22)
plt.legend(title=r' $n=2,m=2$',title_fontsize = 20)#, fontsize=14)
plt.yticks(np.arange(0,2.5,0.5))
plt.xticks(np.arange(0,2.5,0.5))
plt.xlim([0, 2.0])
plt.ylim([0, 2.0])
plt.tick_params(labelsize=17)
plt.show()

### ------ (Eq. 3.20)n2m3 ----- Dissertação ----  beta= 1 --- ###


def F_20(g,a,b):
    #sqrt=np.lib.scimath.sqrt
    
    g1= np.array([i for i in g if a<= i <=b])
    #K=sqrt((g1-1)**1).real
    f1=(3/2)*(g1**2 - 4*(g1-1)* H(g1-1))

    return f1

a=0
b=2
g= np.linspace(0,b,10000)

def plot_hist(dat = ''):
  arquivo = open(dat,'r').readlines()           
  dados   = [float(i[:-2]) for i in arquivo] 
  altura, largura = np.histogram(dados, density = True)
  centro = (largura[:-1] + largura[1:])/2.0
  return [centro, altura]


x, y   = plot_hist('gSn2m3Tudo.dat')
x1, y1 = plot_hist('gEn2m3TJ.dat')
plt.figure(figsize = (5, 5))
plt.plot(g, F_20(g,a,b), lw = 2, color='black')#, label = '($ n=2, m=3$)')
plt.plot(x1, y1, 'o', markersize=np.sqrt(100),color='red')
plt.plot(x, y, 's',markersize=np.sqrt(100))
plt.xlabel(r'$g$', fontsize = 22)
plt.ylabel(r'$F^{(1)}_g(g)$', fontsize = 22)
plt.legend(title=r'$n=2,m=3$',title_fontsize = 20)#, fontsize=14)
plt.yticks(np.arange(0,2.5,0.5))
plt.xticks(np.arange(0,2.5,0.5))
plt.xlim([0, 2.0])
plt.ylim([0, 2.0])
plt.tick_params(labelsize=17)
plt.show()

### ------ (Eq. 3.21)n3m3 ----- Dissertação -----  beta= 1 --- ###


def F_21(g,a,b):
    sqrt=np.lib.scimath.sqrt
    g1=np.array([i for i in g if 0 <= i <=a])
    g2=np.array([i for i in g if a < i <= b])

    f1=(6/7)* g1 **(7/2)
    
    K=sqrt((g2-2)**5).real

    f2=(3/28)*(35*g2**3 - 175*g2**2+273*g2-125.0-8*K*(g2+5)*H(g2-2))

    f=np.concatenate((f1,f2), axis=None)
    return f
a=1
b=3
g= np.linspace(0,b,2500)

def plot_hist(dat = ''):
  arquivo = open(dat,'r').readlines()           
  dados   = [float(i[:-2]) for i in arquivo] 
  altura, largura = np.histogram(dados, density = True)
  centro = (largura[:-1] + largura[1:])/2.0
  return [centro, altura]


x, y   = plot_hist('gSn3m3TJ.dat')
x1, y1 = plot_hist('gEn3m3JT.dat')
plt.figure(figsize = (5,5))
plt.plot(g, F_21(g,a,b), lw = 2, color='black')#, label = 'Análitico')
plt.plot(x1, y1, 'o', markersize=np.sqrt(100),color='red')#, label='Estádio')
plt.plot(x, y, 's', markersize=np.sqrt(100))#, label='Sinai'
plt.xlabel(r'$g$', fontsize = 22)
plt.ylabel(r'$F^{(1)}_g(g)$', fontsize = 22)
plt.legend(title=r'$n=3,m=3$',title_fontsize = 20)#, fontsize=14)
plt.yticks(np.arange(0,2.0,0.5))
plt.xticks(np.arange(0,3.5,0.5))
plt.xlim([0, 3.0])
plt.ylim([0, 1.5])
plt.tick_params(labelsize=17)
plt.show()

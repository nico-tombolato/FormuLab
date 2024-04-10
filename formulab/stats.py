from IPython.display import display, Math

import sympy as sp
import numpy as np
from scipy import stats as st

from formulab import config as cfg
from formulab.objects import *

def magnitude(x):   #returns the order of magnitude of x
    if x==0: return 0
    return int(sp.floor(sp.log(abs(x),10)))

def set_cov(x,y, cov=0):
    if cov==0: cov=np.cov(x.values,y.values)[0][1]
    x.set_cov(y,cov)
    y.set_cov(x,cov)



def u_st(nu, sdm=1, alpha=cfg.alpha):
    return st.t.interval(1-alpha, float(nu), loc=0, scale=float(sdm))[1]

def f_dst(nun, nud, alpha=cfg.alpha):
    return st.f.ppf(q=1-alpha, dfn=nun, dfd=nud)

def t_test_final(x, y, nu, t, alpha):
    t_st = u_st(nu, 1, alpha)
    display(Math(rf'\text{{Región de rechazo: }}\, RR = \{{\lvert t \rvert \geq t_{{{alpha/2},{nu}}}\}}'))
    display(Math(rf'RR = \{{\lvert t \rvert \geq {t_st:.3f}\}}'))
    if abs(t) < t_st: display(Math(rf't \not\in RR \quad \text{{Se acepta la Hipótesis nula, }} \, {x} = {y} \, \text{{ con un nivel de significancia }}\, \alpha = {alpha}')) 
    else: display(Math(rf't \in RR \quad \text{{Se rechaza la Hipótesis nula, }} \, {x} \neq {y} \, \text{{ con un nivel de significancia }}\, \alpha = {alpha}')) 

def t_test_varparam(x, y, alpha=cfg.alpha):
    t = (x.val-y.val)/x.sdm
    display(Math(rf'\text{{Se realiza la comparacion con un nivel de significancia }}\, \alpha = {alpha}'))
    display(Math(rf'\text{{Hipótesis nula }}\, H_0: {x} = {y} \quad \text{{Hipótesis alternativa }}\, H_a: {x} \neq {y}'))
    display(Math(rf't = {sp.latex((x-y)/x.sym.sdm)} = {t}'))
    
    t_test_final(x, y, x.nu, t, alpha)

def t_test_varvar(x, y, alpha=cfg.alpha):
    f=x.sd**2/y.sd**2
    F=f_dst(x.nu, y.nu, alpha=alpha)
    display(Math(rf'\text{{Se analiza si las varianzas son homogéneas con un nivel de significancia }}\, \alpha = {2*alpha}'))
    display(Math(rf'\text{{Hipótesis nula }}\, H_0: {x.sym.sd} = {y.sym.sd} \quad \text{{Hipótesis alternativa }}\, H_a: {x.sym.sd} \neq {y.sym.sd}'))
    display(Math(rf'f = {sp.latex(x.sym.sd**2/y.sym.sd**2)} = {f}'))
    display(Math(rf'\text{{Región de rechazo: }}\, RR = \{{f \geq F_{{{alpha},{x.nu},{y.nu}}} \, o \, f \leq F_{{{1-alpha},{x.nu},{y.nu}}} \}}'))
    display(Math(rf'RR = \{{f \geq {F:.3f} \, o \, f \leq {1/F:.3f} \}}'))
    
    nus=sp.Symbol(rf'\nu')
    if f < F and f > 1/F: 
        display(Math(rf'f \not\in RR \quad \text{{Se acepta la Hipótesis nula, }}\, {x.sym.sd} = {y.sym.sd} \, \text{{ con un nivel de significancia }}\, \alpha = {2*alpha}')) 
        
        display(Math(rf'\text{{Se procede a la comparación para varianzas homogéneas con un nivel de significancia }}\, \alpha = {alpha}'))
        t = float((x.val-y.val)/(sp.sqrt((x.nu*x.sd**2+y.nu*y.sd**2)*(1/x.n+1/y.n)/(x.n+y.n-2))))
        s_p=sp.Symbol('s_p')
        nu=x.n+y.n-2
        display(Math(rf't = {sp.latex((x.sym.val-y.sym.val)/(s_p*sp.sqrt(1/x.sym.n+1/y.sym.n)))}\quad con \, {s_p**2} = {sp.latex((x.sym.nu*x.sym.sd**2+y.sym.nu*y.sym.sd**2)/(nus))}\,;\,{nus}={x.sym.n+y.sym.n-2}={nu}'))
        display(Math(rf't={t}'))
    else:
        display(Math(rf'f \in RR \quad \text{{Se rechaza la Hipótesis nula, }} \, {x.sym.sd} \neq {y.sym.sd} \, \text{{ con un nivel de significancia }}\, \alpha = {2*alpha}'))
        
        display(Math(rf'\text{{Se procede a la comparación para varianzas no homogéneas con un nivel de significancia }}\, \alpha = {alpha}'))
        t = float((x.val-y.val)/(sp.sqrt(x.sd**2/x.n+y.sd**2/y.n)))
        nuf=(x.sd**2/x.n+y.sd**2/y.n)**2/((x.sd**2/x.n)**2/x.nu+(y.sd**2/y.n)**2/y.nu)
        nu=np.floor(nuf)
        display(Math(rf't = {sp.latex((x.sym.val-y.sym.val)/(sp.sqrt(x.sym.sd**2/x.sym.n+y.sym.sd**2/y.sym.n)))}={t}'))
        display(Math(rf'{nus}={sp.latex((x.sym.sd**2/x.sym.n+y.sym.sd**2/y.sym.n)**2/((x.sym.sd**2/x.sym.n)**2/x.sym.nu+(y.sym.sd**2/y.sym.n)**2/y.sym.nu))}= {nuf}\approx {nu}'))
    
    t_test_final(x, y, nu, t, alpha)
    
def t_test(x, y, alpha=cfg.alpha):
    if type(y) is param: t_test_varparam(x, y, alpha)
    elif type(y) in [var, func]: t_test_varvar(x, y, alpha)
    else: print('Invalid type of data')



# def round_to_1(x): #returns x rounded to one figure
#     if x == 0: return 0
#     return round(x, -magnitude(x))
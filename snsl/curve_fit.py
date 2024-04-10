import scipy as sc

def func_fit(f):
    return sc.optimize.curve_fit(f.lamb, f.x.val, f.y.val, p0=[p.val for p in f.adjParams], sigma=f.y.sdm)
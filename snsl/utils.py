import sympy as sp
import numpy as np
import pandas as pd

# String handling Utils
def name_splitter(name):
    if type(name) is str:
        name = sp.latex(sp.parsing.sympy_parser.parse_expr(name.replace('\\',''))).replace('{', '').replace('}', '')
    else: name = str(name)
    split = name.split('_')
    argument = split[0]
    subindex = split[-1]
    printname = rf'{argument}_{{{subindex}}}'
    name = rf'{argument}_{subindex}'
    if (subindex == argument and len(split)!=2) or subindex == '':
        subindex = ''
        printname = argument
        name = argument
    return argument, subindex, argument+subindex, printname, name

def flatten(name):
    return name.replace('{', '').replace('}', '')


##file utils
def read_file(fName, varnames='', sep=','):
    table = pd.read_csv(fName, sep=sep, header=None)
    if not is_number(table.loc[0][0]):
        table = pd.read_csv(fName, sep=sep, header=0)
    ncols = table.shape[1]
    if ncols%2==1:
        print('Invalid structure')
    nvars=int(ncols/2)
    
    var=np.empty(nvars, dtype=object)

    if varnames:
        varnames=varnames.split(sep)
        for i in range(0,nvars):
            table.rename({rf'{i}':varnames[i], rf'{nvars+i}': rf'u_{varnames[i]}'}) 
    return table, nvars

def save_file(fName, tableDict, sep=','):
    table = pd.DataFrame.from_dict(tableDict)
    table.to_csv(fName, index=False, sep=sep)
    
def file_from_obj(fName, varlists=[], sep=','):
    tableDict={}
    tableDict.update({rf'{V.name} [{V.unit}]': V.val for V in varlists})
    tableDict.update({rf'{V.sym.u} [{V.unit}]': V.u for V in varlists})
    save_file(fName, tableDict, sep=sep)


#Ease of use Utils
def var_dict(values=None, val=None, sd=None, sdm=None, n=None, nu=None, u=None, valr=None, u_st=None):
    if n is None:
        if nu is not None: n = nu + 1
    else: nu = n - 1
    if sdm is None:
        if u is None: pass
        else: sdm = u
    return {'values':values, 'val':val, 'sd':sd, 'sdm':sdm, 'n':n, 'nu':nu, 'u':u, 'valr':valr, 'u_st':u_st}
    
   
#Other Utils
def is_number(string):
    if string is not str: string=str(string)
    return string.replace('.','',1).replace('-','',1).isdigit()


## Array utils
def rm(arr):
    return np.array([x for x in arr if not pd.isnull(x)])


# def is_in_list(list1, list2):
#     return lambda list1, list2: any(i in list2 for i in list1)


# def get_xy(x,y):
#     if isinstance(x, pd.core.series.Series):
#         x=utils.rm(x)
#     if isinstance(y, pd.core.series.Series):
#         y=utils.rm(y)
        
#     if isinstance(x, (list, np.ndarray)) and isinstance(y, (list, np.ndarray)):
#         if len(y) == 0:
#             y=[i for i in range(0,len(x))]
#         elif len(x) == 0:
#             x=[i for i in range(0,len(y))]
#         else: print('cannot forward empty arrays'); return
        
#         x, y = obj.var_list('x', x, vbs=0), obj.var_list('y', y, vbs=0)
#     elif type(x) is not obj.var_list or type(x) is not obj.var_list:
#         print('x, y must be of same type')
#     return x,y
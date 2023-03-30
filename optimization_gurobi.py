import gurobipy as gp
from gurobipy import GRB
opt_model = gp.Model('opt_Q')
x1=opt_model.addVar(vtype=GRB.CONTINUOUS)

min_H=opt_model.addConstr(32.14+1.28*x1-0.32*x1*x1>=row['Min_H'], "min_H")
max_N=opt_model.addConstr(1.215+0.385*x1-0.002*x1*x1<=row['Max_N'], "max_N")
max_Q=opt_model.addConstr(x1<=10,"max_Q")
 
obj = 1.392+19.18*x1-1.362*x1*x1
opt_model.setObjective(obj, GRB.MAXIMIZE)

opt_model.optimize()

row['Recomendation_GUROBI']="Рекомендуется изменить подачу Q на "+str(round(opt_model.getAttr("X", opt_model.getVars())[0],2))+". Будет достигнут максимальный КПД:"+str(round(obj.getValue(),1))

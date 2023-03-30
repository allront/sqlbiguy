from scipy.optimize import minimize
from scipy.optimize import NonlinearConstraint
import numpy as np

#Целевая функция - максимизация КПД
def objective(x, sign=-1.0):
    x1 = x[0]
    return sign*(1.392+19.18*x1-1.362*x1**2-0.014*x1**3)

#Ограничения
##Ограничение на H
con = lambda x: 32.14+1.28*x[0]-0.32*x[0]**2
nlc = NonlinearConstraint(con, row['Min_H'],np.inf)

##Ограничение на N
con2 = lambda x: 1.215+0.385*x[0]-0.002*x[0]**2-0.002*x[0]**3
nlc2 = NonlinearConstraint(con2, -np.inf,row['Max_N'])

cons = [nlc,nlc2]

#Начальное значение Q
x0 = row['Сonsumption_Q']

#Граничные условия Q
b1 = (0,10)
b2 = (-np.inf,+np.inf)
bnds= (b1,b2)

#Оптимизация SLSQP
sol = minimize(objective, x0, method='SLSQP', bounds = bnds, constraints = cons)
solution = sol['x']
evaluation = -1.0*objective(solution)

row['Recomendation_SCIPY']="Рекомендуется изменить подачу Q на "+str(round(solution[0],2))+". Будет достигнут максимальный КПД:"+str(round(evaluation,1))

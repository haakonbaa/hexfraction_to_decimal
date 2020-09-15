import matplotlib.pyplot as plt
from math import *

# Extra function
ln = log
lg = log10

func = "ln(1+y)+sin(x*y)-ln(5)"
point_x = 0
point_y = 4
delta =  0.001

points_x = [point_x]
points_y = [point_y]



def evaluate(func,x,y):
    return eval(func)

best_angle = 1.5*pi
for k in range(100):
    a = best_angle-(pi*0.5)
    b = best_angle+(pi*0.5)
    lowest_error = inf
    for j in range(25):
        for i in range(0,100):
            angle = (i/100)*(b-a)+a
            x = point_x + delta*cos(angle)
            y = point_y + delta*sin(angle)
            error = evaluate(func,x,y)
            if abs(error) < lowest_error:
                lowest_error = abs(error)
                best_angle = angle
        a = best_angle+( (b-a)*(1/50) )
        b = best_angle-( (b-a)*(1/50) )
    point_x += delta*cos(best_angle)
    point_y += delta*sin(best_angle)

    points_x.append(point_x)
    points_y.append(point_y)

points_x2 = []
points_y2 = []
point_x = 0
point_y = 4
best_angle = 0.5*pi
for k in range(100):
    a = best_angle-(pi*0.5)
    b = best_angle+(pi*0.5)
    lowest_error = inf
    for j in range(25):
        for i in range(0,100):
            angle = (i/100)*(b-a)+a
            x = point_x + delta*cos(angle)
            y = point_y + delta*sin(angle)
            error = evaluate(func,x,y)
            if abs(error) < lowest_error:
                lowest_error = abs(error)
                best_angle = angle
        a = best_angle+( (b-a)*(1/50) )
        b = best_angle-( (b-a)*(1/50) )
    point_x += delta*cos(best_angle)
    point_y += delta*sin(best_angle)

    points_x2.append(point_x)
    points_y2.append(point_y)


#plt.plot(points_x,points_y)
#plt.plot(points_x2,points_y2)

fx = [*points_x2[::-1],*points_x]
fy = [*points_y2[::-1],*points_y]

def derive(px,py):
    d = []
    for i in range(len(px)-1):
        d.append((py[i+1]-py[i])/(px[i+1]-px[i]))
    d.append( (py[-1]-py[-2])/(px[-1]-px[-2]) )
    return d


fyd1 = derive(fx,fy)
fyd2 = derive(fx,fyd1)



plt.plot(fx,fy)
plt.plot(fx,fyd1)
plt.plot(fx,fyd2)

#plt.plot([0,1,-1,2,-2,3,-3,4,-4],[1,2,3,4,5,6,7,8,9])

plt.show()

def poly_order(c):
    while len(c)>0 and c[-1]==0:
        c.pop()
    if(c==[]):
        return 0
    return len(c)-1

def poly_coefficient(c,i):
    while len(c)>0 and c[-1]==0:
        c.pop()
    if(c==[]):
        return 0
    if(i >= len(c)):
        return 0
    else:
        return c[i]

def poly_evaluate(c,v):
     answer = 0
     o = len(c)-1
     while o>=0:
         answer += c[o]
         answer *= v
         
         o -= 1
     return answer

def poly_add(a,b):
    g = []
    h = min(len(a),len(b))
    for i in range(h):
        g.append(a[i]+b[i])
    if(len(a)>len(b)):
        g.extend(a[h:])
    elif(len(a)<len(b)):
        g.extend(b[h:])
    return g
            
def poly_mul(a,b):
    g = [0] * (len(a)+len(b)-1)
    for i in range(len(a)):
        for j in range(len(b)):
            g[i+j] += a[i] * b[j]
    return g

def poly_roots(c):
    while len(c)>0 and c[-1]==0:
        c.pop()
    if(len(c)==2):
        return -c[0]/c[1]
    elif(len(c)==3):
        z = complex(c[0])
        y = complex(c[1])
        x = complex(c[2])
        return [(-y+(y*y-4*z*x)**0.5)/(2*x),(-y-(y*y-4*z*x)**0.5)/(2*x)]
        

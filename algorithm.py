import numpy as np

NOM = input(" input the number of member : ")
A=0          
b=1

NOM = int(NOM)

u2 = np.zeros((8,8))
        
while A < NOM : 
    
    u1 = np.zeros((8,8))
    
    while b<65:
        
        a = input(" input the addresses of the boxes that u want to fill : ")
    
        aa =list(a)
        aaa = int(aa[0]) 
        aaa2 =int(aa[2])
        u1[aaa2,aaa] = 1
        aaaa = aaa * aaa2
        
        if aaaa==0:
            
            break  

    u2 = u1 + u2
    
    A = A+1 
    
    if A == NOM:
        print(" done ")
        
u2

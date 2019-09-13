#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
<Code> : Code to implement cellular automata.   
"""

    
def initialize(l,e):
    for i in range(e//10):
        l[i]=1
    for i in range(e//10,len(l)):
        l[i]=0
    return l
            
def cellular_transition(l,e):
    l1=[]
    for i in range(10):
        l1.append(l[i])
    #print("L1 is",l1)
    left=0
    right=0
    for i in range(10):
        if(i==0):
            left = 9
            right = i+1
        elif(i==9):
            left = i-1
            right = 0
        else:
            left = i-1
            right = i+1
        """ Defining the cellular automata neighbour transitions   """#
        if (l[left]==0 and l[i]==0 and l[right]==0):
            l1[i]=l[i]
            #print("Transition 1")
        elif (l[left]==0 and l[i]==0 and l[right]==1):
            l1[i]=l[i]
            #print("Transition 2")
        elif (l[left]==0 and l[i]==1 and l[right]==0):
            l1[i]=0
            if(i!=9):
                l1[i+1]=1
            else:
                l1[0]=1
            #print("Transition 3")
        elif (l[left]==0 and l[i]==1 and l[right]==1):
            l1[i]=0
            #print("Transition 4")
        elif (l[left]==1 and l[i]==0 and l[right]==0):
            if(e==10):
                l1[i]=l[i]
            else:
                l1[i]=1
            #print("Transition 5")
        elif (l[left]==1 and l[i]==0 and l[right]==1):
            l1[i]=l[i]
            #print("Transition 6")
        elif (l[left]==1 and l[i]==1 and l[right]==0):
            l1[i]=l[i]
            #print("Transition 7")
        else:
            l1[i]=l[i]
            #print("Transition 8")
    return l1
            
            


print("Enter the number of rows in the LED")
a=int(input())
print("Enter the number of columns in the LED <Multiple of 10>")
b=int(input())
m=[[0 for i in range(b)] for j in range(a)]
#print(m)
print("Enter the optimization percentage <<multiple of 10 less than 100>>")
e=int(input())
l=[]
c=0
initj=0
set_counter=0
for master_loop in range(11):
    for i in range(a):
        for j in range(b):
            l.append(m[i][j])
            c=c+1
            if(c==10):
                if(set_counter==0):
                    l=initialize(l,e)
                    set_counter=set_counter+1
                #print("Matrix after initializing:")
                
                #print("Matrix after one cellular transition")
                new=cellular_transition(l,e)
                #print(new)
                for k in range(10):
                    m[i][initj]=new[k]
                    initj=initj+1
                #initj=initj-1
                c=0    
        initj=0
    l=[]
    for i in range(a):
        for j in range(b):
            print(m[i][j], end='')
        print()
    print("Do you want to see the next cellular automata transition? Y/N")
    user_opinion=input().lower()
    if(user_opinion=='y'):
        continue
    else:
        print("Breaking")
        break;
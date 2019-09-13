#Two dimensional cellular automata final phase
import math
m=int(input("Enter the number of rows:\n"))
n=int(input("Enter the number of columns:\n"))
e=int(input("Enter efficienccy percent:\n"))
a=[[0 for i in range(n)] for i in range(m)]
"""
Quantizing <phase 1>:
     Store in a list of tuples of format [([row beg, row end),[col beg, col end]) 
     This quantization is for the LEDs that can be grouped into three. The next phase of quantizing still remains
"""
#Define number of rows that can be quantized, and number of columns that can be quantized
rq= m//3
cq = n//3
tq = rq * cq
#Where tq is the maximum number of quantum packets

#Now quantize rows: 
#Starting positions in lr1 and ending positions in lr2
#Store the starting positions of rows in l
lr1=[]
lr2=[]
lr=[]
counter=0
for i in range(0,m,3):
    lr1.append(i)
for i in range(0,m):
    counter+=1
    if(counter==3):
        lr2.append(i)
        counter=0
for i in range(len(lr2)):
    lr.append([lr1[i],lr2[i]])
    
#Do the same for columns
lc1=[]
lc2=[]
lc=[]
for i in range(0,n,3):
    lc1.append(i)
counter=0    
for i in range(0,m):
    counter+=1
    if(counter==3):
        lc2.append(i)
        counter=0
for i in range(len(lc2)):
    lc.append([lc1[i],lc2[i]])

#define a list of tuples l that will store all the quantization positions
l=[]
for i in range(len(lr)):
    for j in range(len(lc)):
        tup=(lr[i],lc[j])
        l.append(tup)
"""
Define phase 2 of quantization:
This is for the LED Strips, the ones that cannot be fit into a circle    

"""
#Phase 2 of quantization
"""
The number of rows that did not get quantized is rq*3
The number of columns that did not get quantized is cq*3
So define the LED Strips as 
1111111110
1111111110
1111111110
1111111110
1111111110
1111111110
1111111110
1111111110
1111111110
0000000000
The whole zero things as 1.
There can be maximum of two strips. Define the second strip as the same. Store them in a list.
Then we turn the LEDs on accordingly, i.e. we see how many LEDs will be on at an instant, and then accordingly we will randomize them.
"""
#Start
nr=rq*3
nc=cq*3
#Check how many strips you will require, ns = m-nr
nsr=m-nr
nsc=n-nc
#These are the functions that will get the strips
def define_strips_rows(a,col_pos,lx):
    for i in range(len(a[0])):
        if [col_pos,i] not in lx:
            lx.append([col_pos,i]) 
    return lx
def define_strips_cols(a,row_pos,strip):
    ly=[]
    for i in range(len(a)):
        if [i,row_pos] not in strip:
            ly.append([i,row_pos]) 
    return ly[::-1]
strip1=[]
strip2=[]
#Defining quantum strips for rows
for i in range(0,nsr):
    if i==0:
        strip1=define_strips_rows(a,nr,strip1)
    elif i==1:
        strip2= define_strips_rows(a,nr+1,strip2)
#Defining quantum strips for columns
for i in range(0,nsc):
    if i==0:
        temp_strip=define_strips_cols(a,nc,strip1)
        for i in temp_strip:
            strip1.append(i)
            
    elif i == 1:
        temp_strip=define_strips_cols(a,nc+1,strip2)
        for i in temp_strip:
            strip2.append(i)
#Optimizing the strips by removing the recurring LEDs present in the strips
if((nsr==1 and nsc==2) or (nsr==2 and nsc==1) or (nsr==2 and nsc==2)):
    if nsr==1:
        strip1.remove([m-1,n-1])
    if nsc==1:
        strip1.remove([m-1,n-1])
    if nsr==2 and nsc==2:
        strip1.remove([m-2,n-1])
        strip1.remove([m-1,n-2])
        

"""
Strip Sorting

"""


#Randomize : phase 1
#Define the function that will traverse throughout each quantum packet
def randomize_2d(l,a,breakpoint):
    quantum_heads=[]
    for i in l:
        c=0
        temp=1
        for j in range(i[0][0],i[0][1]+1):
            for k in range(i[1][0],i[1][1]+1):
                c+=1
                if(c==5 and breakpoint!=5):
                    continue
                a[j][k]=temp
                if(c<=5):
                    if(c==breakpoint-1):
                        temp=0
                if(c==breakpoint):
                        temp=0
        #Make the fifth thing = 1
        c=0
        for j in range(i[0][0],i[0][1]+1):
            for k in range(i[1][0],i[1][1]+1):
                c+=1
                if(c==5):
                    quantum_heads.append([j,k])
                    a[j][k]=1
                    break
    return a,quantum_heads  
"""
Defining the number of leds that need to be on at an instant
number of LEDs n = e/100 * 9
if fractional part of n > 0.5 take ceil else take false
"""
nq=e/100 * 9
nq = math.ceil(nq) if float(str(nq-int(nq))[1:])>0.5 else math.floor(nq) #Breakpoint is defined
a,quantum_heads = randomize_2d(l,a,nq)

"""
Randomize phase 2: Randomizing the Strips
    1.Count the number of LEDs that will be on in an instant
    2.Then acquire the number of LEDs you need to remain keep the system going
    3.Divide them into the strips
"""
#Step 1: Counting the number of 1's in the LED
def count_ons(a):
    c=0
    for i in range(len(a)):
        for j in range(len(a[0])):
            if(a[i][j]==1):
                c+=1
    return c

ons=count_ons(a)
#ne= number of leds you need to have on at an instance
ne=e/100 *(m*n)
#leds_in_strip= no of leds that need to be on in a strip
leds_in_strip=ne-ons
if leds_in_strip<0:
    leds_in_strip=0
"""
Limitation of Strip.

"""

if leds_in_strip>len(strip1)+len(strip2):
    leds_in_strip=len(strip1)+len(strip2)-2
#Defining the number of strips that are present in the LED 
no_of_strips=0
if len(strip1)==0:
    no_of_strips=0
else:
    no_of_strips=1
    if len(strip2)!=0:
        no_of_strips=2
#Define randomize phase 2 function here
def randomize_1d(strip,leds_in_strip):
    c=0
    temp=1
    for i in strip:
        if c==leds_in_strip:
            temp=0
        a[i[0]][i[1]]= temp
        c=c+1
    return a


if(no_of_strips==2):
    a=randomize_1d(strip2,leds_in_strip//2)
    a=randomize_1d(strip1,leds_in_strip//2)
elif no_of_strips==1:
    a=randomize_1d(strip1,leds_in_strip)

"""
Defining the cellular transitions for 1D:

for i in range(m):
        for j in range(n):
            print(a[i][j],end=" ")
        print()
"""
def cellular_transition(a,strip):
    a1=[[0 for i in range(len(a[0]))] for j in range(len(a))]
    for i in range(len(a)):
        for j in range(len(a[0])):
            a1[i][j]=a[i][j]
    left=0
    right=0
    for i in range(len(strip)):
        left_val=0
        right_val=0
        if(i==0):
            left = len(strip)-1
            right = i+1
        elif(i==len(strip)-1):
            left = i-1
            right = 0
        else:
            left = i-1
            right = i+1
        """ Defining the cellular automata neighbour transitions"""
        left_val = a[strip[left][0]][strip[left][1]]
        right_val=a[strip[right][0]][strip[right][1]]
        curr_val=a[strip[i][0]][strip[i][1]]
        if (left_val==0 and curr_val==0 and right_val==0):
            a1[strip[i][0]][strip[i][1]]=curr_val
            #print("Transition 1")
        elif (left_val==0 and curr_val==0 and right_val==1):
            a1[strip[i][0]][strip[i][1]]=curr_val
            #print("Transition 2")
        elif (left_val==0 and curr_val==1 and right_val==0):
            a1[strip[i][0]][strip[i][1]]=0
            #if(i!=9):
            #    a[strip[i+1][0]][strip[i+1][1]]=1
            #else:
            #    a[strip[0][0]][strip[0][1]]
            #print("Transition 3")
        elif (left_val==0 and curr_val==1 and right_val==1):
            a1[strip[i][0]][strip[i][1]]=0
            #print("Transition 4")
        elif (left_val==1 and curr_val==0 and right_val==0):
            if(e==10):
                a1[strip[i][0]][strip[i][1]]=curr_val
            else:
                a1[strip[i][0]][strip[i][1]]=1
            #print("Transition 5")
        elif (left_val==1 and curr_val==0 and right_val==1):
            a1[strip[i][0]][strip[i][1]]=1
            #print("Transition 6")
        elif (left_val==1 and curr_val==1 and right_val==0):
            a1[strip[i][0]][strip[i][1]]=curr_val
            #print("Transition 7")
        else:
            a1[strip[i][0]][strip[i][1]]=curr_val
            #print("Transition 8")
    return a1
#Fix the strip positions
def cellular_transition_strip(a,strip):
    a1=[[0 for i in range(len(a[0]))] for j in range(len(a))]
    for i in range(len(a)):
        for j in range(len(a[0])):
            a1[i][j]=a[i][j]
    left=0
    right=0
    for i in range(len(strip)):
        left_val=0
        right_val=0
        if(i==0):
            left = len(strip)-1
            right = i+1
        elif(i==len(strip)-1):
            left = i-1
            right = 0
        else:
            left = i-1
            right = i+1
        """ Defining the cellular automata neighbour transitions"""
        left_val = a[strip[left][0]][strip[left][1]]
        right_val=a[strip[right][0]][strip[right][1]]
        curr_val=a[strip[i][0]][strip[i][1]]
        if (left_val==0 and curr_val==0 and right_val==0):
            a1[strip[i][0]][strip[i][1]]=curr_val
            #print("Transition 1")
        elif (left_val==0 and curr_val==0 and right_val==1):
            a1[strip[i][0]][strip[i][1]]=curr_val
            #print("Transition 2")
        elif (left_val==0 and curr_val==1 and right_val==0):
            a1[strip[i][0]][strip[i][1]]=1
            #if(i!=9):
            #    a[strip[i+1][0]][strip[i+1][1]]=1
            #else:
            #    a[strip[0][0]][strip[0][1]]
            #print("Transition 3")
        elif (left_val==0 and curr_val==1 and right_val==1):
            a1[strip[i][0]][strip[i][1]]=0
            #print("Transition 4")
        elif (left_val==1 and curr_val==0 and right_val==0):
            if(e==10):
                a1[strip[i][0]][strip[i][1]]=curr_val
            else:
                a1[strip[i][0]][strip[i][1]]=1
            #print("Transition 5")
        elif (left_val==1 and curr_val==0 and right_val==1):
            a1[strip[i][0]][strip[i][1]]=curr_val
            #print("Transition 6")
        elif (left_val==1 and curr_val==1 and right_val==0):
            a1[strip[i][0]][strip[i][1]]=curr_val
            #print("Transition 7")
        else:
            a1[strip[i][0]][strip[i][1]]=curr_val
            #print("Transition 8")
    return a1





"""
This is the final phase of the code that is 2d celular transition
Revision : l contains all the addresses of the tuple
"""

#Defining neighbours

def define_neighbours(m,i,j):
    """
    This will define the position of all the neighbours, and store them in a list in the format [[i,j],[i,j]]
    The list returned will be of format [n,ne,e,se,s,sw,w,nw]
    """
    #Defining all the elements as 0
    n=e=w=s=ne=nw=se=sw=[]
    a=len(m)
    b=len(m[0])
    if(i!=0 and j!=0 and i!=(a-1) and j!=(b-1)):
        n=[i-1,j]
        e=[i,j+1]
        w=[i,j-1]
        s=[i+1,j]
        ne=[i-1,j+1]
        nw=[i-1,j-1]
        se=[i+1,j+1]
        sw=[i+1,j-1]
    elif(i==0):
        s=[i+1,j]
        n=[a-1,j]
        if(j==0):
            se=[i+1,j+1]
            e=[i,j+1]
            ne=[a-1,j+1]
            w=[i,b-1]
            nw=[a-1,b-1]
            sw=[i+1,b-1]
        elif(j==b-1):
            e=[i,0]
            w=[i,j-1]
            nw=[a-1,j-1]
            ne=[a-1,0]
            sw=[i+1,j-1]
            se=[i+1,0]
        else:
            e=[i,j+1]
            w=[i,j-1]
            se=[i+1,j+1]
            sw=[i+1,j-1]
            ne=[a-1,j+1]
            nw=[a-1,j-1]
    elif (i==a-1):
        n=[i-1,j]
        s=[0,j]
        if(j==0):
            e=[i,j+1]
            w=[i,b-1]
            ne=[i-1,j+1]
            nw=[i-1,b-1]
            sw=[0,b-1]
            se=[0,j+1]
        elif(j==b-1):
            w=[i,j-1]
            e=[i,0]
            ne=[i-1,0]
            nw=[i-1,j-1]
            sw=[0,j-1]
            se=[0,0]
        else:
            e=[i,j+1]
            w=[i,j-1]
            nw=[i-1,j-1]
            ne=[i-1,j+1]
            sw=[0,j-1]
            se=[0,j+1]
    elif(j==0):
        n=[i-1,j]
        e=[i,j+1]
        w=[i,b-1]
        s=[i+1,j]
        ne=[i-1,j+1]
        nw=[i-1,b-1]
        se=[i+1,j+1]
        sw=[i+1,b-1]
    elif(j==b-1):
        n=[i-1,j]
        e=[i,0]
        w=[i,j-1]
        s=[i+1,j]
        ne=[i-1,0]
        nw=[i-1,j-1]
        se=[i+1,0]
        sw=[i+1,j-1]
    neighbours=[n,ne,e,se,s,sw,w,nw]
    return neighbours        
"""
cellular transition:
define the neighbours for every quantum_head
#Reacp:
The quantum heads are stored in a list quantum_heads.
For every quantum head, define the neighbours
neighbours = define_neighbours
define cellular transition for every 'neighbours'

"""
#Working code for cellular optimization
def cellular_transition_2d(a,quantum_heads,c):
    a1=[[0 for i in range(len(a[0]))] for j in range(len(a))]
    for i in range(len(a)):
        for j in range(len(a[0])):
            a1[i][j]=a[i][j]
    for i in quantum_heads:
        neighbours = define_neighbours(a,i[0],i[1])
        if(c!=4 and c!=8):
            a=cellular_transition(a,neighbours)
        elif(c==4):
            a1[i[0]][i[1]]=0
            for x in range(len(neighbours)):
                curr=x
                left=right=0
                if(x==0):
                    left=len(neighbours)-1
                    right=x+1
                elif(x==len(neighbours)-1):
                    left=x-1
                    right=0
                else:
                    left=x-1
                    right=x+1
                  
                if(a[neighbours[left][0]][neighbours[left][1]] == 0 and a[neighbours[curr][0]][neighbours[curr][1]] == 0 and a[neighbours[right][0]][neighbours[right][1]] == 1):  
                    a1[neighbours[x][0]][neighbours[x][1]]=1 
            
        elif(c==8):
            a1[i[0]][i[1]]=1
            for x in range(len(neighbours)):
                curr=x
                left=right=0
                if(x==0):
                    left=len(neighbours)-1
                    right=x+1
                elif(x==len(neighbours)-1):
                    left=x-1
                    right=0
                else:
                    left=x-1
                    right=x+1
                  
                if(a[neighbours[left][0]][neighbours[left][1]] == 0 and a[neighbours[curr][0]][neighbours[curr][1]] == 1 and a[neighbours[right][0]][neighbours[right][1]] == 1):      
                    a1[neighbours[x][0]][neighbours[x][1]]=0
            
            
            #a1[neighbours[3][0]][neighbours[3][1]]=0  
    if(c==4 or c==8):
        return a1    
    return a

"""
Final cellular transition
"""
def final_transition(a,quantum_heads,strip1,strip2,c):
    a=cellular_transition_2d(a,quantum_heads,c)
    if(no_of_strips==1):
        a=cellular_transition(a,strip1)
    if(no_of_strips==2):
        a=cellular_transition_strip(a,strip1)
        a=cellular_transition_strip(a,strip2)
        
        
    return a

c=0
for i in range(len(a)):
        for j in range(len(a[0])):
            print(a[i][j],end="")
        print()
print("Begin transition")

while True:
    if(c>8):
        c=0
    c=c+1
    a=final_transition(a,quantum_heads,strip1,strip2,c)
    for i in range(len(a)):
        for j in range(len(a[0])):
            print(a[i][j],end="")
        print()
    print("Number of LEDs on currently: ",count_ons(a))
    ch=input("Want to continue?Y/n")
    if(ch.lower()!='y'):
        break
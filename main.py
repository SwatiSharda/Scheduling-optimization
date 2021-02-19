# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 23:50:28 2019

@author: Aryan
"""
import numpy as np
import sys
import pandas as pd
import matplotlib.pyplot as plt
import csv
prices =[2.5,2.2,1.6,2.3,2.7,2.7,2.8,2.3,3.8,4.2,4.7,6.3,5.1,4.8,5.3,4.4,4.4,3.7,3.5,3.5,3.4,3.2,2.9,2.7]
#[0.047,0.044,0.042,0.042,0.043,0.045,0.053,0.065,0.081,0.080,0.070,0.060,0.053,0.052,0.054,0.059,0.067,0.093,0.091,0.083,0.060,0.054,0.053,0.050]
#[0.06,0.06,0.06,0.06,0.06,0.06,0.06,0.06,0.06,0.06,0.06,0.06,0.06,0.06,0.06,0.06,0.06,0.06,0.120,0.120,0.06,0.06,0.06,0.06]
#[0.045,0.045,0.045,0.045,0.045,0.045,0.045,0.045,0.06,0.06,0.06,0.045,0.045,0.045,0.045,0.045,0.045,0.045,0.09,0.09,0.045,0.045,0.045,0.045]
#[0.06,0.06,0.06,0.06,0.06,0.06,0.06,0.06,0.06,0.06,0.06,0.06,0.06,0.06,0.06,0.06,0.06,0.06,0.06,0.06,0.06,0.06,0.06,0.06]
'''[1.5,1.4,1.4,1.4,1.4,1.5,1.9,2.1,1.5,1.6,1.5,1.5,1.7,1.9,2.0,1.9,2.0,2.4,2.4,3.4,2.3,2.4,2.2,2.1]
[1.6,1.5,1.5,1.5,1.5,1.6,2.3,2.9,2.5,2.3,2,1.9,1.9,1.8,1.9,1.8,1.9,2.3,2.2,2.1,2,2,1.8,1.7]
[2.5,2.2,1.6,2.3,2.7,2.7,2.8,2.3,3.8,4.2,4.7,6.3,5.1,4.8,5.3,4.4,4.4,3.7,3.5,3.5,3.4,3.2,2.9,2.7]
'''
r = []
# for 30 min
'''for i in range(24):
    q = prices[i]
    for j in range(2):
        r.append(q)
prices=r '''
# for 10 min
'''for i in range(24):
    q = prices[i]
    for j in range(6):
        r.append(q)
prices = r '''      
# for 5 min
for i in range(24):
    q = prices[i]
    for j in range(12):
        r.append(q)
prices=r     
        
average_price = np.average(prices)

class device(object):
    
    def __init__(self,power,start,end,execution,name,d_type,phases=-1,state=0,priority = sys.maxsize ):
        #for per hour
        #self.power     = power
        #for 30 min
        #self.power     = power/2
        #for 10 min
        #self.power     = power/6
        #for 5 min
        self.power     = power/12
        self.start     = start*60
        self.end       = end*60
        self.execution = execution*60
        self.name      = name  
        self.priority  = priority
        self.d_type    = d_type
        self.phases    = phases
        self.state     = state
        
    def ready(self,start,end):
        if self.start <= start and self.end >= end :
            return True
        else :
            return False
    
    def run(self):
        self.execution= self.execution - 5
        #self.execution= self.execution - 10 #10 min
        #self.execution= self.execution - 30 #half hour
        #self.execution = self.execution - 60#per hour
      
def schedule(devices):
    for d in devices:
        #least laxity
        d.priority = d.end - d.execution
        
        #early deadline
        #d.priority =  d.end               
    devices = sorted(devices,key = lambda z : z.priority) 
    return devices 
      
taskfile = open('tasks.txt')
lines = taskfile.readlines()
devices = []
renewable = 150
battery = 0
battery_max = 20
power = 0
cost = 0
grap=[]
while lines:
    line = lines[0].split(' ')
    if len(line) == 7 :
        temp = []
        temp.append(device(power = float(line[0]),start=float(line[1]),end=float(line[2]) , execution=float(line[3]),name=line[4],d_type=line[5],phases=0))
        lines.pop(0)
        t=[]
        for i in range(int(line[6])):
            z=lines[0].split(' ')
            t.append(device(power=float(z[0]),start=float(z[1]),end=float(z[2]),execution=float(z[3]),name=z[4],d_type=z[5]))
            lines.pop(0)
        temp.append(t)    
        devices.append(temp)    
    else :
        devices.append(device(power = float(line[0]),start=float(line[1]),end=float(line[2]),execution=float(line[3]),name=line[4],d_type=line[5]))
        lines.pop(0)

per_hour = []
k=-1
for i in range(0,1440,5):#change step
    ready_devices = []
    k=k+1
    if prices[k] <= average_price:
        for d in devices:
            if type(d) is list :
                curr_phase = d[0].phases
                if curr_phase < len(d[1])-1 and d[1][curr_phase].execution <= 0:
                    d[0].phases = d[0].phases + 1
                    curr_phase = curr_phase + 1
                if d[1][curr_phase].execution > 0:
                    if d[1][curr_phase].state == 1:
                        ready_devices.append(d[1][curr_phase])
                        d[1][curr_phase].run()
                        power = power + d[1][curr_phase].power
                        cost = cost + d[1][curr_phase].power*prices[k]
                    else:
                        if d[1][curr_phase].ready(i,i+5):#change step
                            d[1][curr_phase].state = 1
                            ready_devices.append(d[1][curr_phase])
                            d[1][curr_phase].run()
                            power = power + d[1][curr_phase].power
                            cost = cost + d[1][curr_phase].power*prices[k]
                
            else:        
                if d.ready(i,i+5) and d.execution > 0:#change step as per requirement
                    ready_devices.append(d)
                    d.run()
                    power = power + d.power
                    cost = cost + d.power*prices[k]
                
        grap.append(1)                
    else :
        if renewable <= 0 and battery > 0:
            for d in devices:
                if type(d) is list :
                    curr_phase = d[0].phases
                    if curr_phase < len(d[1])-1 and d[1][curr_phase].execution <= 0:
                        d[0].phases = d[0].phases + 1
                        curr_phase = curr_phase + 1
                    if d[1][curr_phase].execution > 0:
                        if d[1][curr_phase].state == 1:
                            '''ty=d[1][curr_phase]
                            ty.power=(-1)*ty.power
                            ready_devices.append(ty)'''
                            ready_devices.append(d[1][curr_phase])
                            d[1][curr_phase].run()
                            if d[1][curr_phase].power <= battery:
                                battery = battery - d[1][curr_phase].power
                            else:
                                power = power + d[1][curr_phase].power
                                cost = cost + d[1][curr_phase].power*prices[k]
                            
                        else:
                            if d[1][curr_phase].ready(i,i+5) and d[1][curr_phase].power <= battery: #change step
                                d[1][curr_phase].state = 1
                                '''tyx=d[1][curr_phase]
                                tyx.power=(-1)*tyx.power
                                ready_devices.append(tyx)'''
                                ready_devices.append(d[1][curr_phase])
                                d[1][curr_phase].run()
                                battery = battery - d[1][curr_phase].power

                else:            
                    if d.ready(i,i+5) and d.execution > 0 and d.power <= battery:#change step acc to requirement
                        '''ty1=d
                        ty1.power=(-1)*ty1.power
                        ready_devices.append(ty1)'''
                        ready_devices.append(d)
                        d.run()
                        battery = battery - d.power
        else:
            x = []
            for d in devices:
                if type(d) is list :
                    curr_phase = d[0].phases
                    if curr_phase < len(d[1])-1 and d[1][curr_phase].execution <= 0:
                        d[0].phases = d[0].phases + 1
                        curr_phase = curr_phase + 1
                    if d[1][curr_phase].execution > 0:
                        if d[1][curr_phase].state == 1:
                            '''tyy=d[1][curr_phase]
                            tyy.power=(-1)*tyy.power
                            ready_devices.append(tyy)'''
                            ready_devices.append(d[1][curr_phase])
                            d[1][curr_phase].run()
                            if d[1][curr_phase].power <= renewable:
                                renewable = renewable - d[1][curr_phase].power
                            else:    
                                power = power + d[1][curr_phase].power
                                cost = cost + d[1][curr_phase].power*prices[k]
                        else:
                            if d[1][curr_phase].ready(i,i+5) and d[1][curr_phase].power <= renewable:#change step
                                x.append(d[1][curr_phase])
                            
                                
                else:                
                    if d.ready(i,i+5) and d.power < renewable and d.execution > 0:#change step
                        x.append(d)
                    
            x = schedule(x)
            
            for d in x:
                if d.power <= renewable :
                    d.state=1
                    '''ki=d
                    ki.power=(-1)*ki.power
                    ready_devices.append(ki)'''
                    ready_devices.append(d)
                    d.run()
                    renewable = renewable - d.power
                    
            if renewable > 0 and battery <= battery_max :
                if battery + renewable <= battery_max:
                    battery = battery + renewable
        
        grap.append(0)  
          
    per_hour.append(ready_devices)  
                  

k=-1
for i in range(0,1440,5):#change step
    k=k+1
    for d in devices:
        if type(d) is list :
            curr_phase = d[0].phases
            if curr_phase < len(d[1])-1 and d[1][curr_phase].execution <= 0:
                d[0].phases = d[0].phases + 1
                curr_phase = curr_phase + 1
            if d[1][curr_phase].execution > 0:
                if d[1][curr_phase].state == 1 :
                    if d[1][curr_phase] not in per_hour[k]:
                        per_hour[k].append(d[1][curr_phase])
                        d[1][curr_phase].run()
                        power = power + d[1][curr_phase].power
                        cost = cost + d[1][curr_phase].power*prices[k]
                else:
                    if d[1][curr_phase].ready(i,i+5):#change step
                        if d[1][curr_phase] not in per_hour[k]:
                            d[1][curr_phase].state = 1
                            per_hour[k].append(d[1][curr_phase])
                            d[1][curr_phase].run()
                            power = power + d[1][curr_phase].power
                            cost = cost + d[1][curr_phase].power*prices[k]
        else:                
            if d.ready(i,i+5) and d.execution > 0 :#change step
                if d not in per_hour[k]:
                    per_hour[k].append(d)
                    d.run()
                    power = power + d.power
                    cost = cost + d.power*prices[k]
                
data1=[]
for d in devices:
    
    if type(d) is list:
        pl=[]
        for curr in range(len(d[1])):
            a=[]
            for i in range(24*12):#change step
                if d[1][curr] in per_hour[i]:
                    a.append(d[1][curr].power)
                else:
                    a.append(0)
            pl.append(a)  
        pl = [sum(x) for x in zip(*pl)]
        pl.insert(0,d[0].name)
        data1.append(pl)
    else:
        a=[]
        a.append(d.name)
        for i in range(24*12): #change step
            if d in per_hour[i]:
                a.append(d.power)
            else:
                a.append(0)
        data1.append(a)
col = []
col.append("Device")
for i in range(0,1440,5):#change step
    col.append(str(i)+'-'+str(i+5)) #change step 


df = pd.DataFrame(columns = col,data = data1)      
df.set_index('Device').T.plot(xticks=60,figsize=(20,20),kind='bar',stacked=True)                  

'''xax =[]
for i in range(0,1440,5):#change step
    xax.append(str(i)+'-'+str(i+5))#change step
plt.xlabel('Interval')
plt.ylabel('energy_type')   
plt.figtext(0.9,0.8,'1:Grid')
plt.figtext(0.9,0.75,'0: Renewable')
plt.figure(figsize=[20,20])
plt.plot(xax,grap) 
 '''
ab = pd.read_csv('106953_36.33_-110.74_1998.csv')  #column 8 
status=[]
for d in data1:
    p=[]
    p.append(d[0])
    time=[]
    t= False
    for x in range(len(d)-1):
        x=x+1
        if x==12*24 and t==True:#change step
            t=False
            time.append(str(int((x*5)/60)) + ':'+str((x*5)%60))#change step
        elif d[x]==0 and t==True:
            t=False
            time.append(str(int(((x-1)*5)/60)) + ':'+str(((x-1)*5)%60))#change step
        elif d[x]>0 and t==False:
            t=True
            time.append(str(int(((x-1)*5)/60))+':'+str(((x-1)*5)%60))#change step
    p.append(time)
    status.append(p)        
row_list=[]
for s in status:
    for i in range(len(s[1])):
        tem=[]
        tem.append(s[0])
        tem.append(s[1][i])
        if i%2==0:
            tem.append(1)
        else:
            tem.append(0)
        row_list.append(tem)

with open('devices.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=' ')
    writer.writerows(row_list)            
    
           
            
            
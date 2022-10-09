import time 
start = time.time()
print(start)

import numpy as np
import math as mt
import pandas as pd

t_s = 1 #time step size in seconds
sigma = 5.6703 * (10**(-8)) #J/m2sK4 #Stefan–Boltzmann constant
S_irr = 1344 #solar irradiance in W/m^2
R_e = 6371*1000 # Earth radius in m
A_Surface = 4 * mt.pi * (R_e**2) #Earth surface area in m^2
q_surface = 237 # infrared reflected by Earth on surface W/m^2
Alt_Orbit = 500*1000 #orbit altitude in m
A_orbit = 4 * mt.pi * ((R_e+Alt_Orbit)**2) #surface of sphere of with orbit altitude as radius in m^2
q_orbit = q_surface * (A_Surface /A_orbit) #infrared reflected by Earth on at orbit surface in W/m^2
###total time###
total_time = 5 #total simulation time in seconds
######
T_space = 3 # Space temperature in K
T_Earth = 303 #Earth temperature in K

#importing input data
operating_folder = 'E:\Thm_mod' #location of the working directory
F_i_j = pd.read_csv(operating_folder + '\F_i_j.csv') #view factors for radiation
A_rad = pd.read_csv(operating_folder + '\A_rad.csv') #area of interacting surfaces
emmv = pd.read_csv(operating_folder + '\e.csv') #emmisivity
F_Sun = pd.read_csv(operating_folder + '\F_sun.csv') #access to sun for the interface nodes
absv = pd.read_csv(operating_folder + '\\absorption.csv') #absorptivity
Ele = pd.read_csv(operating_folder + '\ele.csv') #elevation at every second
F_Earth = pd.read_csv(operating_folder + '\F_Earth.csv') #access to Earth for the interface nodes
Conductivity = pd.read_csv(operating_folder + '\k_i_j.csv') #Conductivity of conduction interfaces
Area_Cond = pd.read_csv(operating_folder + '\A_cond.csv') #cross-sectional area of Conduction area
Length_Cond = pd.read_csv(operating_folder + '\L_cond.csv') #length of conduction interfaces
cont_res = pd.read_csv(operating_folder + '\Cont_Res.csv') #contact resistance
F_space = pd.read_csv(operating_folder + '\F_space.csv') #access to deep space for the interface nodes
node_comb = pd.read_csv(operating_folder + '\Combining_nodes.csv') #node combinations for stored energy
mass = pd.read_csv(operating_folder + '\mass.csv') #mass in kg
Sp_Heat = pd.read_csv(operating_folder + '\Cp.csv') #specific heat in J/kgK
Ti = pd.read_csv(operating_folder + '\Ti.csv') #initial temperatures
Q_GEN = pd.read_csv(operating_folder + '\heat_generated.csv') #heat genearated at each timestep in heat storing nodes
print('csv files read') #reading input CSV files

act_node = node_comb.Heat_Storage_Node.nunique() #calculating number of heat storing nodes
print (('heat storage nodes = ') + (str(act_node))) #number of heat storing nodes

###Initialization###
J = (len(F_i_j)) #nos of rows 
I = (len(F_i_j.columns)) #nos of columns
Rr_i_j = pd.DataFrame(index=range(J),columns=range(I)) #creating dataframe for storing multiplying factor for radiation

i = 0
while i < (len(F_i_j.columns)):
    e_1 = float(emmv.iat[0,i]) #emmisivity of 1
    A_1 = float(A_rad.iat[0,i]) #area of 1
    j = 0 
    while j < (len(F_i_j)):
        e_2 = float(emmv.iat[0,j]) #emmisivity of 2
        A_2 = float(A_rad.iat[0,j]) #area of 2
        F_1_2 = F_i_j.iat[j,i] #view factor for 1 to 2
        
        if F_1_2 == 0:
            Rr_1_2 = 0
        else:
            Rr_1_2 = sigma/(((1-e_1)/(e_1*A_1))+(1/(A_1*F_1_2))+((1-e_2)/(e_2*A_2))) #W/(K^4) #calculating multiplying factor for radiation for 1 to 2 W/K^4
        
        Rr_i_j.iloc[j,i] = Rr_1_2 #storing the calculated multiplying factor for radiation for i to j W/K^4

        j = j+1
    i = i+1

Rr_i_j.to_csv('Rr_i_j.csv') #writing csv file for multiplying factors for radiation for i to j W/K^4
print('initialization complete')

#total time x INF count
Q_net = pd.DataFrame(index=range(total_time),columns=range(I)) #creating dataframe to store total power in each interface node
T = pd.DataFrame(index=range(total_time),columns=range(I)) #creating dataframe to store temperature of each interface node
Q_Sun = pd.DataFrame(index=range(total_time),columns=range(I)) #creating dataframe to store heat recived from sun at each timestep in W
Q_Space = pd.DataFrame(index=range(total_time),columns=range(I)) #creating dataframe to store heat rejected to deep space at each timestep in W

# 1 x HSN count
T_i_store = pd.DataFrame(np.zeros((1, act_node))) #creating dataframe to store initial temperature for each heat storage node

#total time x HSN count
Q_store = pd.DataFrame(np.zeros((total_time, act_node))) #creating dataframe to store energy stored in each heat storage node
T_store = pd.DataFrame(np.zeros((total_time, act_node))) #creating dataframe to store temperature for each heat storage node

#INF count x INF Count
Q_i_j = pd.DataFrame(index=range(J),columns=range(I)) #creating dataframe to store heat transfer between of each interface node i to J
Q_rad_i_j = pd.DataFrame(index=range(J),columns=range(I)) #creating dataframe to store radiation heat transfer between of each interface node i to J
Q_cond_i_j = pd.DataFrame(index=range(J),columns=range(I)) #creating dataframe to store conduction heat transfer between of each interface node i to J
Q_cont_i_j = pd.DataFrame(index=range(J),columns=range(I)) #creating dataframe to store contact heat transfer between of each interface node i to J


print('dataframes created')

####Heat excahange calculations###
timestep = 0
while timestep < total_time:
    
    i = 0 #interface node number
    while i < (len(Rr_i_j.columns)):
        #radiation heat transfer due to interaction
        ###Going through rows keeping column same###
        j = 0 #row number
        """q_net_row = 0 #total heat transfer along the rows with radiation
        q_cond_net_row = 0 #total heat transfer along the rows with conduction
        q_cont_net_row = 0 #total heat transfer along the rows with contact"""
        while j < ((len(Rr_i_j))): #-1):
            r = Rr_i_j.iat[j,i] #taking value of multiplying factor for radiation along row while keeping the column index = node number (column = i, row = j)
            cond = Conductivity.iat[j,i] #taking value of conductivity along row while keeping the column index = node number (column = i, row = j)
            L = Length_Cond.iat[j,i] #taking value of conduction interface length along row while keeping the column index = node number (column = i, row = j)
            A_cond = Area_Cond.iat[j,i] #taking value of cross-section of conduction interface along row while keeping the column index = node number (column = i, row = j)
            res_cont = cont_res.iat[j,i] #taking value of contact resistance along row while keeping the column index = node number (column = i, row = j)
            if timestep == 0: #condition chose temperature of last timestep or initial temperature
                T_1 = float(Ti.iat[0,i]) #initial temperature of i as 1
                T_2 = float(Ti.iat[0,j]) #initial temperature of j as 2

            else:
                T_1 = float(T.iat[(timestep-1),i]) #temperature of i in previous time step for 1
                T_2 = float(T.iat[(timestep-1),j]) #temperature of j in previous time step for 2
                
            ###conduction###
            if cond == 0: #condition to avoide 'divided by zero error'
                q_cond = 0
            else:
                q_cond = ((cond * A_cond) / L) * (T_1 - T_2) #calculating heat transfer between i and j by conduction
            Q_cond_i_j.iloc[j,i] = q_cond #storing value of heat conduction from i to j
            
            ###contact###
            if res_cont == 0: #condition to avoide 'divided by zero error'
                q_cont = 0
            else:
                q_cont = (T_1-T_2)/res_cont #calculating heat transfer between i and j by contact
            Q_cont_i_j.iloc[j,i] = q_cont #storing value of heat flow through contact from i to j
            
            ###Radiation###
            q = r * (((T_1)**4)-((T_2)**4)) #calculating heat transfer between i and j by radtiation
            Q_rad_i_j.iloc[j,i] = q #storing value of heat flow through contact from i to j
            
            #print(('i = ')+(str(i)) + (' j = ') + (str(j)))
            #print(Q_rad_i_j)
            j = j+1
        i = i+1
    
    i = 0
    while i < (len(Rr_i_j.columns)):
        ###Going through columns, keeping row same###
        k_col = 0 #column number     
        q_net_col = 0 #total heat transfer along the column with radiation
        q_cond_net_col = 0 #total heat transfer along the columns with conduction
        q_cont_net_col = 0 #total heat transfer along the columns with contact
        while k_col < (len(Rr_i_j)): #-1):
            
            #Conduction summations
            q_cond = Q_cond_i_j.iat[i,k_col] #retrieving value along columns for conduction
            q_cond_net_col = q_cond_net_col + q_cond #heat transfer from node i to other nodes along the column by conduction
            
            ###contact###
            q_cont = Q_cont_i_j.iat[i,k_col] #retrieving value along columns for contact
            q_cont_net_col = q_cont_net_col + q_cont #heat transfer from node i to other nodes along the column by contact
            
            ###Radiation###
            q = Q_rad_i_j.iat[i,k_col] #retrieving value along columns for contact
            q_net_col = q_net_col + q #heat transfer from node i to other nodes along the column by radiation
        
            #print(('i = ')+(str(i)) + (' k = ') + (str(k)))
            k_col = k_col+1
        
        #Going through rows
        k_row = 0
        q_net_row = 0 #total heat transfer along the column with radiation
        q_cond_net_row = 0 #total heat transfer along the columns with conduction
        q_cont_net_row = 0 #total heat transfer along the columns with contact
        while k_row < (len(Rr_i_j)): #-1):
            #Conduction summations
            q_cond = Q_cond_i_j.iat[k_row,i] #retrieving value along rows for conduction
            q_cond_net_row = q_cond_net_row - q_cond #heat transfer from node i to other nodes along the row by conduction
            
            ###contact###
            q_cont = Q_cont_i_j.iat[k_row,i] #retrieving value along row for contact
            q_cont_net_row = q_cont_net_row - q_cont #heat transfer from node i to other nodes along the row by contact
            
            ###Radiation###
            q = Q_rad_i_j.iat[k_row,i] #retrieving value along row for contact
            q_net_row = q_net_row + q #heat transfer from node i to other nodes along the row by radiation
        
            #print(('i = ')+(str(i)) + (' k = ') + (str(k)))
            k_row = k_row+1
            
        
        
        #heat received from sun
        a = float(absv.iat[0,i]) #absorvity of the interface node
        Tht = float(Ele.iat[timestep,0])  #theta = sun elevation value at that timestep
        f_sun = float(F_Sun.iat[0,i])  #access to sun by the interface node i
        e = float(emmv.iat[0,i]) #emmisivity of the interface node i
        Area = float(A_rad.iat[0,i]) #area of the interface node i when interacting with sun
        f_earth = float(F_Earth.iat[0,i]) #access to Earth by the interface node i
        f_space = float(F_space.iat[0,i]) #access to space by interface node i
        node_store = node_comb.iat[i, 1] #corresponding storage node index for i th interface node
        
        if timestep == 0: #condition to chose temperature of last timestep or initial temperature
            T_node = float(Ti.iat[0,i]) #initial temperature of the node
            T_i_store.iloc[0,node_store] = T_node #storing initial temperature of heat storage node in K
        else:
            T_node = float(T.iat[(timestep-1),i]) #temperature of the node at the previous timestep

        
        q_sun = f_sun * a * S_irr * Area * (mt.sin(mt.radians(abs(Tht)))) # solar irradiance on interface node i in W = J/s        
        q_space = -1 * f_space * sigma * e * Area * ((T_node**4)-(T_space**4)) #heat loss to deep space by interface node i in W = J/s
        q_earth = -1 * f_earth * e * sigma * Area * ((T_node**4)-(T_Earth**4)) #energy radiated to Earth by interface node i in W = J/s
        q_ir = f_earth * e * Area * q_orbit #earth emmited IR received by interface node i in W = J/s
        q_net = q_cont_net_row + q_cont_net_col + q_cond_net_row + q_cond_net_col + q_net_col + q_net_row + q_sun + q_space + q_earth + q_ir #net heat transfer in the interface node in W = J/s
        
        
        #storing value of total heat stored in corresponding heat storage node
        Q_Sun.iloc[timestep,i] = q_sun #storing value of heat received from i th interface node at timestep t
        Q_Space.iloc[timestep,i] = q_space #storing value of heat rejected to space from i th interface node at timestep t
        Q_net.iloc[timestep,i] = q_net #storing value of total heat exchange for i th interface node
        Q_store.iloc[timestep,node_store] = Q_store.iloc[timestep,node_store] + (q_net * t_s) #total heat energy exchanged in the from the storage node in the timestep in J
        
        #print(('i = ')+(str(i)))
        i = i+1
    
    ###calculating and storing heat storage node temperature values###
    node = 0 #heat storage node index
    while node < (act_node):
        Q_store.iloc[timestep, node] = Q_store.iloc[timestep, node] + ((Q_GEN.iat[timestep,node])*t_s) #adding generated heat in the heat storage node
        q_store_temp = Q_store.iat[timestep, node] #total heat stored by the heat storage node at that timestep
        m = mass.iat[0,node] #mass of the the heat storage node
        Cp = Sp_Heat.iat[0,node] #specific heat capacity of the heat storage node
        if timestep == 0:
            Temp = T_i_store.iat[0,node] + (q_store_temp/(m*Cp)) #temperature of the heat storage node at first timestep
        else:
            Temp = T_store.iat[(timestep-1),node] + (q_store_temp/(m*Cp)) #temperature of the heat storage node at that timestep
        
        T_store.iloc[timestep,node] = Temp #storing value of the heat storage node in the dataframe
        node = node+1
    
    ###assigning calculated values of temperature to virtual nodes###
    o = 0 #interface node index
    while o < I:
        temp_node = node_comb.iat[o, 1] #heat storage node corresponding to the interface node at index o
        T.iloc[timestep,o] = T_store.iat[timestep,temp_node] #storing temperature interface node at that timestep
        o = o+1
        
    #print(('timestep = ')+(str(timestep)))
    timestep = timestep + 1

#Saving results to csv files
Q_Sun.to_csv('Q_Sun.csv')
Q_Space.to_csv('Q_Space.csv')
Q_i_j.to_csv('Q_i_j.csv')
Q_net.to_csv('Q_net.csv')
Q_store.to_csv('Q_store.csv')
T_store.to_csv('T_store.csv')
T.to_csv('T_interface.csv')
#print('run complete')

end = time.time() - start
print("time required: ", end)

"""import webbrowser
webbrowser.open('https://music.youtube.com/watch?v=PLEQRIisP_Q&list=RDAMVMPLEQRIisP_Q')"""
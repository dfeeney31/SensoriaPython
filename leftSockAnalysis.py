# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 10:24:35 2020

@author: Daniel.Feeney
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.signal import find_peaks


# Define dynamic calibration function 
def convLeftVals(data, calData):
    #ConvRightVals Convert the Sensoria values to the correct scale using a manual
    #zero calibration. A,B,C,D all come from Sensoria calibration report.
    #Manual calibration requires the subject wear the sock but put their foot
    #in the air to create a new 0.
    #This is based on the zeroing function: 
    #Weight = A (X - (Xo - D))^(-B) + C where A,B,C, and D come from the
    #Sensoria-provided calibration reports and Xo is the average of the sensor
    #recordings during the zero calibration recording. The weight is multiplied
    #by the scaling factor listed below as calFactor to convert to PSI.
    
    
    # Hard code the baseline sensor data from Sensoria. 
    calFactor = (2.20462262/1000)/0.196349148;            #Provided by Sensoria 
    
    A0cal =  16086807437; B0cal = 2.148099; C0cal = -15033.534170; D0cal = 641;
    A1cal = 2295412989; B1cal = 1.886191; C1cal = -10256.829160; D1cal = 686;
    A2cal = 1180664527; B2cal = 1.656981; C2cal = -21312.794500; D2cal = 729;
    A3cal = 8418427991; B3cal = 1.987871; C3cal = -16522.481680; D3cal = 743;
    A4cal = 1542239230; B4cal = 1.723956; C4cal = -18247.250280; D4cal = 721;
    A5cal = 6270000000000; B5cal = 3.134906; C5cal = -8430.332047; D5cal = 676;
    A6cal =  39440040352; B6cal = 2.307837; C6cal = -13813.348140; D6cal = 627; 
    A7cal = 1512411475; B7cal = 1.565646; C7cal = -39854.332850; D7cal = 841;
    
    
    convValuesCS0 = ((data.loc[:,"S0"] - (calData.loc[:,"S0"].mean() - D0cal)).pow(-B0cal).multiply(A0cal) + C0cal).multiply(calFactor)
    convValuesCS1 = ((data.loc[:,"S1"] - (calData.loc[:,"S1"].mean() - D1cal)).pow(-B1cal).multiply(A1cal) + C1cal).multiply(calFactor)
    convValuesCS2 = ((data.loc[:,"S2"] - (calData.loc[:,"S2"].mean() - D2cal)).pow(-B2cal).multiply(A2cal) + C2cal).multiply(calFactor)
    convValuesCS3 = ((data.loc[:,"S3"] - (calData.loc[:,"S3"].mean() - D3cal)).pow(-B3cal).multiply(A3cal) + C3cal).multiply(calFactor)
    convValuesCS4 = ((data.loc[:,"S4"] - (calData.loc[:,"S4"].mean() - D4cal)).pow(-B4cal).multiply(A4cal) + C4cal).multiply(calFactor)
    convValuesCS5 = ((data.loc[:,"S5"] - (calData.loc[:,"S5"].mean() - D5cal)).pow(-B5cal).multiply(A5cal) + C5cal).multiply(calFactor)
    convValuesCS6 = ((data.loc[:,"S6"] - (calData.loc[:,"S6"].mean() - D6cal)).pow(-B6cal).multiply(A6cal) + C6cal).multiply(calFactor)
    convValuesCS7 = ((data.loc[:,"S7"] - (calData.loc[:,"S7"].mean() - D7cal)).pow(-B7cal).multiply(A7cal) + C7cal).multiply(calFactor)
    
    convValues = pd.DataFrame({'C0':list(convValuesCS0), 'C1': list(convValuesCS1), 'C2': list(convValuesCS2),'C3': list(convValuesCS3), 
                               'C4': list(convValuesCS4),'C5': list(convValuesCS5), 'C6':list(convValuesCS6), 'C7':list(convValuesCS7)})
    return convValues

# Read in files
fPath = 'C:/Users/Daniel.Feeney/Dropbox (Boa)/EndurancePerformance/SalomonQuicklace_Aug2020/Joe_Pressure_Data/Sensoria/'
fPath = 'C:/Users/Daniel.Feeney/Dropbox (Boa)/EndurancePerformance/SalomonQuicklace_Aug2020/Sean_Pressure_Data/'
entries = os.listdir(fPath)

# Import data. Hard coded for now
calFile = entries[0]
cal = pd.read_csv(fPath+calFile,sep=',', skiprows = 19, header = 0)

BOAfile = entries[3]
boa = pd.read_csv(fPath+BOAfile,sep=',', skiprows = 19, header = 0)

qlFile = entries[4]
qlFile = pd.read_csv(fPath+qlFile,sep=',', skiprows = 19, header = 0)

#convBoa = boa
#convQL = qlFile

# Use dynamic calibration from above
convQL = convLeftVals(qlFile, cal)
convBoa = convLeftVals(boa, cal)

# Generic function to calculate peaks
def avgPeaks(inputCol, ht, dist):
    x = np.array(inputCol)
    peaks, _ = find_peaks(x.flatten(), height=ht, distance = dist)
    return x[peaks].mean()

# find peaks for navicular, cuboid, and heel
#buckleNav = avgPeaks(convBuckles[['C3']], 45, 30)
#boaNav = avgPeaks(convBoa[['C3']], 45, 30)

#buckleCub = avgPeaks(convBuckles[['C7']], 25, 30)
#boaCub = avgPeaks(convBoa[['C7']], 45, 30)

#buckleHeel = avgPeaks(convBuckles[['C5']], 290, 30)
#boaHeel = avgPeaks(convBoa[['C5']], 290, 30)
        
#[boaNav, boaCub, boaHeel]
#[buckleNav, buckleCub, buckleHeel]
## Optional plotting below to find cutoffs    
#plt.plot(convBuckles[['C3']])
#plt.plot(peaks, x[peaks], "x")
#plt.plot(np.zeros_like(x), "--", color="gray")
#plt.show()


#order of sensors 0: 'Tibia', 1: '5th Met', 2: 'M Malleolus', 3:'Navicular', 4:'1st Met', 5:'Calcneus', 6:'L. Malleolus', 7:'Cuboid'
# Make plots
f, (ax0, ax1, ax2) = plt.subplots(1,3)
ax0.plot('C0', data = convQL)
ax0.plot('C0', data = convBoa)
ax0.title.set_text('L 5th Ray')

ax1.plot('C2', data = convQL)
ax1.plot('C2', data = convBoa)
ax1.title.set_text('5th distal phalanx')

ax2.plot('C6', data = convQL)
ax2.plot('C6', data = convBoa)
ax2.title.set_text('1st distal phalanx')
plt.tight_layout()

f, (ax0, ax1, ax2) = plt.subplots(1,3)
ax0.plot('C3', data = convQL)
ax0.plot('C3', data = convBoa)
ax0.title.set_text('1st MTP')

ax1.plot('C7', data = convQL)
ax1.plot('C7', data = convBoa)
ax1.title.set_text('Cuboid')

ax2.plot('C5', data = convQL)
ax2.plot('C5', data = convBoa)
ax2.title.set_text('Heel')
plt.tight_layout()
plt.legend(['Quick Lace','BOA'])

f, (ax0, ax1) = plt.subplots(1,2)
ax0.plot('C1', data = convQL)
ax0.plot('C1', data = convBoa)
ax0.title.set_text('5th MTP')

ax1.plot('C4', data = convQL)
ax1.plot('C4', data = convBoa)
ax1.title.set_text('Navicular')
plt.tight_layout()
plt.legend(['Quick Lace','BOA'])

# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 11:55:01 2020

@author: Daniel.Feeney
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 08:59:43 2020

@author: Daniel.Feeney
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.misc import electrocardiogram
from scipy.signal import find_peaks


# Define dynamic calibration function 
def convRightVals(data, calData):
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
    
    A0cal = 43333480; B0cal = 1.006716; C0cal = -47705.61; D0cal = 867.9985;
    A1cal = 197658400; B1cal = 1.42; C1cal = -14959.610000; D1cal = 785.0005197;
    A2cal = 5014654000; B2cal = 1.95; C2cal = -11368.490000; D2cal = 781.0011045;
    A3cal = 1159582000; B3cal = 1.66; C3cal = -19559.650000; D3cal = 756.00000728;
    A4cal = 965842000; B4cal = 1.851143; C4cal = -4763.286; D4cal = 735.9987463;
    A5cal = 173966200000; B5cal = 2.77; C5cal = -5534.230000; D5cal = 506.9997497;
    A6cal = 28091580000000; B6cal = 3.68; C6cal = -2596.470000; D6cal = 533.9996174; 
    A7cal = 485425400; B7cal = 1.59; C7cal = -15726.110000; D7cal = 677.0007279;
    
    
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
fPath = 'C:/Users/Daniel.Feeney/Dropbox (Boa)/Snow Protocol/SnowboardPressures/'
entries = os.listdir(fPath)

# Import data. Hard coded for now
BOAfile = entries[1]
boa = pd.read_csv(fPath+BOAfile,sep=',', skiprows = 19, header = 0)

calFname = entries[0]
cal = pd.read_csv(fPath+calFname,sep=',', skiprows = 19, header = 0)

laceFname = entries[2]
lace = pd.read_csv(fPath+laceFname,sep=',', skiprows = 19, header = 0)

qlFname = entries[3]
ql = pd.read_csv(fPath+qlFname,sep=',', skiprows = 19, header = 0)

# Use dynamic calibration from above
convLace = convRightVals(lace, cal)
convBoa = convRightVals(boa, cal)
convQL = convRightVals(ql, cal)

# Generic function to calculate peaks
def avgPeaks(inputCol, ht, dist):
    x = np.array(inputCol)
    peaks, _ = find_peaks(x.flatten(), height=ht, distance = dist)
    return x[peaks].mean()

# find peaks for navicular, cuboid, and heel
buckleNav = avgPeaks(convBuckles[['C3']], 45, 30)
boaNav = avgPeaks(convBoa[['C3']], 45, 30)

buckleCub = avgPeaks(convBuckles[['C7']], 25, 30)
boaCub = avgPeaks(convBoa[['C7']], 45, 30)

buckleHeel = avgPeaks(convBuckles[['C5']], 290, 30)
boaHeel = avgPeaks(convBoa[['C5']], 290, 30)
        
[boaNav, boaCub, boaHeel]
[buckleNav, buckleCub, buckleHeel]
## Optional plotting below to find cutoffs    
#plt.plot(convBuckles[['C3']])
#plt.plot(peaks, x[peaks], "x")
#plt.plot(np.zeros_like(x), "--", color="gray")
#plt.show()


#order of sensors 0: 'Tibia', 1: '5th Met', 2: 'M Malleolus', 3:'Navicular', 4:'1st Met', 5:'Calcneus', 6:'L. Malleolus', 7:'Cuboid'
# Make plots
f, (ax0, ax1, ax2) = plt.subplots(1,3)
ax0.plot('C0', data = convLace)
ax0.plot('C0', data = convBoa)
ax0.plot('C0', data = convQL)
ax0.title.set_text('Tibia')

ax1.plot('C2', data = convLace)
ax1.plot('C2', data = convBoa)
ax1.plot('C2', data = convQL)
ax1.title.set_text('Medial Malleolus')

ax2.plot('C6', data = convLace)
ax2.plot('C6', data = convBoa)
ax2.plot('C6', data = convQL)
ax2.title.set_text('Lateral Malleolus')
plt.tight_layout()

f, (ax0, ax1, ax2) = plt.subplots(1,3)
ax0.plot('C3', data = convLace)
ax0.plot('C3', data = convBoa)
ax0.plot('C3', data = convQL)
ax0.title.set_text('Navicular')

ax1.plot('C7', data = convLace)
ax1.plot('C7', data = convBoa)
ax1.plot('C7', data = convQL)
ax1.title.set_text('Cuboid')

ax2.plot('C5', data = convLace)
ax2.plot('C5', data = convBoa)
ax2.plot('C5', data = convQL)
ax2.title.set_text('Heel')
ax2.set_ylim([0,1000])
plt.tight_layout()
plt.legend(['Lace','BOA', 'SpeedLace'])

f, (ax0, ax1) = plt.subplots(1,2)
ax0.plot('C1', data = convLace)
ax0.plot('C1', data = convBoa)
ax0.plot('C1', data = convQL)
ax0.title.set_text('5th Met')

ax1.plot('C4', data = convLace)
ax1.plot('C4', data = convBoa)
ax1.plot('C4', data = convQL)
ax1.title.set_text('1st Met')
plt.tight_layout()
plt.legend(['Lace','BOA', 'SpeedLace'])

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 17:39:06 2021

@author: Alejandro UC
"""

## Library

import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point

# Insert your NetCDF file here. You can also use a control file to make anomaly maps
data = xr.open_dataset('tmp.nc')
#datacontrol = xr.open_dataset('control.nc')

# Change 'ts' to the variable of your choice.
variable_name = data.ts

#-----------------------------------------------------------------------------
# This will check the shape of your file. Now, it accepts file with multiple time steps.
# Make sure that your data is 3d (lat, lon, time) or 2d (lat, lon).
if len(data.coords)==3 and data.time:
    # If your data has more that one time step change '0' for the time you want to plot.
    var = variable_name.isel(time=0)
elif len(data.coords)==2 and data.lon is not None and data.lat is not None:
    var = variable_name
else:
    raise TypeError('the data is not 3d nor 2d, it has shape '+str(var.shape))   

#-----------------------------------------------------------------------------
# If you want to make an anomaly map, uncomment the following. Otherwise ignore.
# varcontrol_name = datacontrol.temp2
# if len(datacontrol.coords)==3 and datacontrol.time:
#     varcontr = varcontrol_name.isel(time=0)
# elif len(datacontrol.coords)==2 and datacontrol.lon is not None and datacontrol.lat is not None:
#     varcontr = varcontrol_name
# else:
#     raise TypeError('the data is not 3d nor 2d, it has shape '+str(varcontr.shape))  
    
#-----------------------------------------------------------------------------
# Here, multiply, subtract, or add numbers to your values to change it on the map.
var.values = var.values

# To make an anomaly map with a control experiment, use the following instead.
#var.values = var.values - varcontr.values

#-----------------------------------------------------------------------------
# Remove the white line. Do not modify!
lon = data.coords['lon']
lon_idx = var.dims.index('lon')
wrap_data, wrap_lon = add_cyclic_point(var.values, coord=lon, axis=lon_idx)

#-----------------------------------------------------------------------------
# Plot. You can change the central longitude of the map and the projection!
fig = plt.figure(figsize=(8,3))
ax = fig.add_subplot(111, projection=ccrs.Robinson(central_longitude=180), aspect='auto')

# Use the cmap color of your preference. Check online!
cmap='Spectral_r'

# The following will create the map and its color scale. You can play around the transform, the number of levels
# and also force minimum and maximum value with vmin and vmax.
pc = ax.contourf(wrap_lon, var.lat, wrap_data,transform=ccrs.PlateCarree(),levels=100,cmap=cmap,vmin=-20,vmax=20)

# You change manually the label of the colorbar if you are not satisfied with the long name.
cb = plt.colorbar(pc, ax=ax, orientation='vertical', label=str(var.long_name)+' ['+str(var.units)+']')

# Similarly to the colorbar, you can change the name of the map and the name of the file.
ax.coastlines()
ax.set_title(str(var.long_name))
#plt.savefig('My_pretty_map_'+var.name+'.pdf', bbox_inches='tight')
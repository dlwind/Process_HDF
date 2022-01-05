


This is a sample Python code illustrating how to combine daily air pollution data in NASA HDF4 format.
It uses Daily NASA Aerosal Optical Depth generated by satellite images at 1 km resolution (obtained from https://lpdaac.usgs.gov/products/mcd19a2v006/)
and computes the average Aerosal Optical Depth for each grid. It only process valid Aerosal measure without cloud coverage (see MCD19_User_Guide_V6 for details).


'test combine smokedata.py' gets the average of daily air pollution from Sep 18 to Sep 21 in 2011. 
The average for each grid is saved in 'test_combined.hdf' under the first band of layer 'Optical_Depth_047'.





Environment: python 3.6; numpy 1.21.4; pyhdf 0.10.3

HDF References:
https://moonbooks.org/Articles/How-to-read-a-MODIS-HDF-file-using-python-/
https://hdfeos.org/software/pyhdf.php

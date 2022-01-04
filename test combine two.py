from pyhdf.SD import SD, SDC
import numpy
import shutil
import os
import pprint

#https://moonbooks.org/Articles/How-to-read-a-MODIS-HDF-file-using-python-/
#https://hdfeos.org/software/pyhdf.php
# environment: python 3.6 anacoda(smoke)

# this one take in test.hdf, read data from Optical_Depth_047,
# Optical_Depth_047 contain 3 or 4 array, representing the data from 3 or 4 overpass in a day.
# we always use the first, the overpass around 10am.
# get the array, replace Null by 0, multiply by 2, replace the original data.

shutil.copyfile('test copy.hdf','test.hdf')


file = SD('test.hdf', SDC.WRITE|SDC.READ)




datasets_dic = file.datasets()

for idx,sds in enumerate(datasets_dic.keys()):
    print(idx,sds)


sds_obj = file.select('Optical_Depth_047')


data = sds_obj.get() # get sds data
print(data.shape)


#print(data)

#pprint.pprint( sds_obj.attributes() )

array1 = numpy.array(data[0])
array2 = numpy.array(data[0])

array1[array1 == -28672 ] = 0
array2[array2 == -28672 ] = 0
print(array1)

print(array1+array2)
array3 = array1+array2

elements = data

elements[0] = array3
#print("elements",elements)
data = elements
print(data)
sds_obj[:] = data


# Terminate access to the data set
sds_obj.endaccess()


# Close the file
file.end()


#global_attrs = file.attributes()

#pprint.pprint(global_attrs)
#print('time overpass:',global_attrs['Orbit_time_stamp'])
from pyhdf.SD import SD, SDC
import numpy
import shutil
import os
from datetime import datetime



start_time = datetime.now()

# guide for pyhdf
#https://moonbooks.org/Articles/How-to-read-a-MODIS-HDF-file-using-python-/
#https://hdfeos.org/software/pyhdf.php
# environment: python 3.6 anacoda(smoke)
# numpy 1.21.4
# pyhdf 0.10.3


# input test.hdf and all MCD19A2 smoke hdf files under under '/2011' (https://lpdaac.usgs.gov/products/mcd19a2v006/)
# outputs the average for each grid subject to QA filter.

# We use layer Optical_Depth_047 in MCD19A2. Each Optical_Depth_047 layer contains 3 to 5 arrays, representing the data from 3 to 5 overpasses in a day.
# get the average of valid Optical(aerosal) Depth in each grid from all overpasses and all hdf files.
# valid data means cloud == 'clear' see MCD19_User_Guide_V6


# cloud mask QA '001' is clear '010' is partly cloudy. '001' --- 'clear' is recommended
QA = ['001']
year = '2011'
# ['h19v04','h19v05','h20v04','h20v05']
tile_list = ['h19v04','h19v05','h20v04','h20v05']


# create a copy of template file
shutil.copyfile('test.hdf', 'test combined.hdf')
# open it
file = SD('test combined.hdf', SDC.WRITE|SDC.READ)

# get the datasets
datasets_dic = file.datasets()

# get specific layer 'Optical_Depth_047'
sds_obj = file.select('Optical_Depth_047')
data = sds_obj.get() # get sds data
#print(data.shape)

# prepare empty array
array_base = numpy.array(data[0])
array_base[array_base != -9999999999 ] = 0
array_cloud = numpy.array(data[0])
array_cloud[array_cloud != -9999999999 ] = 0
array_0 = numpy.array(data[0])
array_0[array_0 != -9999999999 ] = -28672

#print("array_base:",array_base)

# uncomment print to see all layers
for idx,sds in enumerate(datasets_dic.keys()):
    pass
    #print(idx,sds)



# get the list of all files to be combined
file_list = []
for filex in os.listdir(year):
    name = os.path.basename(filex)

    if filex.startswith("MCD19A2"):
        file_list.append(filex)
        print('name:', name)

count = 0
for f in file_list:
    #name = os.path.basename(f)
    #print('name',name)
    file1 = SD(year+'/'+f, SDC.WRITE | SDC.READ)

    datasets_dic = file1.datasets()

    sds_obj1 = file1.select('Optical_Depth_047')
    sds_obj2 = file1.select('AOD_QA')

    data1 = sds_obj1.get()  # get sds data
    data2 = sds_obj2.get()  # get sds data
    #print(data2.shape)
    #print('data2,', data2[0])
    for i in range(len(data1)):

        # set element ==1 if cloud == 'clear' see MCD19_User_Guide_V6
        qa_cloud = lambda t: int(str(format(t, 'b').zfill(16))[0:3] in QA)
        vfunc = numpy.vectorize(qa_cloud)
        #print('vfunc:',vfunc(data2[i]))

        data2_cloud = vfunc(data2[i])
        #print(numpy.multiply(data1[i], data2_cloud))

        array_add1 = numpy.array(data1[i])
        array_add1[array_add1 == -28672] = 0
        #print(array_add1,data2_cloud)
        array_add1 = numpy.multiply(array_add1, data2_cloud)
        #print('array_add:', array_add)

        array_base+=array_add1
        array_cloud += data2_cloud

        print('count,',count,',overpass:',i)
        #print(array_base, array_cloud)
    count +=1
    sds_obj1.endaccess()
    file1.end()



#array_base = array_base /count

print('array_base',array_base)
print('array_cloud',array_cloud)

array_base = numpy.divide(array_base, array_cloud, out=array_0.astype(float), where=array_cloud!=0)

print('array_base2',array_base)


elements = data

elements[0] = array_base
elements[1] = array_cloud
#print("elements",elements)
data = elements
#print(data)
sds_obj[:] = elements


# Terminate access to the data set
sds_obj.endaccess()


# Close the file
file.end()
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))

#global_attrs = file.attributes()

#pprint.pprint(global_attrs)
#print('time overpass:',global_attrs['Orbit_time_stamp'])


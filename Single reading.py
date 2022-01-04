from pyhdf.SD import SD, SDC
import pprint

#https://moonbooks.org/Articles/How-to-read-a-MODIS-HDF-file-using-python-/

file_name = 'MCD19A2.A2018001.h19v05.006.2018121012939.hdf'
file = SD(file_name, SDC.READ)

print(file.info())

datasets_dic = file.datasets()

for idx,sds in enumerate(datasets_dic.keys()):
    print(idx,sds)

sds_obj = file.select('Optical_Depth_047')



data = sds_obj.get() # get sds data
print(data.shape)
print(data)
print(len(data))


pprint.pprint( sds_obj.attributes() )

for key, value in sds_obj.attributes().items():
    print(key, value)
    if key == 'add_offset':
        add_offset = value
    if key == 'scale_factor':
        scale_factor = value
data = (data - add_offset) * scale_factor
print(data)


global_attrs = file.attributes()

#pprint.pprint(global_attrs)
print('time overpass:',global_attrs['Orbit_time_stamp'])
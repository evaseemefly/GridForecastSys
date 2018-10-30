import netCDF4 as nc
import numpy as np
import os
from GridForecastSys import settings
from apps.GIS.model_middle import WaveModel

readDirPath=settings.NCReader_DIR

# def read():
#     # 修改当前读取路径
#     os.chdir(readDirPath)

class NCEnvironment:
    def __init__(self,read_type):
        self.factory=ReadFactory().make_reader(read_type)


    def read(self,lat,lon):
        return self.factory.read(lat,lon)

class WaveNcReader:
    def __init__(self,path,filename):
        '''
            读取指定路径下的指定名称的nc文件
        :param path:
        :param name:
        :return:
        '''
        self.path=path
        self.filename=filename

    def read(self,lat,lng):
        '''
            根据经纬度返回连续预报值数组
        :param lat:
        :param lng:
        :return:
        '''

        # 1 修改当前工作目录
        self.updateCurrentPaht()

        # 2 读取nc文件
        nc_obj=nc.Dataset(self.filename)

        final_arr=nc_obj.variables['swh'][:].data

        # 3 根据经纬度获取该经纬度在xy坐标上的位置
        lat_index = np.where(nc_obj.variables['latitude'][:].data == lat)[0]
        lng_index = np.where(nc_obj.variables['longitude'][:].data == lng)[0]

        # 3 进行列表推导，获取最终的预报值
        finnal_val=[temp[0][lat_index,lng_index][0] for temp in final_arr]
        return finnal_val

    def updateCurrentPaht(self):
        '''
            修改当前工作目录
        :return:
        '''
        if self.path!=None:
            os.chdir(self.path)

class ReadFactory:
    def __init__(self):
        '''

        '''

        pass

    def make_reader(self,read_type):

        if read_type=='nc_reader':
            # factory=NCEnvironment(WaveNcReader(readDirPath,'global_ecmwf_det_wve_2018082112.nc'))
            # factory.reader()
            return WaveNcReader(readDirPath,'global_ecmwf_det_wve_2018082112.nc')

# read= NCEnvironment('nc_reader')
# finall_arr= read.read(79.0,0.25)
# pass





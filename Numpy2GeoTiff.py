import numpy as np
from osgeo import gdal, gdal_array, osr, ogr

def CreateMultiGeoTiff(Array, Name, driver, NDV, GeoT, Projection, DataType): 
    Array[np.isnan(Array)] = NDV
    DataSet = gdal.GetDriverByName(driver).Create(Name, Array.shape[2], Array.shape[1], Array.shape[0], DataType)
    DataSet.SetGeoTransform(GeoT)
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(Projection)
    DataSet.SetProjection(srs.ExportToWkt() )
    for i, image in enumerate(Array, 1):
        DataSet.GetRasterBand(i).WriteArray( image )
        DataSet.GetRasterBand(i).SetNoDataValue(NDV)
    DataSet.FlushCache()
    return Name

def save2File(rA, outname, nrows, ncols, geo_transform):  # Resolution for the 6min
    # create the output image
    # Note that in the geo transform the third and sixth parameters are equal to the Arc/Info generate fishnet
    # Y-coordinate paramenter (defining the rotation of the final grid)
    # LCORD
    outDs = gdal.GetDriverByName('GTiff').Create(outname, ncols, nrows, 1, gdal.GDT_Float32)
    outBand = outDs.GetRasterBand(1)
    outBand.WriteArray(rA)
    outDs.SetGeoTransform(geo_transform)
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326)
    outDs.SetProjection(srs.ExportToWkt())
    outDs = None

    """
    geotransform[0] = top left x
    geotransform[1] = w-e pixel resolution
    geotransform[2] = 0
    geotransform[3] = top left y
    geotransform[4] = 0
    geotransform[5] = n-s pixel resolution (negative value)
    """

    
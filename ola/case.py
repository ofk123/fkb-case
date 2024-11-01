import geopandas as geopd
import numpy as np

def error_geometries(geodf, outfile, max_distance=1.0):
    
    wrong = []
    Points = geodf[geodf.geometry.type == 'Point']
    nPoints = Points.index.size
    LineStrings = geodf[geodf.geometry.type == 'LineString']
    nLineStrings = LineStrings.index.size
    
    duplicates = Points[Points.duplicated(subset='geometry')]
    if duplicates.index.size > 0:
        wrong += duplicates.index.values.tolist()

    geom_points = Points.geometry.tolist()
    i_points = Points.index.tolist()
    
    for i in range(nPoints):
        for j in range(i + 1,nPoints):
            if geom_points[i].distance(geom_points[j]) <= max_distance:
                wrong += [i_points[i], i_points[j]]

    return geodf.loc[np.unique(np.array(wrong)).tolist()].to_file(outfile, driver='GeoJSON')
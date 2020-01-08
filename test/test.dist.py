import math

a= 6378.137#equitorial radius in km
b= 6356.752#polar radius in km

def Distance(lat1, lons1, lat2, lons2):
    lat1=math.radians(lat1)
    lons1=math.radians(lons1)
    R1=(((((a**2)*math.cos(lat1))**2)+(((b**2)*math.sin(lat1))**2))/((a*math.cos(lat1))**2+(b*math.sin(lat1))**2))**0.5 #radius of earth at lat1
    x1=R1*math.cos(lat1)*math.cos(lons1)
    y1=R1*math.cos(lat1)*math.sin(lons1)
    z1=R1*math.sin(lat1)

    lat2=math.radians(lat2)
    lons2=math.radians(lons2)
    R1=(((((a**2)*math.cos(lat2))**2)+(((b**2)*math.sin(lat2))**2))/((a*math.cos(lat2))**2+(b*math.sin(lat2))**2))**0.5 #radius of earth at lat2
    x2=R1*math.cos(lat2)*math.cos(lons2)
    y2=R1*math.cos(lat2)*math.sin(lons2)
    z2=R1*math.sin(lat2)

    return ((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)**0.5

print(Distance(35.699720, 51.337974,35.700182,51.355169))


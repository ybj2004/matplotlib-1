import pylab as P
import numpy
from mpl_toolkits.basemap import Basemap as Basemap1 
from numpy import ma

class Basemap(Basemap1):
    # subclass Basemap and add bluemarble method.
    def bluemarble(self,masked=False):
        """display 'blue marble next generation' image from http://visibleearth.nasa.gov/"""
        try:
            from PIL import Image
        except ImportError:
            raise ImportError('bluemarble method requires PIL (http://www.pythonware.com/products/pil/)')
        from matplotlib.image import pil_to_array
        
        # read in jpeg image to rgba array of normalized floats.
        pilImage = Image.open('bmng.jpg')
        rgba = pil_to_array(pilImage)
        rgba = rgba.astype(numpy.float32)/255. # convert to normalized floats.
        
        # define lat/lon grid that image spans (projection='cyl').
        nlons = rgba.shape[1]; nlats = rgba.shape[0]
        delta = 360./float(nlons)
        lons = numpy.arange(-180.+0.5*delta,180.,delta)
        lats = numpy.arange(-90.+0.5*delta,90.,delta)

        if self.projection != 'cyl':
            # transform to nx x ny regularly spaced native projection grid
            # nx and ny chosen to have roughly the same horizontal res as original image.
            dx = 2.*numpy.pi*m.rmajor/float(nlons)
            nx = int((self.xmax-self.xmin)/dx)+1; ny = int((self.ymax-self.ymin)/dx)+1
            rgba_warped = ma.zeros((ny,nx,4),numpy.float64)
            # interpolate rgba values from proj='cyl' (geographic coords) to 'lcc'
            # if masked=True, values outside of projection limb will be masked.
            for k in range(4):
                rgba_warped[:,:,k] = self.transform_scalar(rgba[:,:,k],lons,lats,nx,ny,masked=masked)
            # make points outside projection limb transparent.
            rgba_warped = rgba_warped.filled(0.)
            # plot warped rgba image.
            im = self.imshow(rgba_warped)
        else:
            im = self.imshow(rgba)
        return im

# create new figure
fig=P.figure()
# define cylindrical equidistant projection.
m = Basemap(projection='cyl',llcrnrlon=-180,llcrnrlat=-90,urcrnrlon=180,urcrnrlat=90,resolution='l')
# plot (unwarped) rgba image.
im = m.bluemarble()
# draw coastlines.
m.drawcoastlines(linewidth=0.5,color='0.5')
# draw lat/lon grid lines.
m.drawmeridians(numpy.arange(-180,180,60),labels=[0,0,0,1],color='0.5')
m.drawparallels(numpy.arange(-90,90,30),labels=[1,0,0,0],color='0.5')
P.title("Blue Marble image - native 'cyl' projection",fontsize=12)
print 'plot cylindrical map (no warping needed) ...'

# create new figure
fig=P.figure()
# define orthographic projection centered on North America.
m = Basemap(projection='ortho',lat_0=40,lon_0=40,resolution='l')
# plot warped rgba image.
im = m.bluemarble(masked=True)
# draw coastlines.
m.drawcoastlines(linewidth=0.5,color='0.5')
# draw lat/lon grid lines every 30 degrees.
m.drawmeridians(numpy.arange(0,360,30),color='0.5')
m.drawparallels(numpy.arange(-90,90,30),color='0.5')
P.title("Blue Marble image warped from 'cyl' to 'ortho' projection",fontsize=12)
print 'warp to orthographic map ...'

# create new figure
fig=P.figure()
# define Lambert Conformal basemap for North America.
m = Basemap(llcrnrlon=-145.5,llcrnrlat=1.,urcrnrlon=-2.566,urcrnrlat=46.352,\
            rsphere=(6378137.00,6356752.3142),lat_1=50.,lon_0=-107.,\
            resolution='i',area_thresh=1000.,projection='lcc')
im = m.bluemarble()
# draw coastlines.
m.drawcoastlines(linewidth=0.5,color='0.5')
# draw parallels and meridians.
# label on left, right and bottom of map.
parallels = numpy.arange(0.,80,20.)
m.drawparallels(parallels,labels=[1,1,0,1],color='0.5')
meridians = numpy.arange(10.,360.,30.)
m.drawmeridians(meridians,labels=[1,1,0,1],color='0.5')
P.title("Blue Marble image warped from 'cyl' to 'lcc' projection",fontsize=12)
print 'warp to lambert conformal map ...'

# create new figure
fig=P.figure()
# define oblique mercator map.
m = Basemap(height=24000000,width=12000000,
            resolution=None,projection='omerc',\
            lon_0=-100,lat_0=15,lon_2=-120,lat_2=65,lon_1=-50,lat_1=-55)
# plot warped rgba image.
im = m.bluemarble()
# draw lat/lon grid lines every 20 degrees.
m.drawmeridians(numpy.arange(0,360,20),color='0.5')
m.drawparallels(numpy.arange(-80,81,20),color='0.5')
P.title("Blue Marble image warped from 'cyl' to 'omerc' projection",fontsize=12)
print 'warp to oblique mercator map ...'

P.show()

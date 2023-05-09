'''
@autor: Luisa María Zapata Saldarriaga, Universidad de Antioquia, luisazapatasaldarriaga@gmail.com  
'''

from PIL import Image
from numpy import ceil 
from matplotlib import pyplot as plt
import io
import base64
import time

def fig2img(fig):
  """
  Convert a Matplotlib figure to a PIL Image and return it
  """
  import io
  buf = io.BytesIO()
  fig.savefig(buf,format='png')
  buf.seek(0)
  img = Image.open(buf)
  return img

def fig2img_encode(fig):
  """
  Convert a Matplotlib figure to a PIL Image and return encode 

  Parameters
  ----------
    fig: Object to matplolib  


  Returns
  ----------
    my_base64_jpgData: str
      encode base64 to image 
  """
  tick=time.perf_counter()  
  buf = io.BytesIO()
  fig.savefig(buf ,format='jpg')
  buf.seek(0)
  # fig=fig.figure
  # buf=Image.frombytes('RGB',fig.canvas.get_width_height(),fig.canvas.tostring_rgb())
  my_base64_jpgData = base64.b64encode(buf.read())
  tock=time.perf_counter()  
  print('encode::::::::::::::::::::::::::',tock-tick)
  print(type(my_base64_jpgData))
  return my_base64_jpgData
  
def getSize(imageList):
    for image in imageList:
        img_width, img_height = image.size
    return img_width, img_height

def createCollage(imageList, frame_width, images_per_row,name_img,title,save=False):
    imageList=[fig2img(x) for x in imageList] 
    img_width, img_height = getSize(imageList)
    #scaling factor
    sf = (frame_width-(images_per_row-1))/(images_per_row*img_width)

    scaled_img_width =int(ceil(img_width*sf))
    scaled_img_height =int(ceil(img_height*sf))

    number_of_rows = int(ceil(len(imageList)/images_per_row))
    frame_height = int(ceil(sf*img_height*number_of_rows))

    new_im = Image.new('RGB', (frame_width, frame_height),'white')

    i,j=0,0
    for num, im in enumerate(imageList):
        if num%images_per_row==0:
            i=0
        
        #resizing opened image
        im.thumbnail((scaled_img_width,scaled_img_height))
        #Iterate through a 3 x 3 grid
        y_cord = (j//images_per_row)*scaled_img_height
        y_cord=int(y_cord)
        new_im.paste(im, (i,y_cord))
        # print(i, y_cord)
        i=(i+scaled_img_width)
        j+=1
    # new_im.show()
    if save: 
      from PIL import ImageDraw
      draw = ImageDraw.Draw(new_im)
      msg=title
      w, h = draw.textsize(msg)
      # specifying coordinates and colour of text
      draw.text(((img_width-w)/2+80,10), msg, (0, 0, 0))
      new_im.save(name_img, "PNG")
    return new_im
    

def create_collage(cols,rows,width, height, listofimages):
  thumbnail_width = width//cols
  thumbnail_height = height//rows
  size = thumbnail_width, thumbnail_height
  new_im = Image.new('RGB', (width, height), 'white')
  ims = []
  for p in listofimages:
    #im = Image.open(p)
    #im.thumbnail(size)
    #ims.append(im)
    ims.append(fig2img(p).thumbnail(size))
  i = 0
  x = 0
  y = 0
  for col in range(cols):
      for row in range(rows):
          if i>= len(ims):
            pass
          else:
            new_im.paste(ims[i], (x, y))
            i += 1
            x += thumbnail_width
      y += thumbnail_height 
      x = 0
  plt.imshow(new_im)
  return 
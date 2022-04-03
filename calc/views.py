from django.shortcuts import render,redirect
from django.http import HttpResponse
from PIL import Image
from .models import Image_try
from .forms import ImageForm
from django.shortcuts import render_to_response
from django.template import RequestContext
import os
# Create your views here.
def test_res(request):
    img_data1 = request.FILES.get("cover_img")
    img_name1 = "image15"
    img_obj = Image_try(name = img_name1,imagefile = img_data1).save()
    lastimage= Image_try.objects.last()
    imagefile= lastimage.imagefile

   
    im1 = Image.open(imagefile)

    img_data2 = request.FILES.get("hide_img")
    img_name2 = "image61"
    img_obj = Image_try(name = img_name2,imagefile = img_data2).save()
    lastimage= Image_try.objects.last()
    imagefile= lastimage.imagefile
    im2 = Image.open(imagefile)
    size1 = im1.size[0]
    size2 = im1.size[1]
    size3 = im2.size[0]
    size4 = im2.size[1]
    return render(request,'test.html',{'s1':size1, 's2':size2, 's3':size3, 's4':size4})



def home(request):
    return render(request,'index.html',{'name':'Pratik'})

def browse1(request):
    return render(request,'browse1.html',{'val':False})

def feat(request):
    return render(request,'features.html')

def showimage(request):
    img_data = request.FILES.get("cover_img")
    img_name = "image5"
    img_obj = Image_try(name = img_name,imagefile = img_data).save()
    lastimage= Image_try.objects.last()
    imagefile= lastimage.imagefile

   
    im1 = Image.open(imagefile)
   # pixelscover = im1.load()
    pixelscover = im1.load()


    img_data = request.FILES.get("hide_img")
    img_name = "image6"
    img_obj = Image_try(name = img_name,imagefile = img_data).save()
    lastimage= Image_try.objects.last()
    imagefile= lastimage.imagefile

   
    im2 = Image.open(imagefile)
   # pixelscover = im1.load()
    
    pixelsenc = im2.load()

    mylist = []
    mylist1 = []
    mylist2 = []
    x = 0
    k = 0

   
    ##Img size is front problem
    if(im2.size[0] > im1.size[0] or im2.size[1] + 4 > im1.size[1]):
        return render(request,'browse1.html',{'val':True})
 
    size1 = im2.size[0]
    size2 = im2.size[1]

    size_blk = size1*size2

    size1 = '{0:024b}'.format(size1)
    size2 = '{0:024b}'.format(size2)

    size_pix1 = ['','','','','','']
    size_pix2 = ['','','','','','']

    y = 0

    #Get all pixel info in mylist2
    for i in range(im2.size[0]):
        for j in range(im2.size[1]):
            mylist2.extend(pixelsenc[i, j])
            
    #Take set of 4bits of size1 and left shift by 4
    for i in range(0,6):
        for j in range(0,4):
            size_pix1[i] = size_pix1[i] + size1[4*i + j]
        for j in range(0,4):
            size_pix1[i] = size_pix1[i] + '0'
        mylist.extend([int(size_pix1[i],2)])
            
    #Take set of 4bits of size2 and left shift by 4
    for i in range(0,6):
        for j in range(0,4):
                size_pix2[i] = size_pix2[i] + size2[4*i + j]
        for j in range(0,4):
            size_pix2[i] = size_pix2[i] + '0'
        mylist.extend([int(size_pix2[i],2)])

            
    #Utilize Extra Space left after overlapping images by putting lsbs
    #Remember to left shift as we only need msbs
    for i in range(im1.size[0]):
            for j in range(im1.size[1]):
                if j >= im2.size[1] or i >= im2.size[0]:
                    if k <= 3*size_blk:
                        mylist.extend([int('{0:08b}'.format(l)[4:8] + '0000', 2) for l in mylist2[k:k+3]])
                        k = k + 3
                    else:
                        mylist.extend((0,0,0))
                else:
                    mylist.extend(pixelsenc[i, j])                    

    for i in range(im1.size[0]):
        for j in range(im1.size[1]):
            mylist1.extend(pixelscover[i, j])
            

    #MSB + MSB
    for i in range(im1.size[0]):
        for j in range(im1.size[1]):
            pixelscover[i, j] = (int("{0:08b}".format(mylist1[x])[0:4] + "{0:08b}".format(mylist[x])[0:4], 2),
                                 int("{0:08b}".format(mylist1[x + 1])[0:4] + "{0:08b}".format(mylist[x + 1])[0:4], 2),
                                 int("{0:08b}".format(mylist1[x + 2])[0:4] + "{0:08b}".format(mylist[x + 2])[0:4], 2))
            x = x + 3

    im2.close()
    sert = os.getcwd()
    sert = sert.replace("\\","/")
    a = sert.split('/')
    fet = ''
    for i in a:
	    if i == 'calc':
		    break
	    else:
		    fet = fet + i + '/'
    im1.save(fet + 'media/images/hidden.tif')
    im1.close()

    return render(request,'browse2.html')

def dectimage(request):
    img_data = request.FILES.get("dect_img")
    img_name = "image6"
    img_obj = Image_try(name = img_name,imagefile = img_data).save()
    lastimage= Image_try.objects.last()
    imagefile= lastimage.imagefile

   
    im1 = Image.open(imagefile)
    pixelscover = im1.load()

    im2 = Image.new(im1.mode, im1.size)
    pixelsucover = im2.load()

    mylist = []
    lsb = []
    extra = []
    x = 12
    y = 0


    for i in range(im1.size[0]):
        for j in range(im1.size[1]):
            mylist.extend(pixelscover[i, j])

    #First 4 pixels resemble resolution
    size1 = int('{0:08b}'.format(mylist[0])[4:8] + '{0:08b}'.format(mylist[1])[4:8] + '{0:08b}'.format(mylist[2])[4:8] + '{0:08b}'.format(mylist[3])[4:8] + '{0:08b}'.format(mylist[4])[4:8] + '{0:08b}'.format(mylist[5])[4:8],2)
    size2 = int('{0:08b}'.format(mylist[6])[4:8] + '{0:08b}'.format(mylist[7])[4:8] + '{0:08b}'.format(mylist[8])[4:8] + '{0:08b}'.format(mylist[9])[4:8] + '{0:08b}'.format(mylist[10])[4:8] + '{0:08b}'.format(mylist[11])[4:8],2)

    size_blk = im1.size[0]*im1.size[1] - size1*size2 - 4

    #First Column Scan
    for j in range(3*(4+size2),3*(im1.size[1])):
        lsb.extend([mylist[j]])

    new_big = 3*(im1.size[1])    

    #Remaining Column Scan
    for i in range(1,im1.size[0]):
        lsb.extend((mylist[new_big:new_big + 12]))
        #Till Scanner is within width of enc image
        if i <= size1 - 1:
            new_big = new_big + 12 + 3*size2
            for j in range(4+size2,im1.size[1]):
                lsb.extend((mylist[new_big:new_big + 3]))
                new_big = new_big + 3
        else:
            for j in range(4,im1.size[1]):
                lsb.extend((mylist[new_big:new_big + 3]))
                new_big = new_big + 3
    
    for i in range(0,12):
        mylist.extend([0])

    #if size_blk is passed that means there are no extra lsbs so append 0's    
    for i in range(im1.size[0]):
        if i >= size1:
            break
        for j in range(im1.size[1]):
            if j >= size2:
                break
            if y >= size_blk*3:
                extra = [0]*3
            else:
                extra = [lsb[y],lsb[y+1],lsb[y+2]]
                y = y + 3
                
            pixelsucover[i, j] = (int("{0:08b}".format(mylist[x])[4:8] + "{0:08b}".format(extra[0])[4:8], 2),
                                  int("{0:08b}".format(mylist[x + 1])[4:8] + "{0:08b}".format(extra[1])[4:8], 2),
                                  int("{0:08b}".format(mylist[x + 2])[4:8] + "{0:08b}".format(extra[2])[4:8], 2))
            x = x + 3
        x = im1.size[1]*3*i + 12

    im2 = im2.crop((0, 0, int(size1), int(size2)))


    im1.close()
    sert = os.getcwd()
    sert = sert.replace("\\","/")
    a = sert.split('/')
    fet = ''
    for i in a:
	    if i == 'calc':
		    break
	    else:
		    fet = fet + i + '/'
    im2.save(fet + 'media/images/unhidden.jpg')
    im2.close()

    return render(request,'browse3.html')
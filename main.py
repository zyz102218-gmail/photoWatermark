import os

try:
    from PIL import Image, ImageDraw, ImageFont
    import exifread
except ModuleNotFoundError:
    print("Module ERROR. Install Pillow, exif first")
    
# Get icons in ./Icons

icons = {}
for file in os.listdir('./Icons'):
    if ".png" in file:
        icons[file.split('.')[0]] = file
if not icons:
    raise Exception("No Icon files")


# Get input pictures in ./Pics
pics = []
for file in os.listdir("./Pics"):
    if ".jpg" in file or ".jpeg" in file:
        pics.append(file)

if not pics:
    raise Exception("No input pics")
exifs = {}


for pic in pics:
    # extract information which is needed for making watermark
    with open('Pics/' + pic,'rb') as f:
        try: 
            exif_information = exifread.process_file(f)
            exif_needed = {}
            exif_needed['Model'] = exif_information['Image Make'].printable + " " + exif_information['Image Model'].printable
            # exif_needed['Time'] = exif_information['EXIF DateTimeOriginal']
            time_ = exif_information['EXIF DateTimeOriginal'].printable.split()
            date_ = '.'.join(time_[0].split(":"))
            exif_needed['Time'] = date_ +' '+  time_[1]
            exif_needed['FocalLength'] = exif_information['EXIF FocalLength'].printable + "mm"
            exif_needed['F'] = 'f/' + "{:.1f}".format(eval(exif_information['EXIF FNumber'].printable))
            exif_needed['ExpTime'] = exif_information['EXIF ExposureTime'].printable
            exif_needed['ISO'] = "ISO"+exif_information['EXIF ISOSpeedRatings'].printable
            exif_needed['width'] = int(exif_information['EXIF ExifImageWidth'].printable)
            exif_needed['height'] = int(exif_information['EXIF ExifImageLength'].printable)
        except:
            print("{} exif information insuffcient, failed to add watermark.".format(pic))
            continue
        
        

        # pass
        
    # Keep long side the same as the input picture, 
    # and make width as kept in the same 1/2
    WaterMark = Image.new(mode='RGB',size = (exif_needed['width'],int(exif_needed['width']/10)),color='white')
    __draw = ImageDraw.Draw(WaterMark)
    __font_1 = ImageFont.truetype('Fonts/MiSans-Demibold.ttf',size=int(exif_needed['width']/10/6)) # Height of font is about 1/6 of the height of watermark
    __font_2 = ImageFont.truetype('Fonts/MiSans-Thin.ttf',size=int(exif_needed['width']/10/10))
    
    __draw.text((int(exif_needed['width']/40),int(exif_needed['width']/40)),
                text=exif_needed['Model'],font=__font_1,
                fill='black',stroke_width=1)
    
    __draw.text((int(exif_needed['width']/40),int(exif_needed['width']/10*32/60)),
                text=exif_needed['Time'],font=__font_2,
                fill='grey',stroke_width=1)

    __draw.line((int(exif_needed['width']*0.75),int(exif_needed['width']/40))+(int(exif_needed['width']*0.75),
                                                                               int(exif_needed['width']/30*2)),
                                                                            fill='grey',width=1)
    photo_t = " ".join([exif_needed['FocalLength'],exif_needed['F'],exif_needed['ExpTime'],exif_needed['ISO']])
    __draw.text((int(exif_needed['width']*45.5/60),int(exif_needed['width']/40)),
                text=photo_t,font=__font_1,
                fill='black',stroke_width=1)
    #location = input("Location of picture {}(xx xx xx N xx xx xx E):".format(pic))
    
    
    location = u"31° 11\' 29.76\" N  121° 17\' 50.64\" E"
    # location part need to be re-write
    
    __draw.text((int(exif_needed['width']*45.5/60),int(exif_needed['width']/10*32/60)),
                text = location,font=__font_2,
                fill = 'grey',stroke_width=1)
    
    # add logo
    # caculate size of logo
    __height = int((exif_needed['width']/10)*25/60)
    __width = __height
    band_icon = Image.open('Icons/'+icons[exif_needed['Model'].split()[0].lower()])
    band_icon = band_icon.resize((__width,__height))
    # place logo
    WaterMark.paste(band_icon,(int(exif_needed['width']*0.7),int(exif_needed['width']/40)),mask=band_icon)
    # Watermark done, start paste
    Org_pic = Image.open('Pics/' + pic)
    output = Image.new(mode='RGB',size = (Org_pic.width,int(Org_pic.height+Org_pic.width*1/10)),color='white')
    output.paste(Org_pic,(0,0))
    output.paste(WaterMark,(0,Org_pic.height))
    # output.show()
    output.save('Output/'+pic.split('.')[0]+'_watermarked.png',format='png')
    # WaterMark.save("Watermark_test.png")
    # WaterMark.show()
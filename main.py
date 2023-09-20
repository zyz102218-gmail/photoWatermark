import os
try:
    import PIL 
    import exifread
except ModuleNotFoundError:
    print("Module ERROR. Install Pillow, exif first")
    
# Get icons in ./Icons
'''
icons = []
for file in os.listdir('./Icons'):
    if ".png" in file or ".jpg" in file or ".jpeg" in file:
        icons.append(file)
if not icons:
    raise Exception("No Icon files")
'''

# Get input pictures in ./Pics
pics = []
for file in os.listdir("./Pics"):
    if ".png" in file or ".jpg" in file or ".jpeg" in file:
        pics.append(file)

if not pics:
    raise Exception("No input pics")
exifs = {}

# extract information which is needed for making watermark
for pic in pics:
    with open('Pics/' + pic,'rb') as f:
        exif_information = exifread.process_file(f)
        exif_needed = {}
        exif_needed['Model'] = exif_information['Image Make'].printable + " " + exif_information['Image Model'].printable
        # exif_needed['Time'] = exif_information['EXIF DateTimeOriginal']
        time_ = exif_information['EXIF DateTimeOriginal'].printable.split()
        date_ = '.'.join(time_[0].split(":"))
        exif_needed['Time'] = date_ +' '+  time_[1]
        exif_needed['FocalLength'] = exif_information['EXIF FocalLength'].printable + "mm"
        exif_needed['F'] = 'f/' + "{:.1f}".format(eval(exif_information['EXIF FNumber'].printable))
        exif_needed['ExpTime'] = exif_information['EXIF ExposureTime']
        exif_needed['ISO'] = "ISO"+exif_information['EXIF ISOSpeedRatings'].printable
        exif_information[pic] = exif_needed
        pass
        # pass
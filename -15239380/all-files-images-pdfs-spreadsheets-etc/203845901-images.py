import os
from PIL import Image, ImageCms
import subprocess as sub
from io import BytesIO

folder = "C:\Data\Blog"
os.chdir(folder)

filelist = []
for filename in os.listdir(os.curdir):
    if filename.endswith('jpg') or filename.endswith('jpeg'):
        try:
            image = Image.open(filename)
        except:
            continue

        width = image.size[0]
        height = image.size[1]
        mb = round(os.path.getsize(filename)/1048576.0, 2)
        res = (width*height)/1000000
        compression = round(mb/res,5)

        convert_params = []
        if width > 2000:
            new_height = 2000 * height // width
            convert_params += ['-resize', f'2000x{new_height}']
        if compression > 0.5:
            convert_params += ['-quality', '92']
        icc = image.info.get('icc_profile', b'')
        if icc:
            f = BytesIO(icc)
            prf = ImageCms.ImageCmsProfile(f)
            if not "sRGB" in prf.profile.profile_description:
                convert_params += ['-profile', 'sRGB.icc']

        if convert_params:
            filelist.append(str(filename.encode("utf-8")))
            convert_params +=  [filename]
            sub_list = ['magick', 'convert', filename]
            sub_list += convert_params
            sub.check_output(sub_list)

from PIL import Image, ImageFilter, ImageEnhance

# opening the image stored in the local path.

FILENAME = "T_Cupid_V8_Skin19_D.tga"
EXT = "tga"

NEWNAME = FILENAME.split('.')

img = Image.open(FILENAME)
img.save(str(NEWNAME[0]) + "_bak." + EXT)
img.show()

img = Image.open(FILENAME)
enhancer = ImageEnhance.Brightness(img)

# to reduce brightness by 50%, use factor 0.5
img = enhancer.enhance(1.2)


img.show()
img.save(FILENAME)
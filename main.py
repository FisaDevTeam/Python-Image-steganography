#Library used to modify image
from PIL import Image

#Encode data to 8-bit binary in a list
def binary_list(data):
  return [format(ord(i), '08b') for i in data]

#Modify pixel according to bin_list
def pixel_modifier(pix, toEncode):
  bin_list = binary_list(toEncode)
  len_bin_list = len(bin_list)
  img_data = iter(pix)

  for i in range(len_bin_list):
    pix = [value for value in img_data.__next__()[:3] + img_data.__next__()[:3] + img_data.__next__()[:3]]

    #Pixel value is made odd for 1 and even for 0 binary code (while keeping it between 0 and 255)
    for j in range(0, 8): #8 for 8-bit binary
      if bin_list[i][j] == '0' and pix[j]% 2 != 0:
        pix[j] -= 1
      
      elif bin_list[i][j] == '1' and pix[j] % 2 == 0:
        if pix[j] == 0:
          pix[j] += 1
        else:
          pix[j] -= 1
    
    #For every data set, eigth pixel says whether to stop or to keep reading
    #0=keep reading, 1=stop

    if i + 1 == len_bin_list:
      if pix[-1] % 2 == 0:
        if pix[-1] == 0:
          pix[-1] += 1
        else:
          pix[-1] -= 1
    else:
      if pix[-1] % 2 != 0:
        pix[-1] -= 1
    
    #Return pixel tuple
    pix = tuple(pix)
    yield pix[0:3]
    yield pix[3:6]
    yield pix[6:9]

#Modifiy pixels in image variable
def encode_img(newimg, data):
  w = newimg.size[0]
  (x, y) = (0, 0)

  for pixel in pixel_modifier(newimg.getdata(), data):
    newimg.putpixel((x, y), pixel)
    if (x == w - 1):
      x = 0
      y += 1
    else:
      x += 1


#Encode data
def encode(path, new_path, data):
    image = Image.open(path, 'r')
    if (len(data) == 0): raise ValueError('Data is empty')

    new_img = image.copy()
    encode_img(new_img, data)
    new_img.save(new_path, str(new_path.split(".")[1].upper()))


#Decode data
def decode(path):
  image = Image.open(path, 'r')
  data = ""
  imgdata = iter(image.getdata())

  while True:
    pixels = [value for value in imgdata.__next__()[:3] + imgdata.__next__()[:3] + imgdata.__next__()[:3]]

    binstr = ""

    for i in pixels[:8]:
      if (i % 2 != 0):
        binstr += '1'
      else:
        binstr += '0'
      
    data += chr(int(binstr, 2))
    if pixels[-1] % 2 != 0:
      return data

def main():
  user_input = input(
"""1 : Encode
2 : Decode
""")
  if user_input == "1":
    path = input("Image path : ")
    new_path = input("Where to save : ")
    data = input("What do you want to encode : ")
    encode(path, new_path, data)

  elif user_input == "2":
    path = input("Image path : ")
    print("Decoded word : " + decode(path))


if __name__ == "__main__":
  main()
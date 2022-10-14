import os
if os.name == 'posix':
    os.system("/home/harsh/software/blender/blender-3.0.1-linux-x64/blender")
elif os.name == 'nt':
    file = 'C:\\Program Files\\Blender Foundation\\Blender 3.2\\blender.exe'
    os.system('"' + file + '"')
else:
    print("Operating system not recognized!")
    print("os.name =", os.name)
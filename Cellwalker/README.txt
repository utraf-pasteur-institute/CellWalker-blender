This folder contains the source code of the CellWalker-blender addon. If you only want to install the addon (not make changes to the source code), then please use the zip file provided outside this folder. You can use the zip file to install CellWalker-Blender addon in Blender.<br>

Instructions to setup an Anaconda python environment so that the external python packages will work inside the blender addon.

Start the Blender software and go to script tab, see python version in the scripting window first line:Example line- PYTHON INTERACTIVE CONSOLE 3.10.2 (main, Jan 27 2022, 08:34:43) [MSC v.1928 64 bit (AMD64)]

Create an Anaconda environment using the following command. Note that the python version specified here is 3.10 because the Blender's python version was 3.10.2.conda create --name cellwalker-blender python=3.10

Accept to install required packages for this environment and the command will install the environment named cellwalker-blender inside your Anaconda installation.You can check the folder in which this environment is installed. Go to folder-
<Your anaconda installation>\envs

Here you will see all the available environments. Each environment is in its own folder. When you install any other packages to a specific environment, they are installed inside the folder dedicated to that particular environment.

Now, start the Anaconda prompt command line window and activate the environment.

```bash
conda activate cellwalker-blender
```

Once activated, you should see the name of the environment in brackets at the beginning of the line- **(cellwalker-blender) C:\Users\harsh>**<br>
See the image below.<br>


Now you are inside the enviromnent 'cellwalker-blender'. This means, any package you will install or uninstall will happen inside the cellwalker-blender environment and it will not affect any other environments.<br>

On the command prompt run the following commands to install required modules.
```bash
pip install -r requirements.txt
```

On some systems (confirmed for Windows), the installation of the kimimaro package may give errors. This is because some dependencies need Microsoft Visual C++ 14.0 or greater. To resolve the issue download and install Microsoft C++ Build Tools from https://visualstudio.microsoft.com/visual-cpp-build-tools/Remember. Select Workloads and check the option of 'Desktop development using C++' during the installation. Then try installing kimimaro again using ```pip install kimimaro```.<br>

Once all the packages are installed, you have to define the path for your environment folder in the python_environment.txt file which is located 

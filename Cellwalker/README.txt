Download this folder and import it like a addon zip in Blender

Instructions to setup an Anaconda python environment so that the external python packages will work inside the blender addon.

Start the Blender software and go to script tab, see python version in the scripting window first line:Example line- PYTHON INTERACTIVE CONSOLE 3.10.2 (main, Jan 27 2022, 08:34:43) [MSC v.1928 64 bit (AMD64)]

Create an Anaconda environment using the following command. Note that the python version specified here is 3.10 because the Blender's python version was 3.10.2.conda create --name cellwalker-blender python=3.10

Accept to install required packages for this environment and the command will install the environment named cellwalker-blender inside your Anaconda installation.You can check the folder in which this environment is installed. Go to folder-
<Your anaconda installation>\envs

Here you will see all the available environments. Each environment is in its own folder. When you install any other packages to a specific environment, they are installed inside the folder dedicated to that particular environment.

Now you can activate the environment on the Anaconda command prompt.

conda activate cellwalker-blender

Once activated, you should see the name of the environment in brackets at the beginning of the line. See the image below.

(cellwalker-blender) C:\Users\harsh>

Now you are inside the enviromnent 'cellwalker-blender'. That means, any package you will install or uninstall now will happen inside the cellwalker-blender environment and it will not affect any other environments.

On the command prompt run the following commands to install required modules.

pip install -r requirements.txt

On some systems (confirmed for Windows), the installation of the kimimaro package may give errors. This is because some dependencies need Microsoft Visual C++ 14.0 or greater. To resolve the issue download and install Microsoft C++ Build Tools from https://visualstudio.microsoft.com/visual-cpp-build-tools/Remember to select Workloads and check the option of Desktop development using C++ during the installation.

Then try installing kimimaro again using 'pip install kimimaro.

Once all the packages are installed, you have to define the path for your environment folder in the python_environment.txt file which is located.

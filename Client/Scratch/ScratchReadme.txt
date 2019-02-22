How to install the extension into Scratch 2:

1: Extrace the Freenove_Three-wheeled_Smart_Car_Kit_for_Raspberry_Pi-master.zip file
2: cd into the Folder you extracted it to
2: run the following commands:

sudo cp ./Client/Scratch/piCar.js /usr/lib/scratch2/scratch_extensions
sudo cp ./Client/html/imgs/car_photo.jpg /usr/lib/scratch2/medialibrarythumbnails

3: NOTE: **only run the following command if you have only the default extensions already loaded in Scratch**
	If you have extensions already loaded, then add the last line of this extensions.json file into the one on your pi before the last "]"

sudo cp ./Client/Scratch/extensions.json /usr/lib/scratch2/scratch_extensions

4: cd into the Client folder and run the following command:

python ScratchServer.py

5: Run Scratch 2
6: Click "More Blocks"
7: Click "Add an extension"
8: You should now see the "Freenove PiCar" in the list of extensions, double click it to add them.


To use the blocks, always remember to run the "connect to" block first and finish off with a disconnect block.

If you don't disconnect you may not be able to connect to you car from another app (e.g. the android app)


Enjoy!


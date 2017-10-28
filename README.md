# get-tacos
A program designed to optimize Taco Bell orders. Finds the cheapest possible way to get a product by doing substitutions on cheaper products. Also checks to see if making an item "Fresco" or "Supreme" will save money.

How to use:
You'll need python >= 2.7 and pip. If you don't have them go to their website and follow the listed install instructions.

Use pip to install selenium in a command line:
sudo pip install selenium

Chrome driver kept failing on me so I'm using firefox instead. Get the geckodriver file for your platform: https://github.com/mozilla/geckodriver/releases

put a copy of the geckodriver somewhere in your PATH variable:
sudo cp geckodriver /usr/bin

Run the script:
sudo python get-tacos.py


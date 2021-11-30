# Memory Allocation
Arduino + Raspberry Pi to provide a visual representation for different methods of memory allocation

Group Members: Joshua, Shangli, Neython, Jordan, David

__Note that this code is meant to run on a Raspberry Pi 4 working with an Arduino Mega, which has Standard Firmata flashed to it. There is an option to work without these devices, but it is not the optimal method__
## Premise
For this project, we decided to continue our use of the Arduino and Raspberry Pi devices, and this time wanted to program the memory allocation algorithms from the zyBooks chapter 6.

## Memory Allocation
There are a number of different methods that free memory can be allocated. For the purposes of this project, we focused solely on allocation, using four separate methods:
  1.) First-Fit - Memory is allocated in the first 'hole' in memory that has enough space
  2.) Next-Fit - Rather than start over at the beginning of the memory 'array', a pointer is kept to the last location allocated in memory, and the first hole large enough after will be occupied.
  3.) Best-Fit - Rather than immediately storing memory in the first location, this method will search the entire memory 'array' for the best fit possible, ideally equal to the size of memory allocated.
  4.) Worst-Fit - Similar to best-fit, but instead of the best fit possible, the worst-fit is used, usually the largest hole available.
  
Each of the above methods have their own trade-offs: both first-fit and next-fit are in theory quicker, as they do not have to search the entire array. However, best-fit tries to fill smalelr holes that otherwise might remain unfilled, and worst-fit tries to eliminate the creation of such small holes altogether, which are useful properties but come at the cost of lost efficiency.

This is also only one part of memory allocation, we have not implemented solutions for when we run out of memory, which are also very important to the operating syste.
## Code
In this repository, there is a single file which contains all four algorithms. Upon running this file, it will ask whether or not a raspberry pi and arduino are are being used, and then prompt the user with a selection of the 4 algorithms, as well as other options.
## Why Python?
Arduino provides an IDE that allows for code to be written in C++; however, given that this particular program benefits from the use of input, we decided to continue with Python and using the Raspberry Pi. Rather than run the entire algorithm on the device, the Arduino only handles the turning on and off of the LEDs, while the Raspberry Pi takes care of the rest of the algorithm. This is accomplished using Firmata, an intermediate protocol that connects an embedded system to a host computer. Ideally, we would prefer to have direct input on the Arduino board with buttons or dials, but we have not found a satisfactory solution for this at the present time, so we continue using the Python console for input instead.

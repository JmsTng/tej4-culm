# NetPi Battleship
NetPi Battleship (NPB) is a cross-platform, wireless, terminal user interface (TUI) implementation of Battleship you can play between two computers, though it was originally designed with Raspberry Pi hardware in mind.

## Quickstart
To get started, install Python then clone the repository and run `pip install dependencies.txt`. If an error is returned, try `pip install dependencies.txt --break-system-packages`. This will need to be done on both devices.
To start the TUI, navigate to a terminal client of your choice and run `main.py`. You will be prompted to choose whether to be the host or client of the game. A game happens between one host and one client. Once chosen, the game will prompt you to place your ships by first specifying a point, and then using the arrow keys to define a direction. There are 5 ships:
* Carrier - 5 units long
* Battleship - 4 units long
* Cruiser - 3 units long
* Submarine - 3 units long
* Destroyer - 2 units long
After placing your ships, the host computer will output a public and private IP address that the host can use to connect to. The public address should be used when playing between different LANs; conversely, the private address is used when two devices are playing from the same LAN.
Finally, the game begins and play continues until a device disconnects or a player wins.
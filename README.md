# MTserver

Simple server to streamline the proccess of getting prices and sending orders.

Can be deployed on a linux cloud using Wine 10.0, following these simple steps:

```
sudo dpkg --add-architecture i386
sudo apt update
sudo apt upgrade -y
sudo apt install wine wine32 wine64 winetricks -y
sudo apt install xvfb x11vnc -y

Xvfb :1 -screen 0 1024x768x16 &
export DISPLAY=:1
```

To control the installation proccess, of both metatrader and python:

```
x11vnc -storepasswd
x11vnc -display :1 -rfbport 5901 -forever -shared -geometry 1024x768
```

On the client side: install `tigervnc` and connect to the server
```
vncviewer SERVER_IP:5901
```

After installing metatrader5 as per the [official documentation](https://www.mql5.com/en/articles/625), a folder `.mt5`
will be created with the wine enviroment that will run the metatrader.


To install python: `WINEPREFIX=~/.mt5 winetricks vcrun2015` and download a 64-bit version of [python for windows](https://www.python.org/downloads/windows/)
(this code was tested on python 3.12.9) and install it and the dependencies:
```
WINEPREFIX=~/.mt5 wine python-{version}-amd64.exe
WINEPREFIX=~/.mt5 wine pip install fastapi \
                                   uvicorn \
                                   python-multipart \
                                   pandas \
                                   requests \
                                   numpy \
                                   MetaTrader5\
                                   python-dotenv
```

Finally, simply run:

```
WINEPREFIX=~/.mt5 wine uvicorn main:app
```

## Example

To get a price:

```
curl -X GET "http://localhost:8000/tick/AAPL" \
     -H "x-api-key: YOUR_API_KEY"
```

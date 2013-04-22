usb-shootr
==========

# USB missile shooter

- rocket.py - controlling the usb 
- shootr - control with arrow keys


## Using

- https://github.com/walac/pyusb.git
- Tkinter - http://etutorials.org/Programming/Python+tutorial/Part+III+Python+Library+and+Extension+Modules/Chapter+16.+Tkinter+GUIs/16.9+Tkinter+Events/

## Based on 

- Retaliation - http://itr8r.tumblr.com/post/31840231144/raspberry-pi-retaliation

## Usage

- move right for 50ms: 

```
sudo python rocket.py right 50
```

- move right for 50ms then sleep 200, up 200 then left 100: 

```
sudo python rocket.py right 50 sleep 200 up 200 left 100
```


- control with arrow keys: 
```
sudo python shootr.py
```

## Install

```
wget https://github.com/walac/pyusb/archive/master.zip -o pyusb.zip
unzip pyusb.zip -d pyusb
cd pyusb
sudo python setup.py install
```

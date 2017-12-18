Everything is still Work in Progress :)

# EasyIMSI


Python wrapped RTL_SDR based GSM sniffer that uses a software defined radio to sniff gsm traffic and print out a list of IMSI’s in the area, a list of local cell towers or other features as I think of them. 

This project is more of a proof of concept than anything too solid. I started learning python/programming not long ago and wanted something to work on. 

#### Requirements:
- Python 2.7 (Should be converting to 3.x fairly soon)
- gnuradio – www.gnuradio.org
- gr-gsm - https://github.com/ptrkrysik/gr-gsm/tree/master/include/grgsm
- kalibrate-rtl - https://github.com/steve-m/kalibrate-rtl
- RTL_SDR device. Can be bought for as little as £10 from amazon, I’ve tested this with RTL2838 DVB-T based and e4000 based software defined radios
- Something to run it all on – I’ve had this working on Ubuntu / Kali Linux VM’s as well Kali directly installed on Linx 1010b tablet. While I’ve managed to get most of this working with a raspberry pi 3, I haven’t had it successfully running yet and some troubleshooting is still needed.

##### Installation – Method 1, Pybombs
I’ve had some success with this method, but it does sometimes throw up some errors and it is really not suitable for low power systems such as the raspberry pi. 

> sudo apt-get install git python-pip  

> sudo pip install PyBOMBS  

> sudo pybombs prefix init /usr/local -a default_prx  

> sudo pybombs config default_prefix default_prx  

> sudo pybombs recipes add gr-recipes git+https://github.com/gnuradio/gr-recipes.git  

> sudo pybombs recipes add gr-etcetera git+https://github.com/gnuradio/gr-etcetera.git  


During the next step, errors may be received depending on which versions of the software are being installed. I’ve added solutions below to some of the errors I’ve encountered. Others may take some troubleshooting on your end but I’ve found manually installing the software that caused the error then running pybombs again usually fixes things.

>sudo pybombs install gr-gsm  

>sudo ldconfig



#### Apache-thrift error fix
First install libssl1.0-dev
>apt-get install libssl1.0-dev

next navigate to /usr/local/src/apche-thrift/lib/cpp/src/thrift/transport/TSSLSocket.cpp  

open this file with a text editor  

search for SSLv3 and change the second occurrence to SSLv23  

 e.g. "...**SSLv3**_method()" becomes "...**SSLv23**_method()"

Save changes and exit  

>pybombs install gr-gsm

#### Libosmocore error fix
>apt-get install libosmocore*  

>apt-get install gnutls*  

>pybombs install gr-gsm  


To be continued…

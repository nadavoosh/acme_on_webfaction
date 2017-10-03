# Acme on Webfaction

What follows is a quick-and-dirty guide to using Let's Encrypt to manage SSL certs on Webfaction. 

## Prerequisites:
0. Install socat. Find the latest version http://www.dest-unreach.org/socat/download/, then do:
```
mkdir ~/src
cd ~/src
wget http://www.dest-unreach.org/socat/download/socat-1.7.3.2.tar.gz
tar -xf socat-1.7.3.2.tar.gz 
cd socat-1.7.3.2
./configure --prefix=$HOME
make
make install
```
1. Get your list of domains. For this example, we'll use `www.mydomain.com` and `mydomain.com`. 
2. Make sure you have a webfaction website serving those domains with an application at `/`. We'll call this application `mydomain_root`.

## Installation & First Run
1. Get Acme.sh:
```
curl https://get.acme.sh | sh
```
2. Issue a test cert for your domains
```
. acme.sh --test --issue -d mydomain.com -d www.mydomain.com -w ~/webapps/mydomain_root/`
```
3. If that worked, issue a non-test cert:
```
. acme.sh --issue -d mydomain.com -d www.mydomain.com -w ~/webapps/mydomain_root/`
```
4. Now paste the outputs of that command in your webfaction SSL cert panel:

## Auto-Renew
1. Get our python autorenew code
```
cd ~/src
git clone git@github.com:nadavoosh/acme_on_webfaction.git
cd acme_on_webfaction
```
2. Update `~/src/acme_on_webfaction/autorenew.sh` with your webfaction username and password.
3. Update `certs.py` with the correct information for each cert you need.  
4. You can test out the script by running it yourself: 
```
. ~/src/acme_cert_autorenew/autorenew.sh
```
5. Update the cronjob that acme created to run `autorenew.sh` instead, do `crontab -e` and edit the file so that you have:
```
40 0 * * * . ~/src/acme_cert_autorenew/autorenew.sh > /dev/null
```
You can verify with `crontab -l`.

## Source Material:
https://blog.rarepebble.com/https-on-webfaction/ for the bulk of the python script
https://community.webfaction.com/questions/21246/trying-to-use-lets-encrypt-using-acmesh-need-socat-tools
https://community.webfaction.com/questions/19988/using-letsencrypt

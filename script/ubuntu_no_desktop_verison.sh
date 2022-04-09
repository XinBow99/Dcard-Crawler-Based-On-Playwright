# For ubuntu without desktop version
apt-get install  xserver-xorg-core-hwe-18.04
apt-get install  xserver-xorg-video-dummy-hwe-18.04  --fix-missing
Xvfb :1 -screen 0 1920x1080x24+32 -fbdir /var/tmp &
export DISPLAY=:1

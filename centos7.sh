# This is a installation script to install full HorizonSpider
yum update
yum install yum-utils
yum groupinstall development
yum install epel-release
yum install https://centos7.iuscommunity.org/ius-release.rpm
yum install python36u
yum install python36u-pip
yum install python36u-devel
yum install nodejs
yum install npm
yum install python-pip # python2
npm i yarn -g
sudo -H pip install -U pipenv
mkdir Horizon
cd Horizon
git clone https://github.com/HelloZeroNet/ZeroNet
cd ZeroNet
pip2.7 install -r requirements.txt
cd ..
git clone https://github.com/blurHY/HorizonSpider
cd HorizonSpider
pip3.6 install -r requirements.txt
cd ..
git clone https://github.com/blurHY/HorizonPanel
cd HorizonPanel
yarn
yarn build
pipenv install
echo "Installation completed, but not configured"
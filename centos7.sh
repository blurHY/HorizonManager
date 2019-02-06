# This is a installation script to install full HorizonSpider
# Using Chinese registry to speed up downloading
echo "Installing Horizon ..."
yum update -y
yum install yum-utils -y
yum groupinstall development -y
yum install epel-release -y
yum install https://centos7.iuscommunity.org/ius-release.rpm -y
yum install python36u -y
yum install python36u-pip -y
yum install python36u-devel -y
pip3.6 install pip -U
pip3.6 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
yum install -y gcc-c++ make
curl -sL https://rpm.nodesource.com/setup_11.x | sudo -E bash -
yum install nodejs -y
yum install python-pip -y # python2
pip2.7 install --upgrade pip
pip2.7 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
npm set registry https://registry.npm.taobao.org
npm i yarn -g
yarn config set registry 'https://registry.npm.taobao.org'
sudo -H pip3.6 install -U pipenv
mkdir Horizon
cd Horizon
git clone https://github.com/HelloZeroNet/ZeroNet
cd ZeroNet
pip2.7 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
cd ..
git clone https://github.com/blurHY/HorizonSpider
cd HorizonSpider
pip3.6 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
cd ..
git clone https://github.com/blurHY/HorizonPanel
cd HorizonPanel
yarn
yarn build
pipenv install --python /usr/bin/python3.6
echo python2Path=/usr/bin/python2.7 >> /etc/environment
echo python3Path=/usr/bin/python3.6 >> /etc/environment
echo zeronetRoot=../ZeroNet >> /etc/environment
echo spiderRoot=../HorizonSpider >> /etc/environment
echo "Installation completed"
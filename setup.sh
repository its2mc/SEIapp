#This is a bash script that installs the SEI application environment--
#The installation must be installed from root with root previledges--
#The application will be run by opening the SEIapp folder and running the run.sh with sudo bash run.sh--

echo "++Sei Application installation (Will take approximately 2-3 hours to complete--grab a coffee..:) )++"
echo

echo "--updating linux env...--"
sudo apt-get update
echo

echo "--upgrading linux env...--"
sudo apt-get upgrade
echo

echo "--installing packages needed for compiling...--"
sudo apt-get install –y g    make
sudo apt-get install –y g    autoconf
sudo apt-get install –y g    automake
sudo apt-get install –y g    libtool

echo
echo "--installing mysql--"
echo "--You will be asked if you want to continue with the installation, enter y and press enter--"
echo "--A screen will appear asking you to set 'New password for the MySQL 'root' user', enter a password, then confirm it. (Do not forget it)--"
sudo apt-get install mysql-server mysql-client php5-mysql

echo
echo "--installing nodejs v0.6--"
sudo apt-get install nodejs

echo
echo "--installing nodejs v0.10-"
wget http://nodejs.org/dist/v0.10.2/node-v0.10.2.tar.gz
tar -xzf node-v0.10.2.tar.gz
cd node-v0.10.2
./configure
make
sudo make install-
cd ..

echo
echo "--installing zmq--"
wget http://Download.zeromq.org/zeromq-4.0.3.tar.gz
tar zxvf zeromq-4.0.3.tar.gz
cd zeromq-4.0.3 
./configure 
make 
make install ldconfig

echo
echo "--setting up application environment--"
cd SEIapp

echo
echo "--setting up mysql environment--"
echo "--Please input the root password you included during sql setup--"
echo "--If the sql script is successful you will see seidb in the database list at the end--"
sudo mysql -h localhost -u root -p < sqlSetup.sql

echo
echo "--setting up nodejs environment--"
cd node

echo
echo "1--installing nodejs zmq module--"
sudo npm install zmq

echo
echo "2--installing nodejs express module--"
sudo npm install express

echo
echo "3--installing nodejs ws module--"
sudo npm install ws

echo
echo "4--installing nodejs mysql module--"
sudo npm install mysql

echo
echo "5--installing nodejs squel module--"
sudo npm install squel

echo
echo "--setting up python environment--"
cd ../python

echo
echo "1--updating python pip module--"
sudo pip install pip -U

echo
echo "2--installing python cython compiler module--"
sudo pip install cython

echo
echo "3--installing python zmq module--"
sudo pip install pyzmq

echo
echo "4--installing python mysql module--"
sudo pip install pymysql
cd ../..

echo
echo "++SEI installation complete++"



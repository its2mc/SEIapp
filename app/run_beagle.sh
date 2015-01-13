#SEI app runtime
cd node
echo "Running node server."
sudo node commServer.js > output_node.txt &
cd ../python
echo "Running python server."
sudo python main_beagle.py > output_python.txt &
cd ..
echo "SEI app running"

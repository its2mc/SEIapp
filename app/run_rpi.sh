#SEI app runtime
cd node
echo "Running node server.s"
sudo node commServer.js > output_node.txt &
cd ../python
echo "Running python server"
sudo python main_rpi.py > output_python.txt &
cd ..
echo "SEI App running."

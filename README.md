# Semubot hardware audiosystem and ROS2 software integration <br/>
Author: Timur Nizamov <br/>


## ENG
Hello and welcome to the repository of SemuBot's audio system. Here are 3 folders:  <br/>
* `Measurements` leads to the Jupyter notebook `snr.ipynb` with tests for the mic-array and graphs; some test scripts and tryouts for the mic-array are also located there.
* `semubot_audio` is the package that contains the data pubslihing node `respeaker_node`, all of the instructions are located in the `README.md` file.
* `semubot_eyes` is the package that contains the subscriber node that accepts the DOA data from the `respeaker_node` and controls the eye movement of the robot's face, the setup instructions are located in the repository's `README.md` file.

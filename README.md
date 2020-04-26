# People-Counter-App
People counter app is used for monitoring the people at specific area in real time.

Some of the potential use cases of the people counter app are...
1. people counter app can be use for count how many people visited for specific time
    - In this app we can determine this by using total count and duration.
2. people counter app can also used for intrusion detection for specific time.
    - We can add a switch or define a specific time and when app detect any person during a specific time or when switch is on then app can give notification or sound an intrusion alert.
3. people counter app can use for monitoring number of people can allow to present in the monitoring area.
    - We can add a threshold of number people if when the count of detected people go above threshold then app can send a notification or sound an alert
Each of these use cases would be useful because...
- Using the people counter app we can easily monitor the specific area.
- It can be use for intrusion detection and also for allowing limited people.

## Demo video of Running the App with UI
[![demo video with ui](https://img.youtube.com/vi/7ZihwA3PDwo/0.jpg)](https://www.youtube.com/watch?v=7ZihwA3PDwo)

## Demo video of Running the App with opencv window (without UI)
[![demo video without ui](https://img.youtube.com/vi/TTmxVdDghvs/0.jpg)](https://www.youtube.com/watch?v=TTmxVdDghvs)


## Step-by-Step guide for Running the App
### Prerequisites
  - You need to install openvino successfully. <br/>
  See this [guide](https://docs.openvinotoolkit.org/latest/_docs_install_guides_installing_openvino_linux.html) for installing openvino.

### Generating IR files

#### Step 1
Download the pre-trained model from here:- http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz

#### Step 2
Extract the files:-
```
tar -xvf ssd_mobilenet_v2_coco_2018_03_29.tar.gz
```

#### Step 3
Go to the ssd_mobilenet_v2 directory and run the following command line:-
```
python /opt/intel/openvino/deployment_tools/model_optimizer/mo_tf.py --input_model frozen_inference_graph.pb --tensorflow_object_detection_api_pipeline_config pipeline.config --tensorflow_use_custom_operations_config /opt/intel/openvino/deployment_tools/model_optimizer/extensions/front/tf/ssd_v2_support.json --reverse_input_channel
```

#### Step 4
Create model directory in the app directory and move the generated .xml and .bin file into created model directory.

### Running the app

#### Running the app in opencv Window (Without ui)
Open the new terminal and run following commad:
```
cd <app dir>
python main_cv.py -i resources/Pedestrian_Detect_2_1_1.mp4 -m model/frozen_inference_graph.xml -l /opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/libcpu_extension_sse4.so -d CPU -pt 0.6

```

#### Running the app in ui

#### Prerequisites

  ##### Install Nodejs and its depedencies

- This step is only required if the user previously used Chris Lea's Node.js PPA.

	```
	sudo add-apt-repository -y -r ppa:chris-lea/node.js
	sudo rm -f /etc/apt/sources.list.d/chris-lea-node_js-*.list
	sudo rm -f /etc/apt/sources.list.d/chris-lea-node_js-*.list.save
	```
- To install Nodejs and Npm, run the below commands:
	```
	curl -sSL https://deb.nodesource.com/gpgkey/nodesource.gpg.key | sudo apt-key add -
	VERSION=node_6.x
	DISTRO="$(lsb_release -s -c)"
	echo "deb https://deb.nodesource.com/$VERSION $DISTRO main" | sudo tee /etc/apt/sources.list.d/nodesource.list
	echo "deb-src https://deb.nodesource.com/$VERSION $DISTRO main" | sudo tee -a /etc/apt/sources.list.d/nodesource.list
	sudo apt-get update
	sudo apt-get install nodejs
	```

##### Install the following dependencies

```
sudo apt update
sudo apt-get install python3-pip
pip3 install numpy
pip3 install paho-mqtt
sudo apt install libzmq3-dev libkrb5-dev
sudo apt install ffmpeg
```
##### Install npm

There are three components that need to be running in separate terminals for this application to work:

-   MQTT Mosca server 
-   Node.js* Web server
-   FFmpeg server
     
* For mosca server:
   ```
   cd <app_dir>/webservice/server
   npm install
   ```

* For Web server:
  ```
  cd ../ui
  npm install
  ```
  **Note:** If any configuration errors occur in mosca server or Web server while using **npm install**, use the below commands:
   ```
   sudo npm install npm -g 
   rm -rf node_modules
   npm cache clean
   npm config set registry "http://registry.npmjs.org"
   npm install
   ```

#### Run the application

##### Step 1 - Start the Mosca server

```
cd <app_dir>/webservice/server/node-server
node ./server.js
```

You should see the following message, if successful:
```
connected to ./db/data.db
Mosca server started.
```

##### Step 2 - Start the GUI

Open new terminal and run below commands.
```
cd <app_dir>/webservice/ui
npm run dev
```

You should see the following message in the terminal.
```
webpack: Compiled successfully
```

##### Step 3 - FFmpeg Server

Open new terminal and run the below commands.
```
cd <app_dir>
sudo ffserver -f ./ffmpeg/server.conf
```

##### Step 4 - Run the Demo

Open new terminal and run the below commands.
```
source /opt/intel/openvino/bin/setupvars.sh -pyver 3.5
```

Now run following commands on same terminal.

**For running on the CPU**
```
python3 main.py -i resources/Pedestrain_Detect_2_1_1.mp4 -m model/frozen_inference_graph.xml -l /opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/libcpu_extension_sse4.so -d CPU -pt 0.6 | ffmpeg -v warning -f rawvideo -pixel_format bgr24 -video_size 768x432 -framerate 24 -i - http://localhost:8090/fac.ffm
```
To see the output on a web based interface, open the link [http://localhost:8080](http://localhost:8080/) in a browser.

**For running on the GPU**

  ```
  python3 main.py -i resources/Pedestrian_Detect_2_1_1.mp4 -m model/frozen_inference_graph.xml -d GPU -pt 0.6 | ffmpeg -v warning -f rawvideo -pixel_format bgr24 -video_size 768x432 -framerate 24 -i - http://localhost:8090/fac.ffm
  ```
  To see the output on a web based interface, open the link [http://localhost:8080](http://localhost:8080/) in a browser.<br><br>
 
##### Using Camera stream instead of video file

To get the input video from the camera, use ```-i CAM``` command-line argument. Specify the resolution of the camera using 
```-video_size``` command line argument.

For example:
```
python3 main.py -i CAM -m model/frozen_inference_graph.xml -l /opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/libcpu_extension_sse4.so -d CPU -pt 0.6 | ffmpeg -v warning -f rawvideo -pixel_format bgr24 -video_size 768x432 -framerate 24 -i - http://localhost:8090/fac.ffm
```
To see the output on a web based interface, open the link [http://localhost:8080](http://localhost:8080/) in a browser.

**Note:**
User has to give ```-video_size``` command line argument according to the input as it is used to specify the resolution of the video or image file.

##### Using image instead of video file

To get the input video from the camera, use ```-i CAM``` command-line argument. Specify the resolution of the camera using 
```-video_size``` command line argument.

For example:
```
python3 main.py -i <image_file_path> -m model/frozen_inference_graph.xml -l /opt/intel/openvino/deployment_tools/inference_engine/lib/intel64/libcpu_extension_sse4.so -d CPU -pt 0.6
```
To see the output open the **output.jpg** file in person counter app directory.

# Refrences
- https://github.com/intel-iot-devkit

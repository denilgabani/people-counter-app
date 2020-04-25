# people-counter-app
People counter app is used for monitoring the people at specific area in real time.

## step-by-step guide for converting tensorflow model to IR
### Prerequisites
  - You need to install openvino successfully. <br/>
  See this [guide](https://docs.openvinotoolkit.org/latest/_docs_install_guides_installing_openvino_linux.html) for installing openvino.

### Generating IR files

#### Step 1
Download the pre-trained model from here:- http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz

#### Step 2
Extract the files:-
`tar -xvf ssd_mobilenet_v2_coco_2018_03_29.tar.gz`

#### Step 3
Go to the ssd_mobilenet_v2 directory and run the following command line:-
`python /opt/intel/openvino/deployment_tools/model_optimizer/mo_tf.py --input_model frozen_inference_graph.pb --tensorflow_object_detection_api_pipeline_config pipeline.config --tensorflow_use_custom_operations_config /opt/intel/openvino/deployment_tools/model_optimizer/extensions/front/tf/ssd_v2_support.json --reverse_input_channel`

#### Step 4
Move the generated .xml and .bin file to model directory of the app.



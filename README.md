# people-counter-app
People counter app is used for monitoring the people at specific area in real time.

# step-by-step guide for conerting tensorflow model to IR
For the people detection pre trained model is used ssd_mobilenet_v2.

Step:-1 Download the pre-trained model from here:- http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz

step-2 Extract the files:-
`tar -xvf ssd_mobilenet_v2_coco_2018_03_29.tar.gz`

step-3 Go to the ssd_mobilenet_v2 directory and run the following command line:-
`python /opt/intel/openvino/deployment_tools/model_optimizer/mo_tf.py --input_model frozen_inference_graph.pb --tensorflow_object_detection_api_pipeline_config pipeline.config --tensorflow_use_custom_operations_config /opt/intel/openvino/deployment_tools/model_optimizer/extensions/front/tf/ssd_v2_support.json --reverse_input_channel`

step-4 move the generated .xml and .bin file to model directory of the app.

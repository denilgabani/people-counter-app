"""People Counter."""
"""
 Copyright (c) 2018 Intel Corporation.
 Permission is hereby granted, free of charge, to any person obtaining
 a copy of this software and associated documentation files (the
 "Software"), to deal in the Software without restriction, including
 without limitation the rights to use, copy, modify, merge, publish,
 distribute, sublicense, and/or sell copies of the Software, and to
 permit person to whom the Software is furnished to do so, subject to
 the following conditions:
 The above copyright notice and this permission notice shall be
 included in all copies or substantial portions of the Software.
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
 LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


import os
import time
import cv2
import numpy as np


from argparse import ArgumentParser
from inference_cv import Network

# MQTT server environment variables
LABELS = {'1': 'person', '2': 'bicycle', '3': 'car', '4': 'motorcycle', '5': 'airplane', '6': 'bus', '7': 'train', '8': 'truck', '9': 'boat', '10': 'traffic', '11': 'fire', '13': 'stop', '14': 'parking', '15': 'bench', '16': 'bird', '17': 'cat', '18': 'dog', '19': 'horse', '20': 'sheep', '21': 'cow', '22': 'elephant', '23': 'bear', '24': 'zebra', '25': 'giraffe', '27': 'backpack', '28': 'umbrella', '31': 'handbag', '32': 'tie', '33': 'suitcase', '34': 'frisbee', '35': 'skis', '36': 'snowboard', '37': 'sports', '38': 'kite', '39': 'baseball', '40': 'baseball', '41': 'skateboard', '42': 'surfboard', '43': 'tennis', '44': 'bottle', '46': 'wine', '47': 'cup', '48': 'fork', '49': 'knife', '50': 'spoon', '51': 'bowl', '52': 'banana', '53': 'apple', '54': 'sandwich', '55': 'orange', '56': 'broccoli', '57': 'carrot', '58': 'hot', '59': 'pizza', '60': 'donut', '61': 'cake', '62': 'chair', '63': 'couch', '64': 'potted', '65': 'bed', '67': 'dining', '70': 'toilet', '72': 'tv', '73': 'laptop', '74': 'mouse', '75': 'remote', '76': 'keyboard', '77': 'cell', '78': 'microwave', '79': 'oven', '80': 'toaster', '81': 'sink', '82': 'refrigerator', '84': 'book', '85': 'clock', '86': 'vase', '87': 'scissors', '88': 'teddy', '89': 'hair', '90': 'toothbrush','0':'None'}
def build_argparser():
    """
    Parse command line arguments.

    :return: command line arguments
    """
    parser = ArgumentParser()
    parser.add_argument("-m", "--model", required=True, type=str,
                        help="Path to an xml file with a trained model.")
    parser.add_argument("-i", "--input", required=True, type=str,
                        help="Path to image or video file or enter cam for webcam")
    parser.add_argument("-l", "--cpu_extension", required=False, type=str,
                        default=None,
                        help="MKLDNN (CPU)-targeted custom layers."
                             "Absolute path to a shared library with the"
                             "kernels impl.")
    parser.add_argument("-d", "--device", type=str, default="CPU",
                        help="Specify the target device to infer on: "
                             "CPU, GPU, FPGA or MYRIAD is acceptable. Sample "
                             "will look for a suitable plugin for device "
                             "specified (CPU by default)")
    parser.add_argument("-pt", "--prob_threshold", type=float, default=0.5,
                        help="Probability threshold for detections filtering"
                        "(0.5 by default)")
    return parser

def extract_box(img, output, conf_level=0.35):
    h = img.shape[0]
    w = img.shape[1]
    box = output[0,0,:,3:7] * np.array([w, h, w, h])
    box = box.astype(np.int32)
    cls = output[0,0,:,1]
    conf = output[0,0,:,2]
    count=0
    p1 = None
    p2 = None
    for i in range(len(box)):
        label = LABELS[str(int(cls[i]))]
        if (not label=='person') or conf[i]<conf_level:
            continue
        p1 = (box[i][0], box[i][1])
        p2 = (box[i][2], box[i][3])
        cv2.rectangle(img, p1, p2, (0,255,0))
        count+=1
    return img, count, (p1,p2)


def infer_on_stream(args):
    """
    Initialize the inference network, stream video to network,
    and output stats and video.

    :param args: Command line arguments parsed by `build_argparser()`
    :param client: MQTT client
    :return: None
    """
    modelPath = args.model
    deviceType = args.device
    cpuExt = args.cpu_extension
    probThresh = args.prob_threshold
    filePath = args.input
    # Initialise the class
    infer_network = Network()
    # Set Probability threshold for detections
    prob_threshold = probThresh

    ### TODO: Load the model through `infer_network` ###
    
    if filePath.lower()=="cam":
        camera = cv2.VideoCapture(0)
    elif filePath.split(".")[-1].lower() in ['jpg', 'jpeg', 'png', 'bmp']:
        infer_network.load_model(modelPath, 1, deviceType, cpuExt)
        image_input_shape = infer_network.get_input_shape()
        print(image_input_shape)
        img = cv2.imread(filePath, cv2.IMREAD_COLOR)
        resized_frame = cv2.resize(img, (image_input_shape[3], image_input_shape[2]))
        frame_preproc = np.transpose(np.expand_dims(resized_frame.copy(), axis=0), (0,3,1,2))
        infer_network.exec_net(frame_preproc)
        if infer_network.wait()==0:
            outputs = infer_network.get_output()
            box_frame, count, bbox = extract_box(img, outputs, prob_threshold)
            cv2.putText(box_frame, "Count:"+str(count), (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            cv2.imwrite('output.jpg', box_frame)
        return
    else:
        if not os.path.isfile(filePath):
            print(" Given input file is not present.")
            exit(1)
        camera = cv2.VideoCapture(filePath)
    ### TODO: Handle the input stream ###
    
    frame_width = int(camera.get(3))
    frame_height = int(camera.get(4))
    if (camera.isOpened()== False): 
        print("Error opening video stream or file")
    cur_req_id=0
    next_req_id=1
    num_requests=2
    infer_network.load_model(modelPath, num_requests, deviceType, cpuExt)
    image_input_shape = infer_network.get_input_shape()
    print(image_input_shape)
    ret, frame = camera.read()
    #output_video = cv2.VideoWriter('output.mp4',cv2.VideoWriter_fourcc(*'MPEG'), 10, (frame_width,frame_height))
    ### TODO: Loop until stream is over ###
    total_count=0
    pres_count = 0
    prev_count=0
    start_time=0 
    no_bbox=0
    duration=0
    prev_bbox_x = 0

    while camera.isOpened():
        
        ### TODO: Read from the video capture ###
        ret, next_frame = camera.read()
        if not ret:
            break
        key = cv2.waitKey(60)
        ### TODO: Pre-process the image as needed ###
        #frame_cvt = cv2.cvtColor(frame.copy(), cv2.COLOR_BGR2RGB)
        resized_frame = cv2.resize(next_frame.copy(), (image_input_shape[3], image_input_shape[2]))
    
        frame_preproc = np.transpose(np.expand_dims(resized_frame.copy(), axis=0), (0,3,1,2))
        ### TODO: Start asynchronous inference for specified request ###
        infer_network.exec_net(frame_preproc.copy(), req_id=next_req_id)
        ### TODO: Wait for the result ###
        if infer_network.wait(cur_req_id)==0:
            ### TODO: Get the results of the inference request ###
            outputs = infer_network.get_output(cur_req_id)
            ### TODO: Extract any desired stats from the results ###
            frame, pres_count, bbox = extract_box(frame.copy(), outputs[0], prob_threshold)
            box_h = frame.shape[0]
            box_w = frame.shape[1]
            tl, br = bbox #top_left, bottom_right
        
            if pres_count>prev_count:
                start_time = time.time()
                no_bbox=0
            elif pres_count<prev_count:
                if no_bbox<=20:
                    pres_count=prev_count
                    no_bbox+=1
                elif prev_bbox_x<box_w-200:
                    pres_count=prev_count
                    no_bbox=0
                else:
                    total_count+=1
                    duration = int(time.time()-start_time)                    
            
            if not (tl==None and br==None):
                prev_bbox_x=int((tl[0]+br[0])/2)
            
            prev_count=pres_count
            #output_video.write(frame)
            
            ### TODO: Calculate and send relevant information on ###
            ### current_count, total_count and duration to the MQTT server ###
            ### Topic "person": keys of "count" and "total" ###
            ### Topic "person/duration": key of "duration" ###
            offset = int(box_h/10)
    
            cv2.putText(frame, "Count:"+str(pres_count), (20, offset), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            cv2.putText(frame, "Duration:"+str(duration), (20, offset+30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            cv2.putText(frame, "total_count:"+str(total_count), (20, offset+60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        cv2.imshow("people counter",frame)
        
        
        ### TODO: Send the frame to the FFMPEG server ###
        ### TODO: Write an output image if `single_image_mode` ###
        cur_req_id, next_req_id = next_req_id, cur_req_id
        frame = next_frame
        if key==27:
            break
    #output_video.release()
    camera.release()

def main():
    """
    Load the network and parse the output.

    :return: None
    """
    # Grab command line args
    args = build_argparser().parse_args()
    # Connect to the MQTT server
    # Perform inference on the input stream
    infer_on_stream(args)


if __name__ == '__main__':
    main()

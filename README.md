# MSc-Project

## Toolbox:
- Using all the functions in the toolbox.
- All videos used for detection are stored in a single folder.
```bash
python main.py --mode all --source_video_path 'your_folder'
```
### 1. Pedestrian Analysis
#### (0) Weights for Pedestrian Detection (Optional)
https://github.com/EdgeGalaxy/YoloPedestrian
#### (1) Count the number of pedestrians in the zone (Done)
```bash
python main.py --mode count --source_video_path 'your_video'
```
https://github.com/roboflow/supervision/tree/develop/examples/count_people_in_zone
#### (2) Pedestrian Speed Estimator (Done)
```bash
python main.py --mode speed_pede --source_video_path 'your_video'
```    
https://supervision.roboflow.com/develop/how_to/track_objects/#keypoint-tracking
#### (3) Waiting time in the zone (Done)
```bash
python main.py --mode Waiting --source_video_path 'your_video'
```  
https://github.com/roboflow/supervision/tree/develop/examples/time_in_zone
#### (4) Pedestrian tracking (Done)
```bash
python main.py --mode tracking_pede --source_video_path 'your_video'
```    
https://supervision.roboflow.com/develop/how_to/track_objects/#keypoint-tracking
#### (5) Phone usage detection (Done)
```bash
python main.py --mode phone --source_video_path 'your_video'
```  
https://github.com/HasnainAhmedO7/Detection-of-Phone-Usage-with-Computer-Vision
#### (6) Age (Done)
```bash
python main.py --mode face --source_video_path 'your_video'
```
https://github.com/serengil/deepface
#### (7) Gender (Done)
```bash
python main.py --mode gender --source_video_path 'your_video'
```
https://github.com/Sklyvan/Age-Gender-Prediction
#### (8) Race (Done)
```bash
python main.py --mode face --source_video_path 'your_video'
```
https://github.com/serengil/deepface
#### (9) Clothing type analysis (Done)
```bash
python main.py --mode clothing --source_video_path 'your_video'
```
https://github.com/ZerrnArsk/Fashion-Based-Person-Searcher
#### (10) Personal belongings (Done)
```bash
python main.py --mode belongings --source_video_path 'your_video'
```
### 2. Vehicle Analysis 
#### (1) Vehicle Type (Done)
```bash
python main.py --mode vehicle_type --source_video_path 'your_video'
```  
https://github.com/Srilakshmi2717/YOLO-Based-Real-Time-Vehicle-Detection-and-Classification
#### (2) Vehicle Speed (Done)
```bash
python main.py --mode speed --source_video_path 'your_video'
```  
https://github.com/WZS666/Yolov5_DeepSort_SpeedEstimate
#### (3) Distance between vehicles and vehicles (Done)
```bash
python main.py --mode car_distance --source_video_path 'your_video'
```  
https://github.com/maheshpaulj/Lane_Detection
#### (4) Distance between vehicles and pedestrians (Done)
```bash
python main.py --mode pede_distance --source_video_path 'your_video'
```  
https://github.com/maheshpaulj/Lane_Detection
#### (5) Lane Detection (Done)
```bash
python main.py --mode lane --source_video_path 'your_video'
```  
https://github.com/maheshpaulj/Lane_Detection
### 3. Environment Analysis 
#### (1) Weather (Done)
```bash
python main.py --mode weather --source_video_path 'your_video'
```  
https://github.com/nurcanyaz/yolov8WeatherClassification
#### (2) Traffic light (Done)
```bash
python main.py --mode light --source_video_path pedestrian.mp4
```  
https://github.com/alasarerhan/Real-Time-Traffic-Light-and-Sign-Detection-with-YOLO11
#### (3) Traffic sign (Done)
```bash
python main.py --mode traffic_sign --source_video_path 'your_video'
```
https://github.com/MDhamani/Traffic-Sign-Recognition-Using-YOLO
https://github.com/KL-lovesagiri/YOLOv8_GUI_For_Traffic_Sign_Detection
https://github.com/Kartik-Aggarwal/Real-Time-Traffic-Sign-Detection
#### (4) Road Condition (Done)
```bash
python main.py --mode road_defect --source_video_path 'your_video'
```
https://github.com/oracl4/RoadDamageDetection
#### (5) Road Width (Done)
```bash
python main.py --mode width --source_video_path 'your_video'
```
https://github.com/saarthxxk/Real-Time-Road-Width-Detection
#### (6) Day or Evening (Done)
```bash
python main.py --mode daytime --source_video_path 'your_video'
```
https://github.com/KishieKube/CV_Day_Evening_detector
#### (7) Crosswalk (Done)
```bash
python main.py --mode crosswalk --source_video_path 'your_video'
```
https://github.com/xN1ckuz/Crosswalks-Detection-using-YOLO
#### (8) Accident (Done)
```bash
python main.py --mode accident --source_video_path 'your_video'
```
https://github.com/RoadEyeProject/RoadEye_model
#### (9) Sidewalk (Done)
```bash
python main.py --mode sidewalk --source_video_path 'your_video'
```
https://github.com/shaikhubaidahmed/Vehicle_Collision_Detection  
Weights should be downloaded from https://drive.usercontent.google.com/download?id=1X1uKaGENEBZamF6tOfx9eKLTIQLsBN5h&export=download&authuser=0

### 4. Combination Analysis 
#### (1) Risky crossing analysis (Done)
```bash
python main.py --mode risky --source_video_path 'your_video'
```
This function is used to detect whether pedestrians cross the street in a risky way based on the detection of the traffic light, the traffic sign, and the crosswalk
#### (2) Trend in pedestrians speed when crossing (Done)
```bash
python main.py --mode acc --source_video_path 'your_video'
```
This function is used to analyze whether pedestrians accelerate, move at a constant speed, or decelerate while crossing the street.
#### (3) Determine whether a pedestrian has crossed the road (Done)
```bash
python main.py --mode cross_pede --source_video_path 'your_video'
```
This function is used to Determine and record whether each pedestrian in the video has crossed the road.
#### (4) Determine whether a pedestrian has used the crosswalk when crossing (Done)
```bash
python main.py --mode crosswalk_usage --source_video_path 'your_video'
```
This function is used to analyse whether a pedestrian use the crosswalk or not besed on the fact that he/she has crossed the street.
#### (5) Detect red light runner
```bash
python main.py --mode red_run --source_video_path 'your_video'
```
This function is used to analyse whether a pedestrian run the red light or not besed on the fact that he/she has crossed the street.
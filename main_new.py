import argparse
# 0
from track_id_pedestrians import run_pedestrian_tracking
# 1.1
# from modules.count_pedestrians.count_pedestrians import count_pedestrians
# 1.2
from modules.speed_pedestrian.speed_pedestrian import run_pede_speed_estimation
# 1.3
from modules.waiting_time_pede.waiting_time_pede import run_waiting_time_analysis
# 1.4
from modules.tracking_pede.tracking_pede import run_pede_direction_analysis
# 1.5
from modules.phone.phone import run_phone_detection
# 1.6 ~ 1.8
from modules.face.face import run_face_analysis
# 1.9
from modules.clothing.clothing import run_clothing_detection
# 1.10
from modules.belongings.belongings import run_belongings_detection
# 2.1
from modules.type_vehicle.type_vehicle import run_vehicle_frame_analysis
# 2.2
from modules.type_vehicle.type_vehicle import run_vehicle_frame_analysis
# 2.3
from modules.distance_vehicle.distance_vehicle import run_car_detection_with_distance
# 2.4
from modules.distance_pedestrian.distance_pedestrian import visualize_and_estimate_distance
# 2.5
from modules.lane_detection.lane_detection import run_lane_detection
# 3.1
from modules.weather.weather import run_weather_detection
# 3.2
from modules.traffic_light.traffic_light import run_traffic_light_detection
# 3.3.1
from modules.traffic_sign.traffic_sign_euro import run_traffic_sign_euro
# 3.3.2
from modules.traffic_sign.traffic_sign_asia import run_traffic_sign_asia
# 3.4
from modules.road_condition.road_condition import run_road_defect_detection
# 3.5
from modules.road_width.road_width import run_road_width_analysis
# 3.6
from modules.daynight.daytime import run_daytime_detection
# 3.7
from modules.crosswalk.crosswalk import run_crosswalk_detection

import subprocess
import os




def main():
    def run_mode(mode, video_path, extra_args=""):
        cmd = f"python main.py --mode {mode} --source_video_path \"{video_path}\" {extra_args}"
        print(f"Running: {cmd}")
        subprocess.run(cmd, shell=True)
    parser = argparse.ArgumentParser(description="Pedestrian Analysis Toolbox")
    parser.add_argument(
        "--mode",
        type=str,
        required=True,
        choices=["id", "count", "waiting", "car_distance", "tracking_pede", "type", "lane", "width", "speed_pede","traffic", "traffic_sign", "defect", "agegender", "belongings", "weather", "phone", "clothing", "face", "total", "light", "head", "daytime", "crosswalk","all"],
        help="Choose the analysis mode: 'count', 'waiting', 'tracking', 'type', 'traffic', or 'agegender'",
    )
    parser.add_argument(
        "--source_video_path",
        required=True,
        type=str,
        help="Path to the source video file",
    )
    parser.add_argument(
        "--weights_yolo",
        type=str,
        default="yolov8n.pt",
        help="Weights file for tracking mode",
    )

    args = parser.parse_args()

    if args.mode == "count":
        count_pedestrians(
            source_video_path=args.source_video_path,
            zone_configuration_path=args.zone_configuration_path,
            source_weights_path=args.source_weights_path,
            target_video_path=args.target_video_path,
            confidence_threshold=args.confidence_threshold,
            iou_threshold=args.iou_threshold,
        )
    elif args.mode == "id":
        run_pedestrian_tracking(
            video_path=args.source_video_path,
        )
    elif args.mode == "waiting":
        run_waiting_time_analysis(
            video_path=args.source_video_path,
        )
    elif args.mode == "tracking_pede":
        run_pede_direction_analysis(
            video_path=args.source_video_path,
        )
    elif args.mode == "speed_pede":
        run_pede_speed_estimation(
            video_path=args.source_video_path,
        )
    elif args.mode == "traffic_sign":
        run_traffic_sign_asia(
            video_path=args.source_video_path,
        )
        # run_traffic_sign_euro(
        #     video_path=args.source_video_path,
        # )
    elif args.mode == "weather":
        run_weather_detection(
            video_path=args.source_video_path
        )
    elif args.mode == "clothing":
        run_clothing_detection(
            video_path=args.source_video_path
        )
    elif args.mode == "face":
        run_face_analysis(video_path=args.source_video_path)
    elif args.mode == "light":
        run_traffic_light_detection(
            video_path=args.source_video_path,
        )
    elif args.mode == "defect":
        run_road_defect_detection(
            video_path=args.source_video_path
        )
    elif args.mode == "width":
        run_road_width_analysis(
            video_path=args.source_video_path
        )
    elif args.mode == "car_distance":
        run_car_detection_with_distance(
            video_path=args.source_video_path
        )
    elif args.mode == "lane":
        run_lane_detection(
            video_path=args.source_video_path
        )
    elif args.mode == "phone":
        run_phone_detection(
            video_path=args.source_video_path,
            weights=args.weights_yolo
        )
    elif args.mode == "belongings":
        run_belongings_detection(
            video_path=args.source_video_path,
            weights=args.weights_yolo
        )
    elif args.mode == "daytime":
        run_daytime_detection(
            video_path=args.source_video_path
        )
    elif args.mode == "crosswalk":
        run_crosswalk_detection(
            video_path=args.source_video_path,
        )
    elif args.mode == "all":
        video_dir = args.source_video_path
        if not os.path.isdir(video_dir):
            print(f"Error: {video_dir} is not a valid directory.")
            return

        video_files = [f for f in os.listdir(video_dir) if f.lower().endswith((".mp4", ".avi", ".mov", ".mkv"))]

        for video_file in video_files:
            video_path = os.path.join(video_dir, video_file)

            run_mode("count", video_path)
            run_mode("waiting", video_path)
            run_mode("tracking_pede", video_path)
            run_mode("speed_pede",video_path)
            run_mode("clothing", video_path)
            run_mode("phone", video_path)
            run_mode("belongings", video_path)
            run_mode("face", video_path)
            run_mode("weather", video_path)
            run_mode("traffic_sign", video_path)
    else:
        print(f"Unknown mode: {args.mode}")


if __name__ == "__main__":
    main()

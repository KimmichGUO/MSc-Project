import os
import cv2
import pandas as pd
from collections import defaultdict

def pedestrian_count(video_path, tracking_csv_path=None, output_csv_path=None):
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    if tracking_csv_path is None:
        tracking_csv_path = os.path.join("analysis_results", video_name, "[B1]tracked_pedestrians.csv")
    if output_csv_path is None:
        output_dir = os.path.join("analysis_results", video_name)
        os.makedirs(output_dir, exist_ok=True)
        output_csv_path = os.path.join(output_dir, "[P1]pedestrian_count.csv")

    cap = cv2.VideoCapture(video_path)
    frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    cap.release()
    center_line = frame_width / 2

    df = pd.read_csv(tracking_csv_path)

    frame_data = defaultdict(list)
    for _, row in df.iterrows():
        frame_id = int(row["frame_id"])
        x1, x2 = row["x1"], row["x2"]
        cx = (x1 + x2) / 2
        frame_data[frame_id].append(cx)

    results = []
    for frame_id in sorted(frame_data.keys()):
        cxs = frame_data[frame_id]
        left_count = sum(1 for cx in cxs if cx < center_line)
        right_count = sum(1 for cx in cxs if cx >= center_line)
        results.append({
            "frame_id": frame_id,
            "left_count": left_count,
            "right_count": right_count
        })

    results_df = pd.DataFrame(results)
    results_df.to_csv(output_csv_path, index=False)

    print(f"\nPedestrian_count completed. Result saved to {output_csv_path}")


# import json
# from typing import List, Tuple
# import cv2
# import numpy as np
# from tqdm import tqdm
# import os
# import csv
# from ultralytics import YOLO
# import supervision as sv

# COLORS = sv.ColorPalette.DEFAULT

# def load_zones_config(file_path: str) -> List[np.ndarray]:
#     with open(file_path, "r") as file:
#         data = json.load(file)
#         return [np.array(polygon, np.int32) for polygon in data["polygons"]]

# def initiate_annotators(polygons: List[np.ndarray], resolution_wh: Tuple[int, int]):
#     line_thickness = sv.calculate_optimal_line_thickness(resolution_wh=resolution_wh)
#     text_scale = sv.calculate_optimal_text_scale(resolution_wh=resolution_wh)

#     zones, zone_annotators, box_annotators = [], [], []
#     for index, polygon in enumerate(polygons):
#         zone = sv.PolygonZone(polygon=polygon)
#         zone_annotator = sv.PolygonZoneAnnotator(
#             zone=zone,
#             color=COLORS.by_idx(index),
#             thickness=line_thickness,
#             text_thickness=line_thickness * 2,
#             text_scale=text_scale * 2,
#         )
#         box_annotator = sv.BoxAnnotator(
#             color=COLORS.by_idx(index), thickness=line_thickness
#         )
#         zones.append(zone)
#         zone_annotators.append(zone_annotator)
#         box_annotators.append(box_annotator)

#     return zones, zone_annotators, box_annotators

# def detect(frame: np.ndarray, model: YOLO, confidence_threshold: float = 0.5):
#     results = model(frame, imgsz=1280, verbose=False)[0]
#     detections = sv.Detections.from_ultralytics(results)
#     filter_by_class = detections.class_id == 0
#     filter_by_confidence = detections.confidence > confidence_threshold
#     return detections[filter_by_class & filter_by_confidence]

# def annotate(frame, zones, zone_annotators, box_annotators, detections):
#     annotated_frame = frame.copy()
#     counts = []
#     for zone, zone_annotator, box_annotator in zip(zones, zone_annotators, box_annotators):
#         detections_in_zone = detections[zone.trigger(detections=detections)]
#         count = len(detections_in_zone)
#         counts.append(count)
#         annotated_frame = zone_annotator.annotate(scene=annotated_frame)
#         annotated_frame = box_annotator.annotate(
#             scene=annotated_frame, detections=detections_in_zone
#         )
#     return annotated_frame, counts


# def count_pedestrians(
#     source_video_path: str,
#     zone_configuration_path: str,
#     source_weights_path: str = "yolov8n.pt",
#     target_video_path: str = None,
#     confidence_threshold: float = 0.3,
#     iou_threshold: float = 0.7,
#     save_interval_frames: int = 30
# ):
    
#     # base_name = os.path.splitext(os.path.basename(source_video_path))[0]
#     # csv_output_path = f"{base_name}_count_pedestrian.csv"
#     base_name = os.path.splitext(os.path.basename(source_video_path))[0]
#     output_dir = os.path.join("analysis_results", base_name)
#     os.makedirs(output_dir, exist_ok=True)
#     csv_output_path = os.path.join(output_dir, f"{base_name}_pedestrian_speed.csv")
    
#     with open(csv_output_path, mode='w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(["frame", "data"])

#     video_info = sv.VideoInfo.from_video_path(source_video_path)
#     polygons = load_zones_config(zone_configuration_path)
#     zones, zone_annotators, box_annotators = initiate_annotators(
#         polygons=polygons, resolution_wh=video_info.resolution_wh
#     )

#     model = YOLO(source_weights_path)
#     frames_generator = sv.get_video_frames_generator(source_video_path)

#     frame_count = 0

#     if target_video_path is not None:
#         with sv.VideoSink(target_video_path, video_info) as sink:
#             for frame in tqdm(frames_generator, total=video_info.total_frames):
#                 frame_count += 1
#                 detections = detect(frame, model, confidence_threshold)
#                 annotated_frame, counts = annotate(frame, zones, zone_annotators, box_annotators, detections)

#                 if frame_count % save_interval_frames == 0:
#                     count_dict = {i: count for i, count in enumerate(counts)}
#                     with open(csv_output_path, mode='a', newline='') as f:
#                         writer = csv.writer(f)
#                         writer.writerow([frame_count, str(count_dict)])

#                 sink.write_frame(annotated_frame)
#     else:
#         for frame in tqdm(frames_generator, total=video_info.total_frames):
#             frame_count += 1
#             detections = detect(frame, model, confidence_threshold)
#             annotated_frame, counts = annotate(frame, zones, zone_annotators, box_annotators, detections)

#             for i, count in enumerate(counts):
#                 position = (30, 50 + i * 40)
#                 text = f"Zone {i + 1} Count: {count}"
#                 cv2.putText(
#                     annotated_frame, text, position,
#                     fontFace=cv2.FONT_HERSHEY_SIMPLEX,
#                     fontScale=1,
#                     color=(0, 255, 0),
#                     thickness=2
#                 )

#             if frame_count % save_interval_frames == 0:
#                 count_dict = {i: count for i, count in enumerate(counts)}
#                 with open(csv_output_path, mode='a', newline='') as f:
#                     writer = csv.writer(f)
#                     writer.writerow([frame_count, str(count_dict)])

#             print(f"Frame {frame_count}: Zone counts = {counts}")
#             cv2.imshow("Processed Video", annotated_frame)
#             if cv2.waitKey(1) & 0xFF == ord("q"):
#                 break
#         cv2.destroyAllWindows()

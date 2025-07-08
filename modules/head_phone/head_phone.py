def run_head_detection(source_video_path):
    import cv2
    import mediapipe as mp
    import numpy as np
    import time
    import os
    import csv
    from ultralytics import YOLO
    from ultralytics.utils.plotting import Annotator

    model = YOLO("yolov8n.pt")
    names = model.names

    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    cap = cv2.VideoCapture(source_video_path)
    if not cap.isOpened():
        print("Error opening video file")
        exit()

    frame_index = 0
    csv_filename = os.path.splitext(os.path.basename(source_video_path))[0] + "_head_phone.csv"

    with open(csv_filename, mode="w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["frame", "look_down_count", "phone_count"])

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        frame_index += 1
        look_down_count = 0
        phone_count = 0
        person_count = 0

        start = time.time()

        image_rgb = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        img_h, img_w, _ = image.shape

        results = model.predict(image, show=False)
        boxes = results[0].boxes.xyxy.cpu().numpy()
        clss = results[0].boxes.cls.cpu().numpy().astype(int)

        annotator = Annotator(image, line_width=3, example=names)

        for box, cls in zip(boxes, clss):
            if names[cls] == "person":
                person_count += 1
                x1, y1, x2, y2 = map(int, box)
                person_roi = image_rgb[y1:y2, x1:x2]
                if person_roi.size == 0:
                    continue

                face_results = face_mesh.process(person_roi)
                text = "No Face"

                if face_results.multi_face_landmarks:
                    face_landmarks = face_results.multi_face_landmarks[0]

                    roi_h, roi_w, _ = person_roi.shape
                    face_3d = []
                    face_2d = []
                    nose_2d = None
                    nose_3d = None

                    for idx, lm in enumerate(face_landmarks.landmark):
                        if idx in [33, 263, 1, 61, 291, 199]:
                            x = int(lm.x * roi_w)
                            y = int(lm.y * roi_h)

                            face_2d.append([x, y])
                            face_3d.append([x, y, lm.z])

                            if idx == 1:
                                nose_2d = (x, y)
                                nose_3d = (x, y, lm.z * 3000)

                    if len(face_2d) == 6 and nose_2d and nose_3d:
                        face_2d = np.array(face_2d, dtype=np.float64)
                        face_3d = np.array(face_3d, dtype=np.float64)

                        focal_length = 1 * roi_w
                        cam_matrix = np.array([[focal_length, 0, roi_w / 2],
                                               [0, focal_length, roi_h / 2],
                                               [0, 0, 1]])
                        dist_matrix = np.zeros((4, 1), dtype=np.float64)

                        success_pnp, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

                        if success_pnp:
                            rmat, _ = cv2.Rodrigues(rot_vec)
                            angles, _, _, _, _, _ = cv2.RQDecomp3x3(rmat)

                            x_angle = angles[0] * 360
                            y_angle = angles[1] * 360
                            z_angle = angles[2] * 360

                            if x_angle < -10:
                                text = "Looking Down"
                                look_down_count += 1
                            elif y_angle < -10:
                                text = "Looking Left"
                            elif y_angle > 10:
                                text = "Looking Right"
                            elif x_angle > 10:
                                text = "Looking Up"
                            else:
                                text = "Forward"

                annotator.box_label(box, label=f"Person: {text}")

            elif names[cls] == 'cell phone':
                phone_count += 1
                annotator.box_label(box, label='Cell Phone')

        image = annotator.result()
        
        if frame_index % 30 == 0:
            if person_count > 0:
                lookdown_ratio = f"{look_down_count}/{person_count}"
                phone_ratio = f"{phone_count}/{person_count}"
            else:
                lookdown_ratio = "0/0"
                phone_ratio = "0/0"

            with open(csv_filename, mode="a", newline="") as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([frame_index, lookdown_ratio, phone_ratio])

        end = time.time()
        fps = 1 / (end - start)
        cv2.putText(image, f'FPS: {int(fps)}', (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 2)

        cv2.imshow('Activity', image)

        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

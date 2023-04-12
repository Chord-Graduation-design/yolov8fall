
import cv2
import cv2.dnn;
import numpy as np

CLASSES = ["fall","person"]
COLORS = []
def draw_bounding_box(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
    label = f'{CLASSES[class_id]} ({confidence:.2f})'
    # color = colors[class_id]
    color = (0, 0, 255)

    cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 1)
    cv2.putText(img, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
def detect(model:cv2.dnn.Net,source:np.ndarray):
    # [height, width, _] = source.shape
    # length = max((height, width))
    # image = np.zeros((length, length, 3), np.uint8)
    # image[0:height, 0:width] = source
    # scale = length / 640
    blob = cv2.dnn.blobFromImage(source, scalefactor=1 / 255, size=(640, 480))
    model.setInput(blob)
    outputs = model.forward()

    outputs = np.array([cv2.transpose(outputs[0])])
    rows = outputs.shape[1]

    boxes = []
    scores = []
    class_ids = []

    for i in range(rows):
        classes_scores = outputs[0][i][4:]
        (minScore, maxScore, minClassLoc, (x, maxClassIndex)) = cv2.minMaxLoc(classes_scores)
        if maxScore >= 0.25:
            box = [
                outputs[0][i][0] - (0.5 * outputs[0][i][2]), outputs[0][i][1] - (0.5 * outputs[0][i][3]),
                outputs[0][i][2], outputs[0][i][3]]
            boxes.append(box)
            scores.append(maxScore)
            class_ids.append(maxClassIndex)
    result_boxes = cv2.dnn.NMSBoxes(boxes, scores, 0.25, 0.45, 0.5)
    detections = []
    scale = 1
    for i in range(len(result_boxes)):
        index = result_boxes[i]
        box = boxes[index]
        detection = {
            'class_id': class_ids[index],
            'class_name': CLASSES[class_ids[index]],
            'confidence': scores[index],
            'box': box,
            'scale': scale}
        detections.append(detection)
        draw_bounding_box(source, class_ids[index], scores[index], round(box[0] * scale), round(box[1] * scale),
                          round((box[0] + box[2]) * scale), round((box[1] + box[3]) * scale))
    return source;
    pass
def main():
    model: cv2.dnn.Net = cv2.dnn.readNetFromONNX('best.onnx')
    
    # RTSP 地址
    rtsp_url = "rtsp://192.168.31.12:8554/mjpeg/1"
    # 打开 RTSP 视频流
    cap = cv2.VideoCapture(rtsp_url)
    # 检查视频是否成功打开
    if not cap.isOpened():
        print("Failed to open RTSP stream")
    # 循环读取视频帧
    while True:
        # 读取视频帧
        ret, frame = cap.read()
        # 检查是否成功读取视频帧
        if not ret:
            break
        sb = detect(model,frame)
        # 显示视频帧
        cv2.imshow("RTSP Stream", sb)
        # 按 'q' 键退出循环
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # 释放资源
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

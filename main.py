import json
import requests
import sys
import cv2
import os

LIMIT_PX = 1024
LIMIT_BYTE = 1024 * 1024  # 1MB
LIMIT_BOX = 40


def kakao_ocr_resize(image_path: str):
    """
    ocr detect/recognize api helper
    ocr api의 제약사항이 넘어서는 이미지는 요청 이전에 전처리가 필요.

    pixel 제약사항 초과: resize
    용량 제약사항 초과  : 다른 포맷으로 압축, 이미지 분할 등의 처리 필요. (예제에서 제공하지 않음)

    :param image_path: 이미지파일 경로
    :return:
    """
    image = cv2.imread(image_path)
    height, width, _ = image.shape

    if LIMIT_PX < height or LIMIT_PX < width:
        ratio = float(LIMIT_PX) / max(height, width)
        image = cv2.resize(image, None, fx=ratio, fy=ratio)
        height, width, _ = height, width, _ = image.shape

        # api 사용전에 이미지가 resize된 경우, recognize시 resize된 결과를 사용해야함.
        image_path = "{}_resized.jpg".format(image_path)
        print(image_path + ": 원본 대신 리사이즈된 이미지를 사용합니다.")
        cv2.imwrite(image_path, image)

    return image_path


def kakao_ocr(image_path: str, appkey: str):
    """
    OCR api request example
    :param image_path: 이미지파일 경로
    :param appkey: 카카오 앱 REST API 키
    """
    API_URL = 'https://dapi.kakao.com/v2/vision/text/ocr'

    headers = {'Authorization': 'KakaoAK {}'.format(appkey)}

    image = cv2.imread(image_path)
    jpeg_image = cv2.imencode(".jpg", image)[1]
    data = jpeg_image.tobytes()

    return requests.post(API_URL, headers=headers, files={"image": data})


def get_attendance_list(image_path, appkey):
    image_list = os.listdir(image_path)
    target_image_list = []
    for image in image_list:
        target_image_list.append(kakao_ocr_resize(image_path + "/" + image))

    attendance_list = []

    for target_image_path in target_image_list:
        output = kakao_ocr(target_image_path, appkey).json()
        tmp = output["result"]
        for dic in tmp:
            tar = dic["recognition_words"][0]
            attendance_list.append(tar)

    return attendance_list


def main():
    if len(sys.argv) != 4:
        print("Please run with args: $ python example.py /path/to/앞출석 /path/to/뒤출석 appkey")
    before_screenshot, after_screenshot, appkey = sys.argv[1], sys.argv[2], sys.argv[3]

    before_attendance_list = get_attendance_list(before_screenshot, appkey)
    after_attendance_list = get_attendance_list(after_screenshot, appkey)
    before_attendance_list.sort()
    after_attendance_list.sort()

    before_set = set(before_attendance_list)
    after_set = set(after_attendance_list)

    both_attendance = before_set & after_set
    only_before_attendance = before_set - after_set
    only_after_attendance = after_set - before_set

    result = {"both": list(both_attendance), "only_before": list(only_before_attendance), "only_after": list(only_after_attendance)}

    with open("attendance.json", "w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()

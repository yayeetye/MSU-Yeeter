from inference.models.utils import get_roboflow_model
import re
import pyautogui
import time as t
from keypress import *

model_name = "Rune Solver"
model_version = "1"
model = get_roboflow_model(
    model_id="rune-solver-msvzh-z3rhg/1".format(model_name, model_version),
    # Replace ROBOFLOW_API_KEY with your Roboflow API Key
    api_key="NWGzKCmGFDeUpYh68S1G"
)
def extract_x_and_class(pred_str):
    result = {}
    x_match = re.search(r"x=([0-9.]+)", pred_str)
    class_name_match = re.search(r"class_name='([^']*)'", pred_str)
    if x_match:
        result['x'] = float(x_match.group(1))
    if class_name_match:
        result['class_name'] = class_name_match.group(1)
    return result

def rune_break():
    print("rune solver initialised")
    alt()
    t.sleep(2)
    photo = pyautogui.screenshot(region=(0, 0, 1280, 720))
    #photo = "rune.png"
    results = model.infer(image=photo,
                          confidence=0.5,
                          iou_threshold=0.5)  # get result

    s = str(results[0])  # turn the only element in the list to a stirng to be processed

    predictions_str = s.split("predictions=")[1].strip()

    pattern = r'ObjectDetectionPrediction\((.*?)\)'
    matches = re.findall(pattern, predictions_str)  # make a list with 4 element, each one is a long string now.
    # the past 4 line processes it into only the arrow and arrow's descripting elements.

    if (len(matches) == 4):  # check if 4 arrows

        filtered_predictions = [extract_x_and_class(p) for p in matches]  # filter out only x and direciotnal input

        # Optional: Wrap in dictionary
        final_result = {"predictions": filtered_predictions}


        # print("time taken is ", t2 - t1)

        filt_result = final_result["predictions"]


        x_list = []
        for i in range(4):
            x_list.append([float(filt_result[i]['x']), filt_result[i]['class_name']])
            # print(x_list)

        x_list.sort(key=lambda item: item[0])
        # print(x_list)

        for i in range(len(x_list)):
            # pdi.press(x_list[i][1])
            f"{function_map[x_list[i][1]]()}"
            print(x_list[i][1])
            t.sleep(random.uniform(0.05, 0.25))
        return 0

    else:
        print("unable to detect 4 arrows")
        return 0
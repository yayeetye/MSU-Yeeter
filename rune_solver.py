from inference_sdk import InferenceHTTPClient
import pydirectinput as pdi
import time as t
import random
import pyautogui

def rune_break():
#print("calculating start")
    pdi.press("alt")
    t.sleep(2)
    CLIENT = InferenceHTTPClient(
        api_url="https://serverless.roboflow.com",
        api_key="ywk645kJCLEghnzcsq0N"
    )


    CLIENT2 = InferenceHTTPClient(
        api_url="https://serverless.roboflow.com",
        api_key="ywk645kJCLEghnzcsq0N"
    )

    photo = pyautogui.screenshot(region=(0,0, 1280, 720))
    try:
        result = CLIENT.infer(photo, model_id="rune-solver-msvzh-z3rhg/1")
    except:
        print("roboflow V2 failed, using V1")
        result = CLIENT2.infer(photo, model_id="rune-solver-msvzh-z3rhg/1")
    #print("done!")
    print(result)

     #first do filt_result = result["predictions"] to filter out uselss calls
    filt_result = result["predictions"]
    #then sort by x
    #then output directions
    if(len(filt_result)==4):
        x_list = []
        for i in range(4):
            print(i)
            x_list.append([    float(filt_result[i]['x'])   , filt_result[i]['class']])
        #print(x_list)


        x_list.sort(key=lambda item: item[0])
        #print(x_list)


        for i in range (len(x_list)):
            pdi.press(x_list[i][1])
            print(x_list[i][1])
            t.sleep(random.uniform(0.05, 0.25))

        return 0
    else:
        print("unable to detect 4 arrows")
from inference_sdk import InferenceHTTPClient
x = 1
while x < 100:

    CLIENT = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key="ywk645kJCLEghnzcsq0N"
    )

    result = CLIENT.infer('rune.png', model_id="rune-solver-msvzh-z3rhg/1")

    print(result)
    print(str(x))
    x = x+1
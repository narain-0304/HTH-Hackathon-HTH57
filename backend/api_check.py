import google.generativeai as genai

genai.configure(api_key="AIzaSyCyZxm_TFM3Z-LxcJaqES_FnkEGlFIrAOk")
models = genai.list_models()
for model in models:
    print(model.name)

from flask import Flask, json, request, jsonify
from flask_cors import CORS
import pymysql
import erniebot
import base64
import requests
import os
from werkzeug.utils import secure_filename
from paddlespeech.cli.asr.infer import ASRExecutor


DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resource={r'/*': {'origins': '*'}})

erniebot.api_type = 'aistudio'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif','wav'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

OCR_API_URL = "https://b9m7e3705c6bm2l3.aistudio-hub.baidu.com/ocr"
OCR_TOKEN = "1448c89ed7a84bf7f696097eaf645ab7f6ca822d"

TABLE_API_URL = "https://ufua65f3l5eeybef.aistudio-hub.baidu.com/table-recognition"
TABLE_TOKEN = "1448c89ed7a84bf7f696097eaf645ab7f6ca822d"  # 请替换为您的实际token

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/ocr', methods=['POST'])
def ocr():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            # 读取图片文件并进行Base64编码
            with open(filepath, "rb") as image_file:
                image_base64 = base64.b64encode(image_file.read()).decode('ascii')

            # 设置请求头和请求体
            headers = {
                "Authorization": f"token {OCR_TOKEN}",
                "Content-Type": "application/json"
            }
            payload = {
                "image": image_base64
            }

            # 发送请求到OCR API
            resp = requests.post(url=OCR_API_URL, json=payload, headers=headers)
            print(resp.status_code)
            if resp.status_code == 200:
                result = resp.json()["result"]
                # 提取文本信息
                texts = result["texts"]
                # 将文本信息组合成一个字符串
                text_result = "\n".join([text["text"] for text in texts])
                os.remove(filepath)  # 删除临时文件
                return jsonify({'result': text_result})
            else:
                return jsonify({'error': 'OCR API request failed'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'File type not allowed'}), 400


@app.route('/api/speech', methods=['POST'])
def speech_recognition():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            asr = ASRExecutor()
            result = asr(audio_file=filepath, model='conformer_online_wenetspeech')
            os.remove(filepath)
            return jsonify({'result': result}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/api/table', methods=['POST'])
def table_recognition():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            # 读取图片文件并进行Base64编码
            with open(filepath, "rb") as image_file:
                image_base64 = base64.b64encode(image_file.read()).decode('ascii')

            # 设置请求头和请求体
            headers = {
                "Authorization": f"token {TABLE_TOKEN}",
                "Content-Type": "application/json"
            }
            payload = {
                "image": image_base64
            }

            # 发送请求到表格识别API
            resp = requests.post(url=TABLE_API_URL, json=payload, headers=headers)

            if resp.status_code == 200:
                result = resp.json()["result"]
                # 提取表格信息和处理后的图片
                tables = result["tables"]
                table_image = result["ocrImage"]

                os.remove(filepath)  # 删除临时文件
                return jsonify({
                    'result': tables,
                    'processedImage': table_image
                })
            else:
                return jsonify({'error': 'Table recognition API request failed'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/getpolish', methods=["GET", "POST"])
def getpolish():
    # 获取用户名
    username= request.form.get("username")
    # 获取用户的访问令牌
    print(username)
    key = request.form.get("key")
    print(key)
    # 获取用户提问内容
    quescont = request.form.get("cont")
    askcont="帮我润色下面这段话:"+quescont

    erniebot.access_token = key
    try:
        response = erniebot.ChatCompletion.create(
            model='ernie-bot',
            messages=[{'role': 'user', 'content':askcont}],
        )
        restext = response['result']
        webdict = {'answer': restext}
        return jsonify(webdict)
    except:
        return "error"

@app.route('/getcontinuation', methods=["GET", "POST"])
def getcontinuation():
    # 获取用户名
    username= request.form.get("username")
    print(username)
    # 获取用户的访问令牌
    key = request.form.get("key")
    # 获取用户提问内容
    quescont = request.form.get("cont")
    askcont="帮我续写下面这段话:"+quescont

    erniebot.access_token = key
    try:
        response = erniebot.ChatCompletion.create(
            model='ernie-bot',
            messages=[{'role': 'user', 'content':askcont}],
        )
        restext = response['result']
        webdict = {'answer': restext}
        return jsonify(webdict)
    except:
        return "error"

@app.route('/gettranslation', methods=["GET", "POST"])
def gettranslation():
    # 获取用户名
    username= request.form.get("username")
    print(username)
    # 获取用户的访问令牌
    key = request.form.get("key")
    # 获取用户提问内容
    quescont = request.form.get("cont")
    askcont="帮我用英语翻译下面这段话:"+quescont

    erniebot.access_token = key
    try:
        response = erniebot.ChatCompletion.create(
            model='ernie-bot',
            messages=[{'role': 'user', 'content':askcont}],
        )
        restext = response['result']
        print(restext)
        webdict = {'answer': restext}
        return jsonify(webdict)
    except:
        return "error"

@app.route('/getsummarize', methods=["GET", "POST"])
def getsummarize():
    # 获取用户名
    username= request.form.get("username")
    print(username)
    # 获取用户的访问令牌
    key = request.form.get("key")
    # 获取用户提问内容
    quescont = request.form.get("cont")
    askcont="请帮我给下面这段话写一个摘要:"+quescont

    erniebot.access_token = key
    try:
        response = erniebot.ChatCompletion.create(
            model='ernie-bot',
            messages=[{'role': 'user', 'content':askcont}],
        )
        restext = response['result']
        webdict = {'answer': restext}
        return jsonify(webdict)
    except:
        return "error"

@app.route('/getproofread', methods=["GET", "POST"])
def getproofread():
    # 获取用户名
    username= request.form.get("username")
    print(username)
    # 获取用户的访问令牌
    key = request.form.get("key")
    # 获取用户提问内容
    quescont = request.form.get("cont")
    askcont="请修改下面这句话中的语病和错别字，使之能够通顺流畅，但不改变原意思:"+quescont

    erniebot.access_token = key
    try:
        response = erniebot.ChatCompletion.create(
            model='ernie-bot',
            messages=[{'role': 'user', 'content':askcont}],
        )
        restext = response['result']
        print(restext)
        webdict = {'answer': restext}
        return jsonify(webdict)
    except:
        return "error"


@app.route('/api/mindmap', methods=['POST'])
def generate_mindmap():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    text = data['text']

    try:
        # 调用文心大模型生成思维导图
        response = erniebot.create_mindmap(text)

        # 假设返回的是SVG格式的思维导图
        mindmap_svg = response['mindmap']

        return jsonify({'mindmap': mindmap_svg})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(host="127.0.0.1", port=5000, debug=True)
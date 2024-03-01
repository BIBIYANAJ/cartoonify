from flask import Flask, render_template, request, redirect
import cv2
import numpy as np
import base64

app = Flask(__name__, template_folder='template')

def edge_mask(img, line_size, blur_value):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.medianBlur(gray, blur_value)
    edges = cv2.adaptiveThreshold(gray_blur, 355, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_size, blur_value)
    return edges

def cartoon(img, edges, blurred):
    # Step 1: Create a mask to extract only strong edges with a thin line
    _, edges_thresh = cv2.threshold(edges, 100, 255, cv2.THRESH_BINARY)
    edges_mask = cv2.cvtColor(edges_thresh, cv2.COLOR_GRAY2BGR)

    # Step 2: Enhance edges and soften the image using bilateral filtering
    cartoon_img = cv2.bitwise_and(blurred, edges_mask)

    return cartoon_img

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cartoonify', methods=['POST'])
def cartoonify():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    try:
        # Read the uploaded image
        img_array = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        # Perform cartoonification
        edges = edge_mask(img, line_size=5, blur_value=5)
        blurred = cv2.bilateralFilter(img, 9, 300, 300)
        cartoonified_img = cartoon(img, edges, blurred)

        # Convert images to base64 for display
        _, img_encoded = cv2.imencode('.png', img)
        original_img_base64 = base64.b64encode(img_encoded).decode('utf-8')

        _, cartoonified_img_encoded = cv2.imencode('.png', cartoonified_img)
        cartoonified_img_base64 = base64.b64encode(cartoonified_img_encoded).decode('utf-8')

        return render_template('result.html', original_img=original_img_base64, cartoon_img=cartoonified_img_base64)
    except Exception as e:
        print("Error:", e)
        return "An error occurred while processing the image."

if __name__ == '__main__':
    app.run(debug=True)
'''from flask import Flask, render_template, request, redirect
import cv2
import numpy as np
import base64

app = Flask(__name__, template_folder='template')

def edge_mask(img, line_size, blur_value):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.medianBlur(gray, blur_value)
    edges = cv2.adaptiveThreshold(gray_blur, 340, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_size, blur_value)
    return edges

def cartoon(img, edges, blurred):
    # Step 1: Create a mask to extract only strong edges with a thin line
    _, edges_thresh = cv2.threshold(edges, 200, 266, cv2.THRESH_BINARY)
    edges_mask = cv2.cvtColor(edges_thresh, cv2.COLOR_GRAY2BGR)

    # Step 2: Enhance edges and soften the image using bilateral filtering
    cartoon_img = cv2.bitwise_and(blurred, edges_mask)

    return cartoon_img

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cartoonify', methods=['POST'])
def cartoonify():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    try:
        # Read the uploaded image
        img_array = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        # Perform cartoonification
        edges = edge_mask(img, line_size=7, blur_value=7)
        blurred = cv2.bilateralFilter(img, 9, 300, 300)
        cartoonified_img = cartoon(img, edges, blurred)

        # Convert images to base64 for display
        _, img_encoded = cv2.imencode('.png', img)
        original_img_base64 = base64.b64encode(img_encoded).decode('utf-8')

        _, cartoonified_img_encoded = cv2.imencode('.png', cartoonified_img)
        cartoonified_img_base64 = base64.b64encode(cartoonified_img_encoded).decode('utf-8')

        return render_template('result.html', original_img=original_img_base64, cartoon_img=cartoonified_img_base64)
    except Exception as e:
        print("Error:", e)
        return "An error occurred while processing the image."

if __name__ == '__main__':
    app.run(debug=True)'''


---------------------#FIRST-APPROACH------------------------
import cv2
import numpy as np
import mediapipe as mp

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)

# ==================== Helper Functions ====================

def capture_face_image(window_name="Capture Face"):
    cap = cv2.VideoCapture(0)
    captured = False
    img = None

    print(f"📷 Press SPACE to capture image in window: {window_name}")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow(window_name, frame)
        key = cv2.waitKey(1)
        if key == 32:  # Space key to capture
            img = frame.copy()
            captured = True
            break
        elif key == 27:  # ESC to exit
            break

    cap.release()
    cv2.destroyAllWindows()
    if not captured:
        raise Exception("Image not captured")
    return img

def get_landmarks(img):
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb)
    if not result.multi_face_landmarks:
        raise Exception("No face detected")
    landmarks = result.multi_face_landmarks[0]
    h, w, _ = img.shape
    points = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks.landmark]
    return points

def get_triangle_indices(points, img_shape):
    subdiv = cv2.Subdiv2D((0, 0, img_shape[1], img_shape[0]))
    for p in points:
        subdiv.insert(p)
    triangle_list = subdiv.getTriangleList()
    indices = []
    for t in triangle_list:
        pts = [(int(t[0]), int(t[1])), (int(t[2]), int(t[3])), (int(t[4]), int(t[5]))]
        idx = []
        for pt in pts:
            for i, p in enumerate(points):
                if abs(pt[0] - p[0]) < 1 and abs(pt[1] - p[1]) < 1:
                    idx.append(i)
        if len(idx) == 3:
            indices.append(tuple(idx))
    return indices

def warp_triangle(img1, img2, t1, t2):
    r1 = cv2.boundingRect(np.float32([t1]))
    r2 = cv2.boundingRect(np.float32([t2]))

    t1Rect = [(t1[i][0] - r1[0], t1[i][1] - r1[1]) for i in range(3)]
    t2Rect = [(t2[i][0] - r2[0], t2[i][1] - r2[1]) for i in range(3)]

    mask = np.zeros((r2[3], r2[2], 3), dtype=np.float32)
    cv2.fillConvexPoly(mask, np.int32(t2Rect), (1.0, 1.0, 1.0), 16)

    img1Rect = img1[r1[1]:r1[1]+r1[3], r1[0]:r1[0]+r1[2]]
    size = (r2[2], r2[3])

    warpMat = cv2.getAffineTransform(np.float32(t1Rect), np.float32(t2Rect))
    img2Rect = cv2.warpAffine(img1Rect, warpMat, size, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)

    img2Rect = img2Rect * mask
    img2_subsection = img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]]
    img2_subsection = img2_subsection * (1 - mask)
    img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] = img2_subsection + img2Rect

# ==================== Main Process ====================

# Step 1: Capture images from webcam
print("📸 Capture FACE 1")
img1 = capture_face_image("Face 1")

print("📸 Capture FACE 2")
img2 = capture_face_image("Face 2")

# Resize second image to match first
img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

# Step 2: Extract landmarks
points1 = get_landmarks(img1)
points2 = get_landmarks(img2)

# Step 3: Triangulation indices based on image 1
tri_indices = get_triangle_indices(points1, img1.shape)

# Step 4: Warp triangles from img1 to img2
img2_warped = img2.copy()
for tri in tri_indices:
    t1 = [points1[i] for i in tri]
    t2 = [points2[i] for i in tri]
    warp_triangle(img1, img2_warped, t1, t2)

# Step 5: Seamless cloning
hull2 = cv2.convexHull(np.array(points2, dtype=np.int32))
mask = np.zeros_like(img2)
cv2.fillConvexPoly(mask, hull2, (255, 255, 255))
r = cv2.boundingRect(hull2)
center = (r[0] + r[2] // 2, r[1] + r[3] // 2)

output = cv2.seamlessClone(img2_warped, img2, mask, center, cv2.NORMAL_CLONE)

# Step 6: Show result
cv2.imshow("🧑‍🤝‍🧑 Swapped Face", output)
cv2.waitKey(0)
cv2.destroyAllWindows()









----------------------------#SECOND-APPROACH----------------------
from flask import Flask, request, send_file, jsonify
import cv2
import numpy as np
import mediapipe as mp
import tempfile
import os

app = Flask(__name__)
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)

# ====================== Core Utility Functions ======================

def get_landmarks(img):
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb)
    if not result.multi_face_landmarks:
        raise Exception("No face detected")
    landmarks = result.multi_face_landmarks[0]
    h, w, _ = img.shape
    return [(int(lm.x * w), int(lm.y * h)) for lm in landmarks.landmark]

def get_triangle_indices(points, img_shape):
    subdiv = cv2.Subdiv2D((0, 0, img_shape[1], img_shape[0]))
    for p in points:
        subdiv.insert(p)
    triangle_list = subdiv.getTriangleList()
    indices = []
    for t in triangle_list:
        pts = [(int(t[0]), int(t[1])), (int(t[2]), int(t[3])), (int(t[4]), int(t[5]))]
        idx = []
        for pt in pts:
            for i, p in enumerate(points):
                if abs(pt[0] - p[0]) < 1 and abs(pt[1] - p[1]) < 1:
                    idx.append(i)
        if len(idx) == 3:
            indices.append(tuple(idx))
    return indices

def warp_triangle(img1, img2, t1, t2):
    r1 = cv2.boundingRect(np.float32([t1]))
    r2 = cv2.boundingRect(np.float32([t2]))

    t1Rect = [(t1[i][0] - r1[0], t1[i][1] - r1[1]) for i in range(3)]
    t2Rect = [(t2[i][0] - r2[0], t2[i][1] - r2[1]) for i in range(3)]

    mask = np.zeros((r2[3], r2[2], 3), dtype=np.float32)
    cv2.fillConvexPoly(mask, np.int32(t2Rect), (1.0, 1.0, 1.0), 16)

    img1Rect = img1[r1[1]:r1[1]+r1[3], r1[0]:r1[0]+r1[2]]
    size = (r2[2], r2[3])
    warpMat = cv2.getAffineTransform(np.float32(t1Rect), np.float32(t2Rect))
    img2Rect = cv2.warpAffine(img1Rect, warpMat, size, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)

    img2Rect = img2Rect * mask
    img2_sub = img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]]
    img2_sub = img2_sub * (1 - mask)
    img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] = img2_sub + img2Rect

# ====================== Flask Route ======================

@app.route("/swap-face", methods=["POST"])
def swap_face():
    try:
        if 'face1' not in request.files or 'face2' not in request.files:
            return jsonify({"error": "Missing images. Please upload 'face1' and 'face2'"}), 400

        # Read uploaded files
        file1 = request.files['face1']
        file2 = request.files['face2']

        npimg1 = np.frombuffer(file1.read(), np.uint8)
        img1 = cv2.imdecode(npimg1, cv2.IMREAD_COLOR)

        npimg2 = np.frombuffer(file2.read(), np.uint8)
        img2 = cv2.imdecode(npimg2, cv2.IMREAD_COLOR)
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

        # Landmark detection
        points1 = get_landmarks(img1)
        points2 = get_landmarks(img2)

        # Warp triangles
        tri_indices = get_triangle_indices(points1, img1.shape)
        img2_warped = img2.copy()
        for tri in tri_indices:
            t1 = [points1[i] for i in tri]
            t2 = [points2[i] for i in tri]
            warp_triangle(img1, img2_warped, t1, t2)

        # Seamless cloning
        hull2 = cv2.convexHull(np.array(points2, dtype=np.int32))
        mask = np.zeros_like(img2)
        cv2.fillConvexPoly(mask, hull2, (255, 255, 255))
        r = cv2.boundingRect(hull2)
        center = (r[0] + r[2] // 2, r[1] + r[3] // 2)

        output = cv2.seamlessClone(img2_warped, img2, mask, center, cv2.NORMAL_CLONE)

        # Save to temp file and return
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        cv2.imwrite(tmp.name, output)

        return send_file(tmp.name, mimetype='image/jpeg', as_attachment=True, download_name="swapped_face.jpg")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ====================== Run ======================

if __name__ == "__main__":
    app.run(debug=True)

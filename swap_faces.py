import cv2
import numpy as np
import mediapipe as mp

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True)

# Load images
img1 = cv2.imread("face1.jpg")
img2 = cv2.imread("face2.jpg")
img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

def get_landmarks(img):
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb)
    if not result.multi_face_landmarks:
        raise Exception("No face detected")
    landmarks = result.multi_face_landmarks[0]
    h, w, _ = img.shape
    points = []
    for lm in landmarks.landmark:
        x, y = int(lm.x * w), int(lm.y * h)
        points.append((float(x), float(y)))
    return points

def get_triangle_indices(points):
    subdiv = cv2.Subdiv2D((0, 0, img1.shape[1], img1.shape[0]))
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

    t1Rect = []
    t2Rect = []
    for i in range(3):
        t1Rect.append(((t1[i][0] - r1[0]), (t1[i][1] - r1[1])))
        t2Rect.append(((t2[i][0] - r2[0]), (t2[i][1] - r2[1])))

    mask = np.zeros((r2[3], r2[2], 3), dtype=np.float32)
    cv2.fillConvexPoly(mask, np.int32(t2Rect), (1.0, 1.0, 1.0), 16, 0)

    img1Rect = img1[r1[1]:r1[1]+r1[3], r1[0]:r1[0]+r1[2]]
    size = (r2[2], r2[3])

    warpMat = cv2.getAffineTransform(np.float32(t1Rect), np.float32(t2Rect))
    img2Rect = cv2.warpAffine(img1Rect, warpMat, size, None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)

    img2Rect = img2Rect * mask
    img2_subsection = img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]]
    img2_subsection = img2_subsection * (1 - mask)
    img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] = img2_subsection + img2Rect

# Process landmarks
points1 = get_landmarks(img1)
points2 = get_landmarks(img2)

# Get triangle indices
tri_indices = get_triangle_indices(points1)

# Warp triangles
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

cv2.imshow("Swapped Face", output)
cv2.waitKey(0)
cv2.destroyAllWindows()

import cv2
import numpy as np
import random
import time
import dlib
import sys


# # ------------------------------------ Inputs
ratio_blinking = 0.2 # calibrate with my eyes
dict_color = {'green': (0,255,0),
              'blue':(255,0,0),
              'red': (0,0,255),
              'yellow': (0,255,255),
              'white': (255, 255, 255),
              'black': (0,0,0)}
# # ------------------------------------







# -----   Initialize camera
def init_camera(camera_ID):
    camera = cv2.VideoCapture(0)
    return camera
# --------------------------------------------------

# ----- Make black page [3 channels]
def make_black_page(size):
    page = (np.zeros((int(size[0]), int(size[1]), 3))).astype('uint8')
    return page
# --------------------------------------------------

# ----- Make white page [3 channels]
def make_white_page(size):
    page = (np.zeros((int(size[0]), int(size[1]), 3)) + 255).astype('uint8')
    return page
# --------------------------------------------------

# -----   Rotate / flip / everything else (NB: depends on camera conf)
def adjust_frame(frame):
    # frame = cv2.rotate(frame, cv2.ROTATE_180)
    frame = cv2.flip(frame, 1)
    return frame
# --------------------------------------------------

# ----- Shut camera / windows off
def shut_off(camera):
    camera.release() # When everything done, release the capture
    cv2.destroyAllWindows()
# --------------------------------------------------

# ----- Show a window
def show_window(title_window, window):
    cv2.namedWindow(title_window)
    cv2.imshow(title_window,window)
# --------------------------------------------------

# ----- show on frame a box containing the face
def display_box_around_face(img, box, color, size):
    x_left, y_top, x_right, y_bottom = box[0], box[1], box[2], box[3]
    cv2.rectangle(img, (x_left-size[0], y_top-size[1]), (x_right+size[0], y_bottom+size[1]),
                 dict_color[color], 5)
# --------------------------------------------------

# ----- get mid point
def half_point(p1 ,p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)
# --------------------------------------------------

# ----- get coordinates eye
def get_eye_coordinates(landmarks, points):

    x_left = (landmarks.part(points[0]).x, landmarks.part(points[0]).y)
    x_right = (landmarks.part(points[3]).x, landmarks.part(points[3]).y)

    y_top = half_point(landmarks.part(points[1]), landmarks.part(points[2]))
    y_bottom = half_point(landmarks.part(points[5]), landmarks.part(points[4]))

    return x_left, x_right, y_top, y_bottom
# --------------------------------------------------

# ----- draw line on eyes
def display_eye_lines(img, coordinates, color):
    cv2.line(img, coordinates[0], coordinates[1], dict_color[color], 2)
    cv2.line(img, coordinates[2], coordinates[3], dict_color[color], 2)
# --------------------------------------------------

# ----- draw circle at face landmark points
def display_face_points(img, landmarks, points_to_draw, color):
    for point in range(points_to_draw[0], points_to_draw[1]):
        x = landmarks.part(point).x
        y = landmarks.part(point).y
        cv2.circle(img, (x, y), 4, dict_color[color], 2)
# --------------------------------------------------

# ----- function to check blinking
def is_blinking(eye_coordinates):
    blinking = False

    major_axis = np.sqrt((eye_coordinates[1][0]-eye_coordinates[0][0])**2 + (eye_coordinates[1][1]-eye_coordinates[0][1])**2)
    minor_axis = np.sqrt((eye_coordinates[3][0]-eye_coordinates[2][0])**2 + (eye_coordinates[3][1]-eye_coordinates[2][1])**2)

    ratio = minor_axis / major_axis

    if ratio < ratio_blinking: blinking = True

    return blinking
# --------------------------------------------------

# ----- find the limits of frame-cut around the calibrated box
def find_cut_limits(calibration_cut):
    x_cut_max = np.transpose(np.array(calibration_cut))[0].max()
    x_cut_min = np.transpose(np.array(calibration_cut))[0].min()
    y_cut_max = np.transpose(np.array(calibration_cut))[1].max()
    y_cut_min = np.transpose(np.array(calibration_cut))[1].min()

    return x_cut_min, x_cut_max, y_cut_min, y_cut_max
# --------------------------------------------------

# ----- find if the pupil is in the calibrated frame
def pupil_on_cut_valid(pupil_on_cut, cut_frame):
    in_frame_cut = False
    condition_x = ((pupil_on_cut[0] > 0) & (pupil_on_cut[0] < cut_frame.shape[1]))
    condition_y = ((pupil_on_cut[1] > 0) & (pupil_on_cut[1] < cut_frame.shape[0]))
    if condition_x and condition_y:
        in_frame_cut = True

    return in_frame_cut
# --------------------------------------------------

# ----- find projection on page
def project_on_page(img_from, img_to, point):

    scale = (np.array(img_to.shape) / np.array(img_from.shape))  #.astype('int')

    projected_point = (point * scale).astype('int')
    return projected_point
# --------------------------------------------------

# -----   display keys on frame, frame by frame
def dysplay_keyboard(img, keys):

    color_board = (255, 250, 100)
    for key in keys:
		cv2.putText(img,   key[0], key[1], cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 100), thickness = 3)
		cv2.rectangle(img, key[2], key[3], color_board, thickness = 4)
# --------------------------------------------------

# -----   check key on keyboard and take input
def identify_key(key_points, coordinate_X, coordinate_Y):
    pressed_key = False

    for key in range(0, len(key_points)):
        condition_1 = np.mean(np.array([coordinate_Y, coordinate_X]) > np.array(key_points[key][2]))
        condition_2 = np.mean(np.array([coordinate_Y, coordinate_X]) < np.array(key_points[key][3]))

        if (int(condition_1 + condition_2) == 2):
            pressed_key = key_points[key][0]
            break
    return pressed_key
# --------------------------------------------------

# -----   compute eye's radius
def take_radius_eye(eye_coordinates):
    radius = np.sqrt((eye_coordinates[3][0]-eye_coordinates[2][0])**2 + (eye_coordinates[3][1]-eye_coordinates[2][1])**2)
    return int(radius)
# --------------------------------------------------

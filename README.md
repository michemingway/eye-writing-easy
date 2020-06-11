# simple eye-writing project

This is a short & simple project of eye tracking and writing.
It makes use of machine learning-based facial mapping (landmarks) with dlib + python + openCV, with eyes projection on a virtual keyboard. 
The algorithm works in real-time on the video-stream from the webcam. 

Video example: https://www.youtube.com/watch?v=_vMNbsJFbqM

Logic flow:
- find face and track the right eye;
- calibrate the proper range of allowed space for (comfortable) movement;
(then, frame by frame)
- track the right eye and project its centroid on a virtual keyboard in a "working window";
- take inputs and, specifically, "press" the key, using blinking detection;
- updtate a text string and print on screen (and, by just adding a couple of line, on a file).

Notes:
The python script is highly simplified for didactic purposes, with a basic structure (only main and functions).
All the necessary functions are in the single file eye_key_funcs.py. The virtual keyboard is in projected_keyboard.py.

--------------------------------------------------------------------------------------------
Requirements: 
- python2 (python3 works too, just change "print")
- opencv
- numpy
- dlib (and the trained model shape_predictor_68_face_landmarks.dat; see below)
--------------------------------------------------------------------------------------------

More useful information about Facial mapping (landmarks) with Dlib + python can be found here:
https://towardsdatascience.com/facial-mapping-landmarks-with-dlib-python-160abcf7d672
https://www.pyimagesearch.com/2017/04/03/facial-landmarks-dlib-opencv-python/

The trained model file shape_predictor_68_face_landmarks.dat can be found here:
https://github.com/davisking/dlib-models/blob/master/shape_predictor_68_face_landmarks.dat.bz2
and all the details here:
https://github.com/davisking/dlib-models

import sys
import os
import dlib
import glob
from skimage import io
# hacked from the dlib example:
# http://dlib.net/face_landmark_detection.py.html
# mixed camelCase and _, sorry.
if len(sys.argv) != 2:
    print """
    Please provide a folder of named images with faces in them.

    generate_face_vectors.py folder/
    """
    sys.exit()

predictor_path = "shape_predictor_68_face_landmarks.dat"
face_rec_model_path = "dlib_face_recognition_resnet_model_v1.dat"
faces_folder_path = sys.argv[1]


detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(predictor_path)
facerec = dlib.face_recognition_model_v1(face_rec_model_path)
# Now process all the images
for f in glob.glob(os.path.join(faces_folder_path, "*.jpg")):
    print "Processing file: {}".format(f)
    try:
        img = io.imread(f)
    except IOError as e:
        #because SKimage isnt the greatest at opening images....
        print "cannot open {0} because of: {1}".format(f, e)
        continue
    try:
        dets = detector(img, 1)
    except RuntimeError as e:
        print "can't run detector on image {0}, because {1}".format(f,e)
        continue
    print "Number of faces detected: {}".format(len(dets))

    # Now process each face we found.
    for k, d in enumerate(dets):
        print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
            k, d.left(), d.top(), d.right(), d.bottom()))
        # Get the landmarks/parts for the face in box d.
        shape = sp(img, d)
        face_descriptor = facerec.compute_face_descriptor(img, shape)


def getName(name):
    """A function that will return a friendly name
    from a import filename like:
    candidates/Donald-Tusk-1.jpg
    """

    # is there a / in the string?
    if '/' in name:
        #remove the directory fluff and return the last part only
        name = name.split('/')[-1]

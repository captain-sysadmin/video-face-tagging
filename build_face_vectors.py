import sys
import os
import glob
import dlib
from skimage import io
import numpy as np
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

def getName(name):
    """A function that will return a friendly name
    from a import filename like:
    candidates/Donald-Tusk-1.jpg
    """

    print name
    # is there a / in the string?
    if '/' in name:
        #remove the directory fluff and return the last part only
        name = name.split('/')[-1]
        if '.jpg' in name:
            name = name.split('.')[0]
        else:
            raise ValueError
        name = name.split('-')
        name.pop(-1)
        finalName = ' '.join(name)
        return finalName

def compareFace(face1, face2, tolerance = 0.6):
    '''takes two 128 dimention face vetors
    and compares them to each other.

    will return a True if the compared face distance
    is below tolerance

    # https://github.com/ageitgey/face_recognition/blob/master/face_recognition/api.py
    '''
    if len(face1) == 0:
        return False
    faceDistance = np.linalg.norm(face1 - face2, axis=1)
    print faceDistance
    return faceDistance <= tolerance

faceDb = {}

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
        # now push that vector into an array...
        niceName = getName(f)
        if niceName in faceDb:
            faceDb[niceName].append(face_descriptor,)
            print "appending vectors"
        else:
            faceDb[niceName] = []
            faceDb[niceName].append(face_descriptor,)
            print "creating vectors"

for faceName, faceVectors in faceDb.iteritems():
    reference = faceVectors[0]
    print reference
    for faceVector in faceVectors:
        if compareFace(np.array(reference), np.array(faceVector)):
            print "Match"
        else:
            print "no match"


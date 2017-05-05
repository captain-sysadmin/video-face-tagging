import sys
import os
import glob
import face_recognition
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


faceDb = {}

# Now process all the images
for f in glob.glob(os.path.join(faces_folder_path, "*.jpg")):
    print "Processing file: {}".format(f)
    image = face_recognition.load_image_file(f)
    faceDescriptor = face_recognition.face_encodings(image)[0]
    # now push that vector into an array...
    niceName = getName(f)
    if niceName in faceDb:
        faceDb[niceName].append(faceDescriptor)
        print "appending vectors"
    else:
        faceDb[niceName] = []
        faceDb[niceName].append(faceDescriptor)
        print "creating vectors"

for faceName, faceVectors in faceDb.iteritems():
    reference = faceVectors[0]
    print reference
    for faceVector in faceVectors:
        if face_recognition.compare_faces(reference, faceVector):
            print "Match"
        else:
            print "no match"


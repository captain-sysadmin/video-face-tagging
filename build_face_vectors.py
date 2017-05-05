import sys
import os
import glob
import pickle
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
personDb = {}
# Now process all the images
for f in glob.glob(os.path.join(faces_folder_path, "*.jpg")):
    print "\t\tProcessing file: {}".format(f)
    try:
        image = face_recognition.load_image_file(f)
    except IOError as e:
        print "cannot open {0} becuase {1}".format(f, e)
        continue
    try:
        faceDescriptor = face_recognition.face_encodings(image)[0]
    except IndexError as e:
        print "cannot generate vectors for {0} becuase {1}".format(f, e)
        continue


    # now push that vector into an array...
    niceName = getName(f)
    if niceName in faceDb:
        faceDb[niceName].append(faceDescriptor)
    else:
        faceDb[niceName] = []
        faceDb[niceName].append(faceDescriptor)

for faceName, faceVectors in faceDb.iteritems():
    reference = faceVectors[0]
    matches = [False] * 5
    for count, faceVector in enumerate(faceVectors):
        if face_recognition.compare_faces([reference], faceVector):
            matches[count] = True
        else:
            print "no match"
    if matches.count(True) >= 4:
        #we know we have 4 matches to reference
        personDb[faceName] = reference
        print "{0}'s face captured".format(faceName)
    else:
        print "ERROR NOT ENOUGH MATCHES FOR {0}".format(faceName)


with open('facedb.pickle', 'wb') as pickleFile:
    pickle.dump(personDb, pickleFile)

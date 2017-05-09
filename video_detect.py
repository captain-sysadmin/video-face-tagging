#!/usr/bin/python

# Unpack a video into a number of screen grabs
# Iterrogate those screen grabs for faces
# Check those faces against a list of known people
#
import os
import glob
import pickle
import subprocess
import face_recognition
class recogniseFaces(object):
    '''A bunch of methods that allow a users to
    split a video into screen grabs, systematticaly go through
    and detect faces, and then compare them to a list of known
    faces.
    '''

    def __init__(self):
        '''BEGIN
        '''
        self.screenGrabInterval = 10 # extract every n frames
        self.tmpDir = '/tmp/'
        self.faceDb = {}

    def loadFaceDb(self, dbFileLocation):
        '''Load the pickle file that contains the
        dictionary of face name: vectors
        '''
        try:
            with open(dbFileLocation) as dbFile:
                self.faceDb = pickle.load(dbFile)
        except IOError as e:
            print "can't open the face DB: {0}".format(e)
    def getFrameNumber(self, filename):
        '''Takes a filename and returns a frame number
        '''

        name = filename.split("/")[-1]
        # now we should have 'faces_xxx.jpg'
        name = name.split('.')[0]
        number = name.split('_')[-1]
        return int(number) * self.screenGrabInterval


    def unpackVideo(self, filename):
        '''Takes a filename (path) and
        uses ffmpeg to extract frames to tmpDir
        '''
        returnCode = subprocess.call('ffmpeg -i {0} -vf "select=not(mod(n\,{1}))" -vsync vfr -q:v 2 {2}faces_%03d.jpg'.format(filename, self.screenGrabInterval, self.tmpDir), shell=True)
        if returnCode != 0:
            print "error, FFMPEG extraction failed. see STDOut"
            return False
    def detectFaces(self):
        '''Go through the tempDir and pull out all the faces
        and then compare them to a known list
        '''
        matches = {}
        for f in glob.glob(os.path.join(self.tmpDir, "*.jpg")):
	    try:
		image = face_recognition.load_image_file(f)
	    except IOError as e:
		print "cannot open {0} becuase {1}".format(f, e)
		continue
	    try:
		faceDescriptor = face_recognition.face_encodings(image)
	    except IndexError as e:
		print "cannot generate vectors for {0} becuase {1}".format(f, e)
		continue
            if len(faceDescriptor) != 0:
                print "found a face in {0}".format(f)
                for faceName, faceVector in self.faceDb.iteritems():
                    output =  face_recognition.compare_faces(faceVector , faceDescriptor)
                    if True in output:
                        print faceName
                        if faceName in matches:
                            matches[faceName].append(self.getFrameNumber(f))
                        else:
                            matches[faceName] = [self.getFrameNumber(f)]
        return matches



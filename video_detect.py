#!/usr/bin/python

# Unpack a video into a number of screen grabs
# Iterrogate those screen grabs for faces
# Check those faces against a list of known people
#
import pickle
import subprocess

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


    def unpackVideo(self, filename, tmpDir = None):
        '''Takes a filename (path) and
        uses ffmpeg to extract frames to tmpDir
        '''
        returnCode = subprocess.call('ffmpeg -i {0} -vf "select=not(mod(n\,{1}))" -vsync vfr -q:v 2 {2}faces_%03d.jpg'.format(filename, self.screenGrabInterval, tmpDir), shell=True)
        if returnCode != 0:
            print "error, FFMPEG extraction failed. see STDOut"
            return False
    def detectFaces(self):
        '''Go through the tempDir and pull out all the faces
        and then compare them to a known list
        '''

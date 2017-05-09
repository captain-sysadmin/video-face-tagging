# video-face-tagging
Source, tag and store face vectors

# what does it do?
Based heavily on the dlib library, it generates 128 dimension vectors for any face it sees. These vectors can then be compared against each other to provide a primitive facial recognition system

# Whats provided
There are a number of scripts: 

1) download_faces.py Uses the 6 degrees of merkel to generate a list of VIPs. It then talks to bing to find 5 pictures of each person
2) build_face_vetors.py Goes through a directory generated by the previous script and builds a 128D vector for each person. 
3) video_detect.py provides a library that wraps FFMPEG to unpack a video and inspect every n frame for known faces. Returns a dict of faces and frames.

However sadly, this model is not all that acurate. There are lots of false positive, especailly for female leaders. 

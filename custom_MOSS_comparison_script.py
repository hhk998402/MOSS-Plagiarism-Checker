from pathlib import Path
import pickle
import mosspy
userid = 238197006

m = mosspy.Moss(userid, "python")

homeDir = "Machine_Learning_Git_Submissions"

with open('folderMapper.pkl', 'rb') as f:
    folderMapper = pickle.load(f)

m.addFile(str(Path(homeDir, "Nimish Bongale", folderMapper["Nimish Bongale"])) + "/mlp.py")
m.addFile(str(Path(homeDir, "Vibhavari", folderMapper["Vibhavari"])) + "/mlp.py")

url = m.send() # Submission Report URL

print ("Report Url: " + url)
import argparse
import re

# construct the arument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
    help="path to iBug 300-W data split XML file")
ap.add_argument("-t", "--output", required=True,
    help="path to output data split XML file")
args = vars(ap.parse_args())


# in the IBUG 300-W dataset, each (x,y)-cooredinate maps to a specific
# facial feature (i.e., eye, mouth, nose, etc.) -- in order to train a 
# dlib shape predictor on *just* the eyse, we must first define the
# integer index that belong to the eyes
LANDMARKS = set(list(range(27, 35))+list(range(48, 68)))        # for eyes only (change for mouth)

# to easily parse out the eye locations from the XML file we can
# utilize regular expression to germine if there is a 'part'
# element on any  given line
PART = re.compile("part name='[0-9]+'")

# load the contents of the original XML file and open the output file
# for writing 
print("[INFO] parsing data split XML file...")
rows = open(args["input"]).read().strip().split("\n")
output = open(args["output"], "w")

# loop over the rows of the data split file
for row in rows:
    # check to see if the current line ha the (x,y)-coordinates for 
    # the facial landmarks we are interested in 
    parts = re.findall(PART, row)

    # if there is no information related to the (x,y)-coordinates of
    # the facial landmarks, we can write the current line out to disk 
    # with no further modifications
    if len(parts) == 0:
        output.write("{}\n".format(row))
    
    # otherwise, there is annotation information that we must process
    else:
        # parse out the name of the attribute fro the row
        attr = "name='"
        i = row.find(attr)
        j = row.find("'", i + len(attr) + 1)
        name = int(row[i + len(attr):j])

        # if the facial landmark name exists within the range of our
        # indexes, write it to our output file
        if name in LANDMARKS:
            output.write("{}\n".format(row))

# close the output file
output.close()


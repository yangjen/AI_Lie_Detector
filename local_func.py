import time
import math
import os


path = "local_results"


def write_file(filename,array):
    fil = open(filename,'w')
    for item in array:
        fil.write(item + "\r\n")
    fil.close()

    return


def local_save(session_id,log_affdex,log_xlabs,log_events,questions):
    if not os.path.exists(os.path.join(os.getcwd(),path)):
        os.makedirs(os.path.join(os.getcwd(),path))

    write_file(os.path.join(os.getcwd(),path,session_id+"_"+"log_affdex.txt"),log_affdex)
    write_file(os.path.join(os.getcwd(),path,session_id+"_"+"log_xlabs.txt"),log_xlabs)
    write_file(os.path.join(os.getcwd(),path,session_id+"_"+"log_events.txt"),log_events)
    write_file(os.path.join(os.getcwd(),path,session_id+"_"+"log_questions.txt"),questions)

    return


def local_save_truth(session_id,ground_truth):
    filepath = os.path.join(os.getcwd(),path,session_id+"_"+"log_questions.txt")

    fil = open(filepath,'r')
    lector = fil.readlines()
    fil.close()

    j = 0
    questions = []
    for i in range(len(lector)):
        # Remove the nextline character
        lector[i] = lector[i][:-1]

        # Check that it is not empty
        if len(lector[i]) == 0:
            continue

        j += 1
        if (ground_truth == str(j)):
            value = "1"
        else:
            value = "0"

        # Append the true value to the question
        questions.append(lector[i]+" "+value)

    # Re-Write the file
    write_file(filepath, questions)

    return

import time,math,os

def write_file(filename,array):
    fil = open(filename,'w')
    for item in array:
        fil.write(item + "\r\n")
    fil.close()
    return

def local_save(questions,log_affdex,log_xlabs,log_events):
    path = "local_results"
    if not os.path.exists(os.path.join(os.getcwd(),path)):
        os.makedirs(os.path.join(os.getcwd(),path))
    idd = math.floor(time.time())

    write_file(os.path.join(os.getcwd(),path,str(idd)+"_"+"log_questions.txt"),questions)
    write_file(os.path.join(os.getcwd(),path,str(idd)+"_"+"log_affdex.txt"),log_affdex)
    write_file(os.path.join(os.getcwd(),path,str(idd)+"_"+"log_xlabs.txt"),log_xlabs)
    write_file(os.path.join(os.getcwd(),path,str(idd)+"_"+"log_events.txt"),log_events)

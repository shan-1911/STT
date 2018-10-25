import speech_recognition as sr
import csv
import os
import pydub
import subprocess
from subprocess import call
from subprocess import check_output
import re
import pandas as pd
import math


reftxt = r'/home/tony/speech/pda/audios/test/ref.txt'
hyptxt= r'/home/tony/speech/pda/audios/test/hyp.txt'
TEXTFILE = r'/home/tony/speech/output/outputfile.txt'
SOURCE = r'/home/tony/speech/mp3test'
reftxt = r'/home/tony/speech/pda/audios/test/ref.txt'
hyptxt= r'/home/tony/speech/pda/audios/test/hyp.txt'
DIRNAME = r'/home/tony/speech/noise_reduction/old'
OUTPUTFILE = r'/home/tony/speech/output/outputfile_google.csv'
REFFILE = r'/home/tony/speech/wer_ref.csv'
BING_KEY = "41e2e4802ca44c5e88423a6ce22f8381"
HOUNDIFY_CLIENT_ID = "YJRTv6Lx1G6D-hnL5CAgOw=="  # Houndify client IDs are Base64-encoded strings
HOUNDIFY_CLIENT_KEY = "-smnwMoRqMu5j2snwWKjhmq1qddLNBiRxDbLYpMla78banKiqXBq2lDa-_gwyasErhq4srA5-4LiCffHC-Yr_A=="  # Houndify client keys are Base64-encoded strings
IBM_USERNAME = "f1a9cde6-84ee-427b-9595-674df7f437fd"  # IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
IBM_PASSWORD = "OeSE2XzayIXH"  # IBM Speech to Text passwords are mixed-case alphanumeric strings
WIT_AI_KEY = "6TECMQEZ2TMIZAPTJHDA4JTAA4YGHQUB"  # Wit.ai keys are 32-character uppercase alphanumeric strings
DEL_PENALTY=1
INS_PENALTY=1
SUB_PENALTY=1

def wer(ref,hyp):
	if(str(hyp)=="nan"):
	#if math.isnan(float(hyp)):
		return 1	
	with open(reftxt,'w') as my_data:
            	my_data.write(ref)
	with open(hyptxt,'w') as my_data:
            	my_data.write(hyp)
	a=check_output(["wer" ,reftxt, hyptxt])
    	n=re.search('WER:    (.+?)% ',a)
	if n:
    		found = n.group(1)
    		return (float(found)/100.0000)
	n2=re.search('WER:   100.000% ',a)
	if n2:
    		return 1

def get_file_paths(dirname):
    file_paths = []
    for root, directories, files in os.walk(dirname):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    return file_paths

def recog_google(file):
    r = sr.Recognizer()
    a = ''
    result=[]
    with sr.AudioFile(file) as source:
        audio = r.record(source)
        try:
            a =  r.recognize_google(audio)
        except sr.UnknownValueError:
            a = "Google Speech Recognition could not understand audio"
        except sr.RequestError as e:
            a = "Could not request results from Google Speech Recognition service; {0}".format(e)
        result=a
        return result


def recog_bing(file):
    r = sr.Recognizer()
    a = ''
    result=[]
    with sr.AudioFile(file) as source:
        audio = r.record(source)
        try:
            a =r.recognize_bing(audio, key=BING_KEY)
        except sr.UnknownValueError:
            a = "Microsoft Bing Voice Recognition could not understand audio"
        except sr.RequestError as e:
            a = "Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e)
        result=a
    return result
def recog_houndify(file):
    r = sr.Recognizer()
    a = ''
    result=[]
    with sr.AudioFile(file) as source:
        audio = r.record(source)
        try:
            a =r.recognize_houndify(audio, client_id=HOUNDIFY_CLIENT_ID, client_key=HOUNDIFY_CLIENT_KEY)
        except sr.UnknownValueError:
            a = "Houndify Voice Recognition could not understand audio"
        except sr.RequestError as e:
            a = "Could not request results from Houndify Voice Recognition service; {0}".format(e)
        result=a
    return result

def recog_ibm(file):
    r = sr.Recognizer()
    a = ''
    result=[]
    with sr.AudioFile(file) as source:
        audio = r.record(source)
        try:
            a =r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD)
        except sr.UnknownValueError:
            a = "IBM Voice Recognition could not understand audio"
        except sr.RequestError as e:
            a = "Could not request results from IBM Voice Recognition service; {0}".format(e)
        result=a
    return result

def recog_wit(file):
    r = sr.Recognizer()
    a = ''
    result=[]
    with sr.AudioFile(file) as source:
        audio = r.record(source)
        try:
            a =  r.recognize_wit(audio, key=WIT_AI_KEY)
        except sr.UnknownValueError:
            e = "Wit.ai could not understand audio"
        except sr.RequestError as e:
            e = "Could not request results from Wit.ai service; {0}".format(e)
        result=a
        return result


def main():
	df = pd.read_csv(REFFILE)
	n_rows = len(df)
	reference=df.Text
	file_name=df.FileName
	a = df.Google
	b = df.IBM
	c = df.BING
	d = df.Houndify
	e = df.Nuance
	f = df.DeepSpeech
	g = df.WIT
	for i in range(n_rows):
		print(a[i])
		wer_a=wer(reference[i],b[i])
		print(wer_a)
    	#a=check_output(["wer" ,"/home/tony/speech/wer/ref.txt", "/home/tony/speech/wer/hyp.txt"])
    	


if __name__ == '__main__':
    main()

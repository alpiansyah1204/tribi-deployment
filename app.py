from flask import Flask,request,jsonify,render_template,send_file
# from camera import VideoCamera
import cv2
#import moviepy editor 
from moviepy.editor import *

# import StemmerFactory class
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory  

app = Flask(__name__)
# video_stream = VideoCamera()

list_animation = ["me","masak","apa","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

def animation(word):
    video = []
    word_list = word.split()
    
    #load file
    for i in word:
        if (i in list_animation):
            i.upper()
            video.append(VideoFileClip(fr'video\{i}.mp4'))
        elif(i == " "):
            video.append(VideoFileClip(fr'video\idle.mp4'))
    # # join and write 
    result = concatenate_videoclips(video)
    result.write_videofile('combined.mp4',20)

def hasil(word):
    # stemmer
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    # stemming process
    sentence = word
    output   = stemmer.stem(sentence)
    sentence =list(sentence.lower().split())
    output = list(output.lower().split())
    print(f"{sentence}  {len(sentence)}")
    print(f"{output}  {len(output)}")

    hasil = []
    imbuhan = ['ter', 'te', 'se', 'per', 'peng', 
               'pen', 'pem', 'pe', 'men', 'mem', 
               'me', 'ke', 'di', 'ber', 'be']

    # print(imbuhan)
    for i in range(len(sentence)):
        word = sentence[i]
        if (output[i]!= word):
            for j in imbuhan:
                if word.startswith(j):
                    c = word[:len(j)]
                    # print(c)
                    hasil.append(j)
                    hasil.append(output[i])
                    break
        else:
            hasil.append(output[i])
    
    print(hasil)
    return hasil


@app.route('/animasi',methods= ['GET'])
def animasi():
    word = request.form['word']
    seperate = hasil(word)
    result =' '.join(map(str, seperate))
    animation(result)
    return send_file('combined.mp4')

@app.route('/')
def index():
    return 'hello world '

if __name__ == '__main__':
    app.run(debug=True) 
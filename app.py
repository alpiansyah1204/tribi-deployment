from flask import Flask,request,send_file
# from camera import VideoCamera

from moviepy.editor import *
# import StemmerFactory class
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

    
app = Flask(__name__)
# video_stream = VideoCamera()

imbuhan = ['ter', 'te', 'se', 'per', 'peng', 
               'pen', 'pem', 'pe', 'men', 'mem', 
               'me', 'ke', 'di', 'ber', 'be']
list_animation = ["me","masak","apa","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

factory = StemmerFactory()
stemmer = factory.create_stemmer()


def animation(word):
    video = [ VideoFileClip(f"video\{i.upper()}.mp4") for i in word]
    # # join and write 
    result = concatenate_videoclips(video)
    result.write_videofile('combined.mp4',20)


def textToAnimation(word_sequence):
    # print(word_sequence)
    wordToAnimation = []
    for i in word_sequence:
        if i in list_animation:
            wordToAnimation.append(i)
            wordToAnimation.append('idle')
        elif i not in list_animation :
            for j in i :
                if j in list_animation:
                    wordToAnimation.append(j)
                elif j not in list_animation:
                    error = 'data tidak ditemukan'
                    return error
            wordToAnimation.append('idle')
    # print(wordToAnimation)
    return wordToAnimation

def trimKataImbuhan(word):
    li_stem = list(stemmer.stem(word).split(" "))     
    li = list(word.split(" "))
    
    # print(li)
    word_sequence = []

    for i in range(len(li)):
        if li[i] == li_stem[i]:
            word_sequence.append(li[i])
        elif li[i] != li_stem[i]:
            for j in imbuhan:
                if li[i].startswith(j):
                    word_sequence.append(j)
                    word_sequence.append(li_stem[i])
                break
    # print(word_sequence)
    return(word_sequence)
    # textToAnimation(word_sequence)
   
@app.route('/animasi',methods= ['GET'])
def animasi():
    word = request.form['word'] 
    trim = trimKataImbuhan(word)
    textanimasi = textToAnimation(trim)
    animation(textanimasi)    
    return send_file('combined.mp4')

@app.route('/')
def index():
    return 'hello world '

if __name__ == '__main__':
    app.run(debug=True) 
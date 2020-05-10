from gtts import gTTS
import pyglet
import PyPDF2
from io import BytesIO
import pygame
import sys

pygame.init()


#################################Speak_with_Save###############################################


def save_text_as_sound(text, file_name):
    tts = gTTS(text=text, lang="en")
    tts.save(file_name)


def play_from_save(file_name):
    music = pyglet.resource.media(file_name)
    music.play()
    pyglet.app.run()


def speak_with_save(text):
    file_name = "voice.mp3"
    save_text_as_sound(text, file_name)
    play_from_save(file_name)


def pdf_to_sound_save(filename):
    pdfFileObj = open(filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    num_pages = pdfReader.numPages
    final_text = ""
    for i in range(num_pages):
        final_text += text_extract_one_page(i, pdfReader)
    final_text.replace("\n", "")
    speak_with_save(final_text)


#################################Speak_without_Save###############################################


def pdf_to_sound(filename):
    pdfFileObj = open(filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    num_pages = pdfReader.numPages
    for i in range(num_pages):
        text = text_extract_one_page(i, pdfReader)
        sentence_list = text_fragmentation(text)
        for i in sentence_list:
            speak_without_save(text)


def text_fragmentation(text):
    text = text.replace("\n", "")
    sentence_list = text.split(". ")
    return sentence_list


def text_extract_one_page(page_num, pdfReader):
    num_pages = pdfReader.numPages
    text = ""
    if page_num >= num_pages:
        print("Page num error")
    else:
        pageObj = pdfReader.getPage(page_num)
        text += pageObj.extractText()
    return text


def speak_without_save(text):
    tts = gTTS(text=text, lang='en')
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    pygame.mixer.init()
    pygame.mixer.music.load(fp)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def help():
    print("----------------------------------------------------------")
    print("--------------------The Professor-------------------------")
    print("----------------------------------------------------------")
    print("usage: main.py [pdf_path] [<blank>|--save]")
    print("$[main.py input.pdf --save]  : Save sound as mp3 ")
    print("$[main.py input.pdf ]        : Play as sound text of pdf")
    print("----------------------------------------------------------")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        help()
    else:
        if len(sys.argv) > 2:
            if str(sys.argv[2]) == "--save":
                speak_with_save("a")
            else:
                help()
        else:
            pdf_to_sound(str(sys.argv[1]))

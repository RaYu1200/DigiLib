import boto3
from PIL import Image
import pytesseract
import numpy as np
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
import yake
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
import aspose.words as aw
import os
pwd = os.path.dirname(__file__)
import moviepy.editor as mp
import speech_recognition as sr

# def getImageKeywords(file):
#     keywords = []
#     pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
#     img1 = np.array(Image.open(file))
#     text = pytesseract.image_to_string(img1)
#     total_words = text.split()
#     total_word_length = len(total_words)

#     language = "en"
#     numOfKeywords = int(total_word_length*0.15)
#     text_keywords = []
#     kw_extractor = yake.KeywordExtractor(stopwords = stop_words, n=1, top = numOfKeywords )
#     keywords = kw_extractor.extract_keywords(text)
#     for kw in keywords:
#         text_keywords.append(kw[0])

#     # path = "files"
#     # dir_list = os.listdir(path)
#     # # print(len(dir_list))
#     # for file in dir_list:
#     #     filename = file.split(".")
#     filename = file.split(".")
#     image_metadata = {}
#     image_metadata['text_keywords'] = text_keywords
#     image_metadata['filename'] = filename
#     if(filename.pop() == 'jpg'):
#         image = Image.open(file)
#         exifdata = image.getexif()
#         for tag_id in exifdata:
#             tag = TAGS.get(tag_id, tag_id)
#             data = exifdata.get(tag_id)
#             if isinstance(data, bytes):
#                 data = data.decode()
#             if(tag == 'DateTime'):
#                 image_metadata['DateTime'] = data
#             if(tag=='ImageDescription'):
#                 image_metadata['description'] = data
#     return image_metadata

# def getAudioKeywords(file):
#     import os
#     video_file = file
#     video_clip = mp.VideoFileClip(video_file)
#     audio = video_clip.audio
#     temp_audio_file = "temp_audio.wav"
#     audio.write_audiofile(temp_audio_file)
#     recognizer = sr.Recognizer()
#     recognizer.energy_threshold = 4000  
#     with sr.AudioFile(temp_audio_file) as source:
#         audio_data = recognizer.record(source)
#         try:
#             text = recognizer.recognize_sphinx(audio_data)
#             print("Extracted Text: " + text)
#         except sr.UnknownValueError:
#             print("Could not understand audio")
#         except sr.RequestError as e:
#             print(f"Recognition error; {e}")

#     os.remove(temp_audio_file)

#     audio_keywords = []
#     total_words = text.split()
#     total_word_length = len(total_words)
#     numOfKeywords = int(total_word_length*0.15)
#     kw_extractor = yake.KeywordExtractor(stopwords = stop_words, n=1, top = numOfKeywords)
#     keywords = kw_extractor.extract_keywords(text)
#     for kw in keywords:
#         audio_keywords.append(kw)
#     return audio_keywords


def getDocKeywords(file):
    doc = aw.Document(file)
    doc.save("doc-to-text.txt")
    f = open("doc-to-text.txt", "r")
    text = f.read()
    f.close()
    total_words = text.split()
    total_word_length = len(total_words)
    numOfKeywords = int(total_word_length*0.05)
    kw_extractor = yake.KeywordExtractor(stopwords = stop_words, n=1, top=numOfKeywords)
    keywords = kw_extractor.extract_keywords(text)
    docs_keywords = []
    for kw in keywords:
        docs_keywords.append(kw[0])
    os.remove("doc-to-text.txt")
    return docs_keywords

@api_view(['POST'])
def upload_to_s3(request):
    file = request.FILES['file']
    uploadedAt = request.data['uploadedAt']
    keyWords = request.data['keyWords']
    keyWords = list(keyWords.split(","))
    try:
        file_name = file.name
        extension = file_name.rsplit(".",1)[-1]
        if extension == 'doc':
            docKeywords = getDocKeywords(file_name)
            keyWords += docKeywords
        # elif extension == 'jpg':
            # imageKeywords = getImageKeywords(file_name)
            # print(imageKeywords)
            # keywords += imageKeywords
        # elif extension == 'mp4':
        #     with open(file_name, 'wb+') as f:
        #         for chunk in file.chunks():
        #             f.write(chunk)
        # audioKeywords = getAudioKeywords(file_name)
        

        s3 = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        s3.upload_fileobj(file, settings.AWS_STORAGE_BUCKET_NAME, file.name)
        s3Url = f'https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{file.name}'
        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        table = dynamodb.Table('DRM')
        response = table.put_item(
            Item = {
                'fileName': file.name,
                's3Url': s3Url,
                'uploadedAt': uploadedAt,
                'keyWords': keyWords
            }
        )
        return Response({
            'success': True,
            'metaData': response,
            'message': 'File uploaded successfully'
        })
    except Exception as e:
        return Response({
            'success': False, 
            'message': str(e)
        })

@api_view(['GET'])
def searchFile(request):
    try:
        searchText = request.GET['searchText']
        dynamodb = boto3.client(
            'dynamodb',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        response = dynamodb.scan(
            TableName = 'DRM',
            FilterExpression = 'contains(keyWords, :value)',
            ExpressionAttributeValues = {
                ':value': {'S' : searchText}
            }
        )
        return Response({
            'success': False, 
            'metaData': response,
            'message': 'Data search completed successfully'
        })
    except Exception as e:
        return Response({
            'success': False, 
            'message': str(e)
        })
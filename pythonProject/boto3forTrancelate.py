# # This is a sample Python script.
#
# # Press ⌃R to execute it or replace it with your code.
# # Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
#
#
# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/


import boto3
import contextlib
import time
import uuid
import pprint

# t_obj = boto3.client('translate')
txt = '翻訳したい言語入れる'
# txt_en = 'I am studing at AIIT.'


def translateFnc():
    print("translateFnc()関数実施")
    t_obj = boto3.client('translate')

    t_out = t_obj.translate_text(
        Text=txt,
        # SourceLanguageCode='ja',
        # TargetLanguageCode='en'
        SourceLanguageCode='ja',
        TargetLanguageCode='en'
    )
    print("翻訳後")
    print(t_out)
    print(t_out['TranslatedText'])
    pollyFnc(t_out['TranslatedText'])

f_out = 's_out.mp3'
k_name = 's_out.mp3'
b_name = 'data.riosong.sk'


def pollyFnc(text):
 print("tpollyFnc()関数実施")
 p_obj = boto3.client('polly')
 p_out = p_obj.synthesize_speech(
  Text=text,
  OutputFormat='mp3',
  VoiceId='Joanna'
 )

 with contextlib.closing(p_out['AudioStream'])as a_stream:
    with open(f_out, 'wb')as file:
     file.write(a_stream.read())
     transcribeFnc()


def transcribeFnc():
    print("transcribeFnc()関数実施")
    s3_obj = boto3.resource('s3')
    b_obj = s3_obj.Bucket(b_name)
    b_obj.upload_file(f_out, k_name)

    t_obj = boto3.client('transcribe', 'ap-northeast-1')
    jobID = str(uuid.uuid1())
    t_out = t_obj.start_transcription_job(
     TranscriptionJobName=jobID,
     Media={'MediaFileUri': 's3://' + b_name + '/' + f_out},
     MediaFormat='mp3',
     LanguageCode='en-US'
    )
    pprint.pprint(t_out)

    while True:
     t_out = t_obj.get_transcription_job(TranscriptionJobName=jobID)
     status = t_out['TranscriptionJob']['TranscriptionJobStatus']
     if status != 'IN_PROGRESS':
      break
     time.sleep(5)
    pprint.pprint(t_out)

txt = 'クラウドサーバ構築特論の授業です。'
txt_en = 'I am studing at AIIT.'

def translateFnc():
t_obj = boto3.client('translate')
t_out = t_obj.translate_text(
Text=txt_en,
# SourceLanguageCode='ja',
# TargetLanguageCode='en'
SourceLanguageCode='en',
TargetLanguageCode='ja'
)
print(t_out)
print(t_out['TranslatedText'])

if __name__ == "__main__":
    translateFnc()

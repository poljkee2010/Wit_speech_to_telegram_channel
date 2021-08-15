from pydub import AudioSegment
from wit import Wit
from pydub.utils import make_chunks
from telethon import TelegramClient, sync
import time
import warnings
warnings.filterwarnings("ignore")

def split(filepath):
    myaudio = AudioSegment.from_mp3(filepath)
    chunk_length_ms = 15000  # pydub calculates in millisec
    chunks = make_chunks(myaudio, chunk_length_ms)  # Make chunks of one sec
    return chunks

def start_wit(filepath):
    client_wit = Wit(config.get("Settings", "WIT_ACCESS_TOKEN"))
    text = []
    for i, chunk in enumerate(split(filepath)):
        chunk_name = "{0}.mp3".format(i)
        # print("exporting", chunk_name)
        chunk.export(chunk_name, format="mp3")
        with open(chunk_name, 'rb') as f:
            resp = client_wit.speech(f, {'Content-Type': 'audio/mpeg3'})
            # time.sleep(2)
            text.append(resp['text'])
            # print(resp['text'])
    # print(text)
    # print('OK')
    return text

############################################################################################
# 1 вариант реализации для отправки сообщения в канал "Избранное"
def send_text_to_telegram():
    name = 'session_name'
    api_id = int(config.get("Settings", "api_id"))
    api_hash = config.get("Settings", "api_hash")
    channel_id = int(config.get("Settings", "channel_id"))

    client = TelegramClient(name, api_id, api_hash)
    client.start()
    for i, val in enumerate(start_wit(config.get("Settings", "PATH_MP3_FILE"))):
        client.send_message(channel_id, val)

def Config(path):
    """
    Чтение конфига
    :param path: путь к файлу конфигурации
    :return: параметры конфига
    """
    import configparser  # импортируем библиотеку
    config = configparser.ConfigParser()  # создаём объекта парсера
    config.read(path, encoding='utf-8')  # читаем конфиг
    return config

# Сборка .exe файла в один + иконка
# pyinstaller -F --icon=speech.ico main.py
if __name__ == '__main__':
    path = "config.ini"
    config = Config(path)

    start = 'Program for speech recognition and sending messages to a Telegram Bot; by Aleks Ananikyan, 2021\n' \
            '===============Menu===============\n' \
            'Список доступных действий в программе:\n' \
            'go    -- начало процесса распознавания аудио и отправка в телеграмм канал\n'
    print(start)

    while True:
        start = input()
        try:
            if start == 'go':
                send_text_to_telegram()
                print("Текст отправлен в телеграмм канал")
                # exit()
            else:
                print("Некорректная команда")
        except Exception as e:
            print(e)
            exit()
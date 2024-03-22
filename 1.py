import os
import time
import ffmpeg
from PIL import Image
import mutagen
from pydub import AudioSegment


# Основной класс определяющий основные матаданные медиафайла:
# имя, тип файла, вес, дата создания, дата изменения, владелец, уникальный идентификатор.
class MediaFile:
    uid = 1

    def __init__(self, name, filetype, weight=None, crdate=None, chdate=None, owner=None, uid=None):
        self.name = name
        self.filetype = filetype
        self.weight = os.stat(name).st_size
        self.crdate = time.ctime(os.stat(name).st_ctime)
        self.chdate = time.ctime(os.stat(name).st_mtime)
        self.owner = os.stat(name).st_uid
        self.uid += 1

    # Метод удаления
    def file_remove(self):
        os.remove(self.name)
        print(f'Файл: {self.name} был удален')


# Класс для изображений, в дополнении к основным методанным поределенным в классе MediaFile содержит:
# Разрешение и формат

class ImageFile(MediaFile):
    def __init__(self, name, filetype=None, weight=None, crdate=None, chdate=None, owner=None, uid=None):
        super().__init__(name, filetype, weight, crdate, chdate, owner, uid)
        self.solution = Image.open(name).size
        self.format = Image.open(name).format

    # Класс содержит метод конвертации файла в ЧБ спектр
    def conv(self):
        im = Image.open(self.name)
        new_name = self.name.lower().split('.')[0]
        format = self.name.lower().split('.')[1]
        print(new_name)
        im.show()
        rgb_im = im.convert("L")
        rgb_im.show()
        rgb_im.save((f"{new_name}_l.{format}"),
                    format='PNG',
                    quality=72,
                    optimize=True,
                    dpi=self.solution)
        print(f'Файл: {self.name} был сконвертирован в файл: {new_name}_l.{format}')

    # Класс содержит измененное описание вывода, которое позволяет вывести метаданные изображения
    def __str__(self):
        return (
            f'Метаданные файлаЖ'
            f'Файл: {self.name}\n'
            f'Тип: {self.filetype}\n'
            f'Вес: {self.weight}\n'
            f'Дата создания: {self.crdate}\n'
            f'Дата изменения: {self.chdate}\n'
            f'Владелец: {self.owner}\n'
            f'Разрещение: {self.solution}\n'
            f'Формат: {self.format}')


# Класс для видео, в дополнении к основным методанным поределенным в классе MediaFile содержит:
# Кодек и длинну видео
class VideoFile(MediaFile):
    def __init__(self, name, filetype, weight=None, crdate=None, chdate=None, owner=None, uid=None):
        super().__init__(name, filetype, weight, crdate, chdate, owner, uid)
        self.vmeta = ffmpeg.probe(self.name)
        self.codec = self.vmeta['streams'][0]['codec_name']
        self.len = self.vmeta['streams'][0]['duration']

    # Класс содержит метод, который разворачивает видео на 90 градусов относительно горизонта
    def v_conv(self):
        vid = self.name
        print(f"{vid}")
        print(ffmpeg.input(vid))
        my_vid_stream = ffmpeg.input(vid)
        new_name = self.name.lower().split('.')[0] + '_c'
        fformat = self.name.lower().split('.')[1]
        my_vid_stream = my_vid_stream.video.hflip().output(f'{new_name}.{fformat}')
        ffmpeg.run(my_vid_stream)
        print(f'Файл: {self.name} был сконвертирован в файл: {new_name}.{fformat}')

    # Класс содержит измененное описание вывода, которое позволяет вывести метаданные изображения
    def __str__(self):
        return (
            f'Метаданные файлаЖ'
            f'Файл: {self.name}\n'
            f'Тип: {self.filetype}\n'
            f'Вес: {self.weight}\n'
            f'Дата создания: {self.crdate}\n'
            f'Дата изменения: {self.chdate}\n'
            f'Владелец: {self.owner}\n'
            f'Длительность: {self.len}\n'
            f'Кодек: {self.codec}')


# Класс для аудио, в дополнении к основным методанным поределенным в классе MediaFile содержит:
# Длинну и битрейт
class AudioFile(MediaFile):
    def __init__(self, name, filetype, weight=None, crdate=None, chdate=None, owner=None, bitrate=None, len=None,
                 uid=None):
        super().__init__(name, filetype, weight, crdate, chdate, owner, uid)
        self.bitrate = mutagen.File(self.name).info.bitrate
        self.len = mutagen.File(self.name).info.length

    # Класс содержит метод, который реверсирует файл
    def rev_file(self):
        afile = self.name
        aname = self.name.lower().split('.')[0]
        aformat = self.name.lower().split('.')[1]
        print(afile, aformat)
        afile = AudioSegment.from_file(afile, aformat)
        new_afile = afile.reverse()
        new_afile.export(f"{aname}_r.{aformat}", format=aformat)
        print(f'Файл: {self.name} был сконвертирован в {aname}_r.{aformat}')

    # Класс содержит измененное описание вывода, которое позволяет вывести метаданные изображения
    def __str__(self):
        return (
            f'Метаданные файла:'
            f'Файл: {self.name}\n'
            f'Тип: {self.filetype}\n'
            f'Вес: {self.weight}\n'
            f'Дата создания: {self.crdate}\n'
            f'Дата изменения: {self.chdate}\n'
            f'Владелец: {self.owner}\n'
            f'Битрейт: {self.bitrate}\n'
            f'Длительность: {self.len}')


def checkfolder(dir_path):
    # Определяем и выводим тип файла
    # Словарь расширений файлов и их типов

    dirfiles = {}
    print(f'Перечень файлов в папке {dir_path}')
    count = 1
    for entry in os.scandir(dir_path):
        dirfiles.update({count: entry.path})
        print(f'{count} - {entry.path}')
        count += 1
    chfile = int(input('Введите номер файла:'))
    return dirfiles[chfile]


# функция определения типа файла по расширению
def chfiletype(name):
    # Словарь расширений файлов и их типов
    file_types = {
        '.jpg': 'изображение',
        '.jpeg': 'изображение',
        '.png': 'изображение',
        '.gif': 'изображение',
        '.mp3': 'аудио',
        '.wav': 'аудио',
        '.aac': 'аудио',
        '.mp4': 'видео',
        '.avi': 'видео',
        '.mov': 'видео',
        # Дополнительные расширения и типы файлов...
    }
    file_type = file_types.get('.' + name.lower().split('.')[-1], "неизвестный тип")
    return file_type


def main():
    # Указываем путь до папки, можно использовать input и попросить пользователя ввести путь вкручную
    dir_path = 'C:\examples'
    fpath = checkfolder(dir_path)
    chfile = MediaFile(fpath, chfiletype(fpath))

    #Логика, которая обеспечивает возможность выбрать файл и вызвать возможные функции, характерные для типа медиафайла.
    if chfile.filetype == 'изображение':
        selfile = ImageFile(chfile.name)
        print(selfile)
        todo = input('Введите:\n1 - для конвертации файла в Ч\Б\n2 - для удаления\n:')
        if todo == '1':
            selfile.conv()
        elif todo == '2':
            selfile.file_remove()
    elif chfile.filetype == 'аудио':
        selfile = AudioFile(fpath, chfiletype(fpath))
        print(selfile)
        todo = input('Введите:\n1 - для создания реверсивного файла\n2 - для удаления\n:')
        if todo == '1':
            selfile.rev_file()
        elif todo == '2':
            selfile.file_remove()
    elif chfile.filetype == 'видео':
        selfile = VideoFile(fpath, chfiletype(fpath))
        print(selfile)
        todo = input('Введите:\n1 - для поворота видеофайла на 90 градусов\n2 - для удаления\n:')
        if todo == '1':
            selfile.v_conv()
        elif todo == '2':
            selfile.file_remove()


main()

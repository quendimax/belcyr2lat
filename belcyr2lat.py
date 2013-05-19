#!/usr/bin/env python3

import argparse
import sys


cyrillic_alphabet = "абвгґдеёжзіїйклмнопрстуўфхцчшыьэюяАБВГҐДЕЁЖЗІЇЙКЛМНОПРСТУЎФХЦЧШЫЬЭЮЯ'’ʼ"
latin_alphabet = "abcćčdefghiïjklłmnńoprsśštuŭvyzźžABCĆČDEFGHIÏJKLŁMNŃOPRSŚŠTUŬVYZŹŽ"

# dla abrevijatur, šmatsłoŭnych nazvaŭ i inš.
spec_dictionary = {
}

# dla častak słovaŭ
dictionary = {
    1 : {
        'а': 'a',   'б': 'b',   'в': 'v',   'г': 'h',
        'ґ': 'g',   'д': 'd',   'е': 'je',  'ё': 'jo',
        'ж': 'ž',   'з': 'z',   'і': 'i',   'ї': 'ï',
        'й': 'j',   'к': 'k',   'л': 'ł',   'м': 'm',
        'н': 'n',   'о': 'o',   'п': 'p',   'р': 'r',
        'с': 's',   'т': 't',   'у': 'u',   'ў': 'ŭ',
        'ф': 'f',   'х': 'ch',  'ц': 'c',   'ч': 'č',
        'ш': 'š',   'ы': 'y',   'э': 'e',   'ю': 'ju',
        'я': 'ja'
    },

    2 : {
        'бе': 'bie',  'бё': 'bio',  'бю': 'biu',  'бя': 'bia',
        'ве': 'vie',  'вё': 'vio',  'вю': 'viu',  'вя': 'via',
        'ге': 'hie',  'гё': 'hio',  'гю': 'hiu',  'гя': 'hia',
        'ґе': 'gie',  'ґё': 'gio',  'ґю': 'giu',  'ґя': 'gia',
        'зе': 'zie',  'зё': 'zio',  'зю': 'ziu',  'зя': 'zia',  'зь': 'ź',
        'ке': 'kie',  'кё': 'kio',  'кю': 'kiu',  'кя': 'kia',
        'ле': 'le',   'лё': 'lo',   'лю': 'lu',   'ля': 'la',   'ль': 'l',   'лі': 'li',
        'ме': 'mie',  'мё': 'mio',  'мю': 'miu',  'мя': 'mia',  'мь': 'm',
        'не': 'nie',  'нё': 'nio',  'ню': 'niu',  'ня': 'nia',  'нь': 'ń',
        'пе': 'pie',  'пё': 'pio',  'пю': 'piu',  'пя': 'pia',  'пь': 'p',
        'се': 'sie',  'сё': 'sio',  'сю': 'siu',  'ся': 'sia',  'сь': 'ś',
        'фе': 'fie',  'фё': 'fio',  'фю': 'fiu',  'фя': 'fia',  'фь': 'f',
        'хе': 'chie', 'хё': 'chio', 'хю': 'chiu', 'хя': 'chia',
        'це': 'cie',  'цё': 'cio',  'цю': 'ciu',  'ця': 'cia',  'ць': 'ć',
        'бʼ': 'b',    "б'": 'b',    'б’': 'b',
        'вʼ': 'v',    "в'": 'v',    'в’': 'v',
        'гʼ': 'h',    "г'": 'h',    'г’': 'h',
        'ґʼ': 'g',    "ґ'": 'g',    'ґ’': 'g',
        'дʼ': 'd',    "д'": 'd',    'д’': 'd',
        'жʼ': 'ž',    "ж'": 'ž',    'ж’': 'ž',
        'зʼ': 'z',    "з'": 'z',    'з’': 'z',
        'кʼ': 'k',    "к'": 'k',    'к’': 'k',
        'лʼ': 'ł',    "л'": 'ł',    'л’': 'ł',
        'мʼ': 'm',    "м'": 'm',    'м’': 'm',
        'нʼ': 'n',    "н'": 'n',    'н’': 'n',
        'пʼ': 'p',    "п'": 'p',    'п’': 'p',
        'рʼ': 'r',    "р'": 'r',    'р’': 'r',
        'сʼ': 's',    "с'": 's',    'с’': 's',
        'тʼ': 't',    "т'": 't',    'т’': 't',
        'фʼ': 'f',    "ф'": 'f',    'ф’': 'f',
        'хʼ': 'ch',   "х'": 'ch',   'х’': 'ch',
        'цʼ': 'c',    "ц'": 'c',    'ц’': 'c',
        'чʼ': 'č',    "ч'": 'č',    'ч’': 'č',
        'шʼ': 'š',    "ш'": 'š',    'ш’': 'š',
        'кг': 'g'
    },

    3 : {
        'кге': 'gie',  'кгё': 'gio',  'кгю': 'giu',  'кгя': 'gia',  'кгь': 'g',
        'кгʼ': 'g',    "кг'": 'g',    'кг’': 'g',
    },

    7 : {
        'вікіпэд': 'wikiped'
    }
}


def translate(line):
    max_key_size = max(dictionary.keys())

    result = ''
    i = 0
    while i < len(line):
        max_word_size = len(line) - i
        translated = False
        key_word = ''

        for word_size in range(min(max_word_size, max_key_size), 0, -1):
            key_word = line[i : i + word_size]

            is_expression = True    # kali abapał key_word znachodziacca nia litarnyja znaki
            if i == 0 and i + word_size == len(line):
                is_expression = False
            elif i > 0 and i+word_size < len(line) and (line[i-1].isalpha() or line[i+word_size].isalpha()):
                is_expression = False
            elif i == 0 and line[i+word_size].isalpha():
                is_expression = False
            elif i + word_size == len(line) and line[i-1].isalpha():
                is_expression = False

            if is_expression:
                dic = spec_dictionary.get(word_size)
                if dic:
                    value_word = dic.get(key_word)
                    if value_word:
                        result += value_word
                        translated = True
                        i += len(key_word)
                        break

            norm_key_word = key_word.lower()
            dic = dictionary.get(word_size)
            if dic:
                value_word = dic.get(norm_key_word)
                if value_word:
                    if key_word.istitle():
                        value_word = value_word.title()
                    elif key_word.isupper():
                        value_word = value_word.upper()

                    result += value_word
                    translated = True
                    i += len(key_word)
                    break

        if not translated:
            result += key_word
            i += 1

    return result


def parseArguments():
    parser = argparse.ArgumentParser(description='Conventer of belarusian text from cyrillic to latin alphabet')
    parser.add_argument('input', metavar='FILENAME', nargs='?', default='-', help='input file name. If missing then reads from stdin')
    parser.add_argument('-o', '--output', default='-', metavar='FILENAME', help='output file name. If it don\'t enumerate then writes to stdout')
    parser.add_argument('--input-encoding', dest='incodec', default='utf8', metavar='CODEC', help='choose a codec for input stream (default utf8)')
    parser.add_argument('--output-encoding', dest='outcodec', default='utf8', metavar='CODEC', help='choose a codec for output stream (default utf8)')
    args = parser.parse_args()
    if args.input == '-':
        args.input = sys.stdin
    else:
        args.input = open(args.input, 'r', encoding=args.incodec)
    if args.output == '-':
        args.output = sys.stdout
    else:
        args.output = open(args.output, 'w', encoding=args.outcodec)
    return args


def main():
    args = parseArguments()
    for line in args.input:
        args.output.write(translate(line))


if __name__ == '__main__':
    main()

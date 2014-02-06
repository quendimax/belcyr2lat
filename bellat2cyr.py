#!/usr/bin/env python3

import argparse
import sys


cyrillic_alphabet = "абвгґдеёжзіїйклмнопрстуўфхцчшыьэюяАБВГҐДЕЁЖЗІЇЙКЛМНОПРСТУЎФХЦЧШЫЬЭЮЯ'’ʼ"
latin_alphabet = "abcćčdefghiïjklłmnńoprsśštuŭvwyzźžABCĆČDEFGHIÏJKLŁMNŃOPRSŚŠTUŬVWYZŹŽ"

# dla abrevijatur, šmatsłoŭnych nazvaŭ i inš.
spec_dictionary = {
}

# dla častak słovaŭ
dictionary = {
    1 : {
        'a': 'а',   'b': 'б',   'c': 'ц',   'ć': 'ць',
        'č': 'ч',   'd': 'д',   'e': 'э',   'f': 'ф',
        'g': 'ґ',   'h': 'г',   'i': 'і',   'ï': 'ї',
        'j': 'й',   'k': 'к',   'l': 'ль',  'ł': 'л',
        'm': 'м',   'n': 'н',   'ń': 'нь',  'o': 'о',
        'p': 'п',   'r': 'р',   's': 'с',   'ś': 'сь',
        'š': 'ш',   't': 'т',   'u': 'у',   'ŭ': 'ў',
        'v': 'в',   'w': 'в',   'y': 'ы',   'z': 'з',
        'ź': 'зь',  'ž': 'ж'
    },

    2 : {
        'ch': 'х',
        'cz': 'ч',
        'sz': 'ш',
        'ja': 'я',
        'je': 'е',
        'ji': 'і',
        'la': 'ля', 'le': 'ле', 'lo': 'лё', 'lu': 'лю', 'li': 'лі',
        'jo': 'ё',
        'ju': 'ю'
    },

    3 : {
        'bia': 'бя',   'bie': 'бе',   'bio': 'бё',   'biu': 'бю',
        'bja': 'бʼя',  'bje': 'бʼе',  'bjo': 'бʼё',  'bju': 'бʼю',
        'cia': 'ця',   'cie': 'це',   'cio': 'цё',   'ciu': 'цю',
        'cja': 'цʼя',  'cje': 'цʼе',  'cjo': 'цʼё',  'cju': 'цʼю',
        'dia': 'дя',   'die': 'де',   'dio': 'дё',   'diu': 'дю',
        'dja': 'дʼя',  'dje': 'дʼе',  'djo': 'дʼё',  'dju': 'дʼю',
        'fia': 'фя',   'fie': 'фе',   'fio': 'фё',   'fiu': 'фю',
        'fja': 'фʼя',  'fje': 'фʼе',  'fjo': 'фʼё',  'fju': 'фʼю',
        'gia': 'ґя',   'gie': 'ґе',   'gio': 'ґё',   'giu': 'ґю',
        'gja': 'ґʼя',  'gje': 'ґʼе',  'gjo': 'ґʼё',  'gju': 'ґʼю',
        'hia': 'гя',   'hie': 'ге',   'hio': 'гё',   'hiu': 'гю',
        'hja': 'гʼя',  'hje': 'гʼе',  'hjo': 'гʼё',  'hju': 'гʼю',
        'kia': 'кя',   'kie': 'ке',   'kio': 'кё',   'kiu': 'кю',
        'kja': 'кʼя',  'kje': 'кʼе',  'kjo': 'кʼё',  'kju': 'кʼю',
        'lja': 'лья',  'lje': 'лье',  'ljo': 'льё',  'lju': 'лью',
        'mia': 'мя',   'mie': 'ме',   'mio': 'мё',   'miu': 'мю',
        'mja': 'мʼя',  'mje': 'мʼе',  'mjo': 'мʼё',  'mju': 'мʼю',
        'nia': 'ня',   'nie': 'не',   'nio': 'нё',   'niu': 'ню',
        'nja': 'нʼя',  'nje': 'нʼе',  'njo': 'нʼё',  'nju': 'нʼю',
        'pia': 'пя',   'pie': 'пе',   'pio': 'пё',   'piu': 'пю',
        'pja': 'пʼя',  'pje': 'пʼе',  'pjo': 'пʼё',  'pju': 'пʼю',
        'ria': 'ря',   'rie': 'ре',   'rio': 'рё',   'riu': 'рю',
        'rja': 'рʼя',  'rje': 'рʼе',  'rjo': 'рʼё',  'rju': 'рʼю',
        'sia': 'ся',   'sie': 'се',   'sio': 'сё',   'siu': 'сю',
        'sja': 'сʼя',  'sje': 'сʼе',  'sjo': 'сʼё',  'sju': 'сʼю',
        'tja': 'тʼя',  'tje': 'тʼе',  'tjo': 'тʼё',  'tju': 'тʼю',
        'via': 'вя',   'vie': 'ве',   'vio': 'вё',   'viu': 'вю',
        'vja': 'вʼя',  'vje': 'вʼе',  'vjo': 'вʼё',  'vju': 'вʼю',
        'wia': 'вя',   'wie': 'ве',   'wio': 'вё',   'wiu': 'вю',
        'wja': 'вʼя',  'wje': 'вʼе',  'wjo': 'вʼё',  'wju': 'вʼю',
        'zia': 'зя',   'zie': 'зе',   'zio': 'зё',   'ziu': 'зю',
        'zja': 'зʼя',  'zje': 'зʼе',  'zjo': 'зʼё',  'zju': 'зʼю',
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

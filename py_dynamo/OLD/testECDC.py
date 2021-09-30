# This Python file uses the following encoding: utf-8
import re, sys
import sys
reload(sys)
sys.setdefaultencoding('utf8')

text = "Sàn Đáy bể"

print (text)
print(sys.stdout.encoding) # xem bộ Mã hóa mặc định #cp437

whitespace = ' \t\n\r\v\f'
ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'
ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ascii_letters = ascii_lowercase + ascii_uppercase
digits = '0123456789'
hexdigits = digits + 'abcdef' + 'ABCDEF'
octdigits = '01234567'
punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
printable = digits + ascii_letters + punctuation + whitespace
# print(printable)


dicStr = "{0}{1}{2}"

print(dicStr.format("{","123","}"))

doublequote = "\""
print(doublequote)
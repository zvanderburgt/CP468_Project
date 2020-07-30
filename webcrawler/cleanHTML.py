'''
This program will clean HTML files
runs through web crawler dataset
'''
import re


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    cleanr2 = re.compile('\{.*?\}')
    cleantext2 = re.sub(cleanr2, '', cleantext)
    cleanr3 = re.compile('\(.*?\)')
    cleantext3 = re.sub(cleanr3, '', cleantext2)
    return cleantext3


def main():
    print("HTML cleaner")
    inFile = open('Self-driving car - Wikipedia.txt',
                  'r',  encoding='utf8', errors="ignore")
    outFile = open('clean.txt', 'w', encoding='utf-8')
    data = inFile.read()
    cleanData = cleanhtml(data)
    outFile.write(cleanData)

    inFile.close()
    outFile.close()


main()

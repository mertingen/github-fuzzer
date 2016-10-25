# -*- coding:utf-8 -*-
#!/usr/local/bin/python
import argparse
import sys
import requests
import os

#kod parametre vermeden çalıştırılırsa açıklaması
description = """
    Github için kullanıcı adı isimlerini var olup, olmadığını kontrol eder.
    Twitter: @_mertsimsek
    Ornek: python github-fuzzer.py --url https://github.com/USERNAME --status 404 --wordlist /home/user/wordlist.txt
"""

#script parametreleri alınır.
parser = argparse.ArgumentParser("github-fuzzer", description)
parser.add_argument("--wordlist", "-w", help="wordlist dosya adresi, format:/home/user/wordlist.txt")
parser.add_argument("--url", "-u", help="url, format: https://www.github.com/USERNAME")
parser.add_argument("--status", "-s", help="bakılacak http kodu", default="404")
args = parser.parse_args()

#fuzzing yapan fonksiyon
def checking():
    #eğer url sonunda USERNAME yoksa uyarı veriyor.
    if not args.url.endswith("USERNAME"):
        print "Url formatı bu şekilde olmalı: http://www.example.com/USERNAME"
        exit(0)
    #USERNAME stringi çıkartılıyor, url alınıyor.
    url = args.url.split('USERNAME')[0]
    #İstenilen status code parametrelerden alınıyor.
    args.status = args.status.split(",")
    #wordlist satır satır okunuyor
    with open(args.wordlist, "r") as f:
        for line in f.readlines():
            line = line.strip()

            #bağlantı hatası olursa program sonlanıyor.
            try:
                req = requests.head("{}{}".format(url, line))
            except requests.exceptions.ConnectionError:
                print "Bağlantı Hatası..."
                exit(0)

            #eğer 404 yani kullanıcı adı bulunamazsa valid_names.txt dosyasına yazılıyor.
            if str(req.status_code) in args.status:
               sys.stdout.write('{} kullanıcı adı için boş alan bulundu :) -> valid_names.txt dosyasına yazıldı.\n'.format(line))
               with open("valid_names.txt", "a") as text_file:
                    text_file.write("{}\n".format(line))
            else:
                sys.stdout.write('{} kullanıcı adı için boş alan bulunamadı :( \n'.format(line))
            sys.stdout.flush()

#program çalıştırılıyor.
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print parser.print_help()
        exit(0)
    checking()

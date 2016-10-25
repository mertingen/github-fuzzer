# -*- coding:utf-8 -*-
#!/usr/local/bin/python
import argparse
import sys
import requests
import os

description = """
    Github için kullanıcı adı isimlerini var olup, olmadığını kontrol eder.
    Twitter: @_mertsimsek
    Ornek: python github-fuzzer.py --url https://github.com/USERNAME --status 404 --wordlist /home/user/wordlist.txt
"""

parser = argparse.ArgumentParser("github-fuzzer", description)
parser.add_argument("--wordlist", "-w", help="wordlist dosya adresi, format:/home/user/wordlist.txt")
parser.add_argument("--url", "-u", help="url, format: https://www.github.com/USERNAME")
parser.add_argument("--status", "-s", help="bakılacak http kodu", default="404")
args = parser.parse_args()

def checking():
    if not args.url.endswith("USERNAME"):
        print "Url formatı bu şekilde olmalı: http://www.example.com/USERNAME"
        exit(0)
    url = args.url.split('USERNAME')[0]
    args.status = args.status.split(",")
    with open(args.wordlist, "r") as f:
        for line in f.readlines():
            line = line.strip()

            try:
                req = requests.head("{}{}".format(url, line))
            except requests.exceptions.ConnectionError:
                print "Bağlantı Hatası..."
                exit(0)

            if str(req.status_code) in args.status:
               sys.stdout.write('{} kullanıcı adı için boş alan bulundu :) -> valid_names.txt dosyasına yazıldı.\n'.format(line))
               with open("valid_names.txt", "a") as text_file:
                    text_file.write("{}\n".format(line))
            else:
                sys.stdout.write('{} kullanıcı adı için boş alan bulunamadı :( \n'.format(line))
            sys.stdout.flush()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print parser.print_help()
        exit(0)
    checking()

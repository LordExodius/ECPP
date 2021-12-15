#!/bin/bash
inotifywait -m /home/oscar/www/photobook |
while read; do
	python3 /home/oscar/www/photobook/updateNames.py
done
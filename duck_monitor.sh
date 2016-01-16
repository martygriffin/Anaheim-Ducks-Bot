#!/bin/bash
until python -u ./posting_bot.py > log.txt &; do
    echo "'duck bot' crashed with exit code $?. Restarting..." >&2
    sleep 300
done
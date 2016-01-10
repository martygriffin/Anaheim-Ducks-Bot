#!/bin/bash
until python ./posting_bot.py; do
    echo "'duck bot' crashed with exit code $?. Restarting..." >&2
    sleep 300
done
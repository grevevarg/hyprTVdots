#!/usr/bin/env bash

python3 "$(pwd)/bin/create_webapp_automated.py" "--app-name=Youtube --app-url=https://www.youtube.com/tv"
python3 "$(pwd)/bin/create_webapp_automated.py" "--app-name=YoutubeMusic --app-url=https://music.youtube.com"
python3 "$(pwd)/bin/create_webapp_automated.py" "--app-name=Twitch --app-url=https://www.twitch.tv"

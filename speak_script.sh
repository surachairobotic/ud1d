#!/bin/bash
say() { local IFS=+; C:/Program Files/VideoLAN/VLC/vlc.exe --play-and-exit "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=th"; }
say $*

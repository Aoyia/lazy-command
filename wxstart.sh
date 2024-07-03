#!/bin/bash
cd /Users/neoyuan/Desktop/aoyi/github-source-code/md/dist
source ~/.zshrc
# npm install -g http-server
pkill -f http-server
http-server -p 8844 &
sleep 3
open http://localhost:8844

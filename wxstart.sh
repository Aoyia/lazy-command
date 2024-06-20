#!/bin/bash
cd /Users/neoyuan/Desktop/aoyi/github-source-code/md/dist
# npm install -g http-server
http-server -p 8844 &
sleep 1
open http://localhost:8844

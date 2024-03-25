#!/bin/sh

if [[ $PWD == *'define'* ]]; then
  fnm use 14
  echo -e '\033[32mNode.js 版本已切换到 14\033[0m'
else
  fnm use 18
fi

#!/usr/bin/env bash
# $1=%DIR%, $2=%OUTDIR%, $3=%DOCFILE%
echo $1; echo $2; echo $3
NAME=$(echo $1 | rev | cut -d '/' -f-1 | rev)
cp "$2/$3.pdf" "$1/$NAME.pdf"
cp "$2/$3.synctex.gz" "$1/$NAME.synctex.gz"
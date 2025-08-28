#!/bin/sh

# Decrypt the file
# --batch to prevent interactive command
# --yes to assume "yes" for questions
# --pinentry-mode loopback to avoid ioctl issues in CI
export GPG_TTY=$(tty)
gpg --quiet --batch --yes --pinentry-mode loopback --passphrase="$LINK_PASSPHRASE" --decrypt --output links links.gpg

mkdir processing

python -m pip install --user requests
python download_links.py

cd processing
ls | xargs -n 1 gpg -e -f ../tiles.asc
mkdir -p ../automatic
mv *.gpg ../automatic

cd ../

rm -r processing
rm links
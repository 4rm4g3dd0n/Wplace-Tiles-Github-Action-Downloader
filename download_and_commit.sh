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
find . -name "*.png" -exec gpg -e -f ../tiles.asc {} \;
mkdir -p ../automatic
# Copy the entire folder structure with .gpg files to automatic, preserving directory structure
find . -name "*.gpg" | while read file; do
    # Create the directory structure in automatic
    dir=$(dirname "$file")
    mkdir -p "../automatic/$dir"
    # Move the file preserving the path
    mv "$file" "../automatic/$file"
done

cd ../

rm -r processing
rm links
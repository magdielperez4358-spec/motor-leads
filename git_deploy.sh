#!/data/data/com.termux/files/usr/bin/bash

pkg install git -y

git init
git add .

git config --global user.email "tu@email.com"
git config --global user.name "TuNombre"

git commit -m "Deploy automático"

git branch -M main
git remote add origin https://github.com/USUARIO/REPO.git
git push -u origin main

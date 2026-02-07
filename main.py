# 1. Instalar Git si no lo tienes
pkg install git -y

# 2. Inicializar y añadir archivos
git init
git add .

# 3. Configurar identidad (Solo si es la primera vez)
git config --global user.email "tu@email.com"
git config --global user.name "TuNombre"

# 4. Crear el commit
git commit -m "Deploy: Motor de Leads pipeline"

# 5. Conectar con tu repositorio de GitHub
# Sustituye USUARIO y REPO por los tuyos
git remote add origin https://github.com/USUARIO/REPO.git
git branch -M main

# 6. Subir archivos y disparar el APK Build
git push -u origin main


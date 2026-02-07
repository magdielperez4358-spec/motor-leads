#!/data/data/com.termux/files/usr/bin/bash

########################################
# CONFIG
########################################

PROJECT="$HOME/motor-leads"
DEST="/storage/emulated/0/MotorMakBackup"
LOG="$DEST/system.log"
MAIN="main.py"   # cambia si tu motor usa otro nombre
KEEP_DAYS=7
MAX_LOG=500000   # tamaño máximo del log en bytes

########################################
# PREPARACIÓN
########################################

mkdir -p "$DEST"

fecha=$(date +%Y-%m-%d_%H-%M-%S)

# rotar log si crece demasiado
if [ -f "$LOG" ] && [ $(stat -c%s "$LOG") -gt $MAX_LOG ]; then
  mv "$LOG" "$LOG.old"
fi

echo "===== [$fecha] SYSTEM RUN =====" >> "$LOG"

cd "$PROJECT" || {
  echo "ERROR: proyecto no encontrado" >> "$LOG"
  exit 1
}

########################################
# WATCHDOG INMORTAL
########################################

pgrep -f "$MAIN" > /dev/null

if [ $? -ne 0 ]; then
  echo "Motor caído — reiniciando" >> "$LOG"
  nohup python "$MAIN" >> "$LOG" 2>&1 &
else
  echo "Motor activo" >> "$LOG"
fi

########################################
# VERIFICACIÓN DE INTEGRIDAD
########################################

if [ ! -f "$MAIN" ]; then
  echo "ERROR CRÍTICO: archivo principal perdido" >> "$LOG"
  exit 1
fi

########################################
# BACKUP COMPRIMIDO NIVEL PRO
########################################

BACKUP_FILE="$DEST/motor-leads_$fecha.tar.gz"

tar --exclude='venv' -czf "$BACKUP_FILE" . 2>>"$LOG"

if [ $? -eq 0 ]; then
  echo "Backup OK: $BACKUP_FILE" >> "$LOG"
else
  echo "ERROR backup" >> "$LOG"
fi

########################################
# ROTACIÓN DE BACKUPS
########################################

find "$DEST" -name "motor-leads_*.tar.gz" -mtime +$KEEP_DAYS -delete
echo "Rotación completada" >> "$LOG"

########################################
# GIT AUTO SYNC
########################################

ping -c 1 github.com > /dev/null 2>&1

if [ $? -eq 0 ]; then
  git add . >> "$LOG" 2>&1
  git commit -m "auto backup $fecha" >> "$LOG" 2>&1
  git push >> "$LOG" 2>&1
  echo "Git OK" >> "$LOG"
else
  echo "Sin internet — git omitido" >> "$LOG"
fi

########################################
# NOTIFICACIÓN VISUAL
########################################

termux-toast "Sistema estable $fecha"

########################################
# FIN
########################################

echo "===== FIN =====" >> "$LOG"
echo "" >> "$LOG"

#!/bin/bash
# Gold Pack Engine v1.0 - Procesa leads + genera hooks + exporta CSV
# Autor: Mak | Fecha: 2026-02-08

# 1️⃣ Configuración de API
export GEMINI_KEY="AIzaSyCKsaXL91ZtwUimolp9kNh8tzQB0r8aM9w"

# 2️⃣ Archivo de leads de entrada (sqlite o CSV)
LEADS_DB="leads.db"
OUTPUT_CSV="ecommerce_goldpack_v1.csv"

# 3️⃣ Extraer los 50 leads top (SQLite)
echo "Extrayendo 50 leads de e-commerce..."
sqlite3 $LEADS_DB ".headers on" ".mode csv" "SELECT Company_Name, Store_URL, Primary_Email, Tech_Stack FROM leads WHERE industry='ecommerce' ORDER BY EFF_Score DESC LIMIT 50;" > leads_tmp.csv

# 4️⃣ Limpiar CSV de encabezados duplicados
tail -n +2 leads_tmp.csv > leads_clean.csv

# 5️⃣ Crear archivo final con encabezados extendidos
echo "Company_Name,Store_URL,Primary_Email,Tech_Stack,Target_Pain,Hook,Ad_Strategy" > $OUTPUT_CSV

# 6️⃣ Procesar cada lead con Gemini
echo "Generando hooks con Gemini..."
while IFS=',' read -r Company Store Email Tech
do
    # Comando curl para Gemini
    HOOK=$(curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=$GEMINI_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"contents\":[{\"parts\":[{\"text\":\"Genera un hook de venta de 10 palabras para un lead de ecommerce con 94% de eficiencia: $Company, $Tech\"}]}]}" \
    | jq -r '.candidates[0].content.parts[0].text')

    # Generar Pain Point y Ad Strategy (ejemplo simple, se puede enriquecer)
    PAIN="Abandono de carrito alto"
    AD="Usar campaña retargeting inmediata"

    # Agregar al CSV final
    echo "$Company,$Store,$Email,$Tech,$PAIN,\"$HOOK\",\"$AD\"" >> $OUTPUT_CSV
done < leads_clean.csv

# 7️⃣ Limpieza temporal
rm leads_tmp.csv leads_clean.csv

# 8️⃣ Resultado final
echo "✅ Gold Pack generado: $OUTPUT_CSV listo para Gumroad"

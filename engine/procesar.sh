#!/bin/bash
API_KEY="AIzaSyCKsaXL91ZtwUimolp9kNh8tzQB0r8aM9w"
OUTPUT="hooks_liquidados.csv"

echo "Iniciando procesamiento de bloques..."
# Simulación de lectura de leads del motor
for i in {1..5}; do
    echo "Procesando bloque $i..."
    RESPONSE=$(curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=$API_KEY" \
        -H "Content-Type: application/json" \
        -d '{"contents":[{"parts":[{"text":"Genera un hook de venta agresivo de 10 palabras para ecommerce"}]}]}')
    
    HOOK=$(echo $RESPONSE | jq -r '.candidates[0].content.parts[0].text')
    
    if [ "$HOOK" != "null" ]; then
        echo "$(date),Bloque_$i,$HOOK" >> $OUTPUT
        echo "✅ Éxito: Lead liquidado."
    else
        echo "❌ Error en bloque $i: Verificando response.json"
        echo $RESPONSE > error_log.json
    fi
    sleep 2 # Evitar throttling de Google
done
echo "Proceso finalizado. Archivo: $OUTPUT"

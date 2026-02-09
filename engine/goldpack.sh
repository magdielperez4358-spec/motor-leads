#!/bin/bash
# goldpack.sh - Generación automática de E-commerce Gold Pack v1.0

INPUT="leads_input.csv"
OUTPUT="ecommerce_goldpack_v1.csv"
API_KEY="AIzaSyCKsaXL91ZtwUimolp9kNh8tzQB0r8aM9w"

# Cabecera del CSV final
echo "Company_Name,Store_URL,Primary_Email,Tech_Stack,Validation_Timestamp,EFF_Score,Hook" > $OUTPUT

# Saltar la primera línea del CSV de entrada (cabecera)
tail -n +2 $INPUT | while IFS=',' read -r Company_Name Store_URL Primary_Email Tech_Stack Validation_Timestamp EFF_Score
do
    # Generar hook de venta usando Gemini
    HOOK=$(curl -s -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=$API_KEY" \
        -H "Content-Type: application/json" \
        -d "{\"contents\":[{\"parts\":[{\"text\":\"Genera un hook de venta de 10 palabras para un lead de ecommerce con eficiencia $EFF_Score\"}]}]}" \
        | jq -r '.candidates[0].content.parts[0].text')

    # Evitar null
    if [ "$HOOK" == "null" ] || [ -z "$HOOK" ]; then
        HOOK="Hook no generado"
    fi

    # Añadir fila al CSV de salida
    echo "$Company_Name,$Store_URL,$Primary_Email,$Tech_Stack,$Validation_Timestamp,$EFF_Score,\"$HOOK\"" >> $OUTPUT

    echo "✅ Lead procesado: $Company_Name"
done

echo "🎯 Gold Pack generado: $OUTPUT listo para Gumroad"

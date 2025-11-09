#!/bin/bash

echo "================================================"
echo "Servidor Django - Detección de Malware Android"
echo "================================================"
echo ""
echo "🔄 Iniciando servidor..."
echo ""
echo "⚠️  NOTA: La primera carga puede tardar 1-2 minutos"
echo "   mientras se procesan los datos y entrenan los modelos."
echo ""
echo "📊 El servidor procesará:"
echo "   - 632,000 registros del dataset CICAAGM"
echo "   - Entrenamiento de Random Forest Classifier"
echo "   - Entrenamiento de Random Forest Regressor"
echo ""
echo "🌐 Una vez iniciado, accede a:"
echo "   http://127.0.0.1:8000/"
echo ""
echo "================================================"
echo ""

cd "$(dirname "$0")"
python manage.py runserver


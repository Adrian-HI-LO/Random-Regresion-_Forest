#!/bin/bash
# Script para subir la nueva funcionalidad de configuración interactiva

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║   🎛️ SUBIENDO CONFIGURACIÓN INTERACTIVA                     ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# 1. Verificar cambios
echo "1️⃣  Verificando cambios..."
git status --short | head -20
echo ""

# 2. Agregar archivos
echo "2️⃣  Agregando archivos..."
git add analyzer/urls.py analyzer/views.py templates/configure.html templates/base.html CONFIGURACION_INTERACTIVA.txt
echo "✅ Archivos agregados"
echo ""

# 3. Commit
echo "3️⃣  Haciendo commit..."
git commit -m "Agregar configuración interactiva del dataset para el cliente final"
echo ""

# 4. Push
echo "4️⃣  Subiendo a GitHub..."
git push origin main
echo ""

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║                     ✅ COMPLETADO                            ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "🎉 NUEVA FUNCIONALIDAD IMPLEMENTADA:"
echo ""
echo "   El cliente final ahora puede:"
echo "   ✅ Configurar el tamaño del dataset desde la web"
echo "   ✅ Ver indicadores visuales de riesgo de memoria"
echo "   ✅ Reentrenar el modelo con un clic"
echo "   ✅ Ver métricas del nuevo modelo"
echo ""
echo "🌐 ACCESO:"
echo "   https://tu-app.onrender.com/configure/"
echo ""
echo "📍 EN EL MENÚ:"
echo "   Verás un nuevo botón: ⚙️ Configurar"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "📖 Para más detalles, lee: CONFIGURACION_INTERACTIVA.txt"
echo ""


# Servidor Django - Detección de Malware en Android

Sistema de análisis de malware en Android utilizando Random Forest Classifier y Regressor, con interfaz web oscura y minimalista.

## 🚀 Características

- **Random Forest Classifier**: Detección de malware con métricas de F1 Score, Precision, Recall y Accuracy
- **Random Forest Regressor**: Predicción de duración del tráfico de red con métricas R², RMSE, MAE y MSE
- **Procesamiento Independiente**: El servidor procesa los datos de forma independiente al notebook
- **Interfaz Oscura Minimalista**: Diseño moderno y limpio con tema oscuro
- **Visualización de Datos**: Tablas interactivas y métricas detalladas
- **API REST**: Endpoint JSON para obtener todas las métricas

## 📋 Requisitos

- Python 3.8+
- Dataset CICAAGM (incluido en `dataset/TotalFeatures-ISCXFlowMeter.csv`)

## 🔧 Instalación

1. **Clonar o navegar al directorio del proyecto:**
```bash
cd /home/adrian/Escritorio/Apis/RandomForestAndRegresor
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Ejecutar migraciones:**
```bash
python manage.py migrate
```

## 🎯 Uso

### Iniciar el servidor

```bash
python manage.py runserver
```

El servidor estará disponible en: `http://127.0.0.1:8000/`

### Rutas Disponibles

- **`/`** - Página de inicio con descripción del proyecto
- **`/dashboard/`** - Dashboard completo con todas las métricas
- **`/classification/`** - Análisis detallado de Random Forest Classifier
- **`/regression/`** - Análisis detallado de Random Forest Regressor
- **`/dataset/`** - Exploración del dataset CICAAGM
- **`/api/metrics/`** - API JSON con todas las métricas

## 📊 Métricas Disponibles

### Random Forest Classifier
- **F1 Score** (principal métrica de clasificación)
- Accuracy
- Precision
- Recall
- Matriz de Confusión
- Reporte de Clasificación
- Top 10 características más importantes

### Random Forest Regressor
- **R² Score** (coeficiente de determinación)
- RMSE (Root Mean Squared Error)
- MAE (Mean Absolute Error)
- MSE (Mean Squared Error)
- Top 10 características más importantes

Todas las métricas se muestran para los conjuntos de **entrenamiento**, **validación** y **test**.

## 🎨 Diseño

La interfaz utiliza un tema oscuro minimalista con:
- Colores suaves para reducir la fatiga visual
- Diseño responsive para diferentes tamaños de pantalla
- Tarjetas y tablas organizadas para fácil lectura
- Badges y colores para identificar rápidamente estados

## 📁 Estructura del Proyecto

```
RandomForestAndRegresor/
├── analyzer/                    # Aplicación Django principal
│   ├── ml_models.py            # Modelos de Machine Learning
│   ├── views.py                # Vistas del servidor
│   └── urls.py                 # Rutas de la aplicación
├── dataset/                     # Dataset CICAAGM
│   └── TotalFeatures-ISCXFlowMeter.csv
├── templates/                   # Templates HTML
│   ├── base.html               # Template base con estilos
│   ├── home.html               # Página de inicio
│   ├── dashboard.html          # Dashboard principal
│   ├── classification.html     # Vista de clasificación
│   ├── regression.html         # Vista de regresión
│   └── dataset.html            # Vista del dataset
├── malware_detector/           # Configuración de Django
│   ├── settings.py
│   └── urls.py
├── manage.py                    # Script de gestión de Django
└── requirements.txt            # Dependencias del proyecto
```

## 🔬 Sobre el Dataset

**CICAAGM Dataset** (Canadian Institute for Cybersecurity - Android Adware and General Malware)

- **Total de aplicaciones**: 1,900
  - Adware: 250 apps
  - General Malware: 150 apps
  - Benignas: 1,500 apps
- **Características**: 80 features extraídas del tráfico de red
- **Herramienta**: CIC-FlowMeter

### Categorías de Malware

**Adware:**
- Airpush
- Dowgin
- Kemoge
- Mobidash
- Shuanet

**General Malware:**
- AVpass
- FakeAV
- FakeFlash/FakePlayer
- GGtracker
- Penetho

## 🔗 Referencias

- Dataset: https://www.unb.ca/cic/datasets/android-adware.html
- Paper: Arash Habibi Lashkari et al., "Towards a Network-Based Framework for Android Malware Detection and Characterization", PST 2017

## ⚙️ Procesamiento de Datos

El servidor realiza el siguiente procesamiento:

1. **Carga del dataset** desde el archivo CSV
2. **Limpieza de datos**: manejo de valores infinitos y NaN
3. **División de datos**: 60% train, 20% validation, 20% test
4. **Escalado de características** (RobustScaler para clasificación)
5. **Entrenamiento de modelos** con 100 estimadores
6. **Cálculo de métricas** para todos los conjuntos
7. **Análisis de importancia** de características

## 🚀 Optimizaciones

- Los modelos se entrenan una sola vez al iniciar el servidor
- Se utiliza `n_jobs=-1` para aprovechar todos los núcleos del CPU
- Las vistas utilizan caché para mejorar el rendimiento
- Procesamiento independiente del notebook para evitar dependencias

## 📝 Notas

- La primera carga del servidor puede tardar unos minutos mientras procesa el dataset y entrena los modelos
- El dataset tiene ~632,000 registros con 80 características
- Los modelos utilizan Random Forest con 100 árboles de decisión
- El F1 Score es la métrica principal para clasificación
- El R² Score es la métrica principal para regresión

## 🐛 Solución de Problemas

Si el servidor no inicia:
1. Verifica que el dataset esté en `dataset/TotalFeatures-ISCXFlowMeter.csv`
2. Asegúrate de tener todas las dependencias instaladas
3. Ejecuta las migraciones: `python manage.py migrate`
4. Verifica que el puerto 8000 esté disponible

## 📜 Licencia

Este proyecto es independiente del notebook original y utiliza el dataset público CICAAGM.


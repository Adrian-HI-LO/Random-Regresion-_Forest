from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from .ml_models import MalwareAnalyzer
import os

# Instancia global del analizador
analyzer = None

def initialize_analyzer():
    """Inicializar el analizador si no existe"""
    global analyzer
    if analyzer is None:
        # Intentar usar el dataset local primero (para desarrollo)
        local_dataset_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'dataset',
            'TotalFeatures-ISCXFlowMeter.csv'
        )

        # Si existe el dataset local, usarlo; sino, descargar de Google Drive
        if os.path.exists(local_dataset_path):
            print("Usando dataset local...")
            analyzer = MalwareAnalyzer(dataset_path=local_dataset_path)
        else:
            print("Dataset local no encontrado. Descargando desde Google Drive...")
            # Intentar primero con file_id (más confiable), luego con folder_id
            file_id = getattr(settings, 'GDRIVE_FILE_ID', None)
            folder_id = getattr(settings, 'GDRIVE_FOLDER_ID', None)
            analyzer = MalwareAnalyzer(
                gdrive_file_id=file_id,
                gdrive_folder_id=folder_id
            )

        print("Iniciando análisis completo...")
        analyzer.run_full_analysis()
        print("✓ Análisis completo finalizado")
    return analyzer


def home(request):
    """Vista principal"""
    return render(request, 'home.html')


def dashboard(request):
    """Dashboard con todas las métricas"""
    analyzer_instance = initialize_analyzer()

    context = {
        'clf_metrics': analyzer_instance.clf_metrics,
        'reg_metrics': analyzer_instance.reg_metrics,
    }

    return render(request, 'dashboard.html', context)


def classification_view(request):
    """Vista de clasificación"""
    analyzer_instance = initialize_analyzer()

    context = {
        'metrics': analyzer_instance.clf_metrics,
        'feature_importance': analyzer_instance.get_feature_importance('classifier')[:10]
    }

    return render(request, 'classification.html', context)


def regression_view(request):
    """Vista de regresión"""
    analyzer_instance = initialize_analyzer()

    context = {
        'metrics': analyzer_instance.reg_metrics,
        'feature_importance': analyzer_instance.get_feature_importance('regressor')[:10]
    }

    return render(request, 'regression.html', context)


def dataset_view(request):
    """Vista del dataset"""
    analyzer_instance = initialize_analyzer()

    # Obtener primeras 100 filas
    df = analyzer_instance.df.head(100)

    # Convertir a formato para la tabla
    columns = df.columns.tolist()
    rows = df.values.tolist()

    # Estadísticas básicas
    stats = {
        'total_rows': len(analyzer_instance.df),
        'total_columns': len(analyzer_instance.df.columns),
        'malware_count': len(analyzer_instance.df[analyzer_instance.df['calss'] != 'benign']),
        'benign_count': len(analyzer_instance.df[analyzer_instance.df['calss'] == 'benign']),
    }

    context = {
        'columns': columns,
        'rows': rows,
        'stats': stats,
    }

    return render(request, 'dataset.html', context)


def api_metrics(request):
    """API endpoint para obtener métricas en JSON"""
    analyzer_instance = initialize_analyzer()

    data = {
        'classification': analyzer_instance.clf_metrics,
        'regression': analyzer_instance.reg_metrics,
    }

    return JsonResponse(data)


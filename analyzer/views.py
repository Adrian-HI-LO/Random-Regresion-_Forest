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

        # En producción (Render), usar subset para ahorrar memoria
        use_subset = os.environ.get('USE_DATASET_SUBSET', 'true').lower() == 'true'

        # Permitir configurar el tamaño del subset desde variable de entorno
        subset_size = int(os.environ.get('DATASET_SUBSET_SIZE', '50000'))

        # Si existe el dataset local, usarlo; sino, descargar de Google Drive
        if os.path.exists(local_dataset_path):
            print("Usando dataset local...")
            analyzer = MalwareAnalyzer(
                dataset_path=local_dataset_path,
                use_subset=use_subset,
                subset_size=subset_size
            )
        else:
            print("Dataset local no encontrado. Descargando desde Google Drive...")
            # Intentar primero con file_id (más confiable), luego con folder_id
            file_id = getattr(settings, 'GDRIVE_FILE_ID', None)
            folder_id = getattr(settings, 'GDRIVE_FOLDER_ID', None)

            analyzer = MalwareAnalyzer(
                gdrive_file_id=file_id,
                gdrive_folder_id=folder_id,
                use_subset=use_subset,
                subset_size=subset_size
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
        'dataset_info': {
            'using_subset': analyzer_instance.use_subset,
            'subset_size': analyzer_instance.subset_size,
            'full_dataset_size': 631955,
            'percentage_used': round((analyzer_instance.subset_size / 631955) * 100, 1) if analyzer_instance.use_subset else 100,
        }
    }

    return render(request, 'dashboard.html', context)


def classification_view(request):
    """Vista de clasificación"""
    analyzer_instance = initialize_analyzer()

    context = {
        'metrics': analyzer_instance.clf_metrics,
        'feature_importance': analyzer_instance.get_feature_importance('classifier')[:10],
        'dataset_info': {
            'using_subset': analyzer_instance.use_subset,
            'subset_size': analyzer_instance.subset_size,
            'full_dataset_size': 631955,
        }
    }

    return render(request, 'classification.html', context)


def regression_view(request):
    """Vista de regresión"""
    analyzer_instance = initialize_analyzer()

    context = {
        'metrics': analyzer_instance.reg_metrics,
        'feature_importance': analyzer_instance.get_feature_importance('regressor')[:10],
        'confusion_matrix': analyzer_instance.clf_metrics.get('test', {}).get('confusion_matrix', []),
        'dataset_info': {
            'using_subset': analyzer_instance.use_subset,
            'subset_size': analyzer_instance.subset_size,
            'full_dataset_size': 631955,
        }
    }

    return render(request, 'regression.html', context)


def dataset_view(request):
    """Vista del dataset"""
    analyzer_instance = initialize_analyzer()

    # Verificar si el dataframe fue eliminado para liberar memoria
    if analyzer_instance.df is None:
        # Recargar solo para mostrar (sin entrenar de nuevo)
        import pandas as pd
        import os

        dataset_path = analyzer_instance.dataset_path
        if dataset_path and os.path.exists(dataset_path):
            # Cargar solo 1000 filas para mostrar (muy ligero)
            df_sample = pd.read_csv(dataset_path, nrows=1000)

            # Obtener info del subset usado
            subset_size = analyzer_instance.subset_size if hasattr(analyzer_instance, 'subset_size') else 50000
            use_subset = analyzer_instance.use_subset

            # Estadísticas del subset usado para entrenamiento
            stats = {
                'total_rows': subset_size if use_subset else 631955,
                'total_columns': len(df_sample.columns),
                'malware_count': 'N/A',
                'benign_count': 'N/A',
                'using_subset': use_subset,
                'subset_size': subset_size if use_subset else 631955,
                'full_dataset_size': 631955,
            }

            # Mostrar primeras 100 filas
            df_display = df_sample.head(100)
            columns = df_display.columns.tolist()
            rows = df_display.values.tolist()
        else:
            # Fallback si no hay archivo
            stats = {
                'total_rows': 0,
                'total_columns': 0,
                'malware_count': 0,
                'benign_count': 0,
                'using_subset': True,
                'subset_size': 50000,
                'full_dataset_size': 631955,
            }
            columns = []
            rows = []
    else:
        # El dataframe aún existe en memoria
        df = analyzer_instance.df.head(100)
        columns = df.columns.tolist()
        rows = df.values.tolist()

        # Estadísticas básicas
        subset_size = analyzer_instance.subset_size if hasattr(analyzer_instance, 'subset_size') else len(analyzer_instance.df)
        use_subset = analyzer_instance.use_subset

        stats = {
            'total_rows': len(analyzer_instance.df),
            'total_columns': len(analyzer_instance.df.columns),
            'malware_count': len(analyzer_instance.df[analyzer_instance.df['calss'] != 'benign']),
            'benign_count': len(analyzer_instance.df[analyzer_instance.df['calss'] == 'benign']),
            'using_subset': use_subset,
            'subset_size': subset_size,
            'full_dataset_size': 631955,
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


def configure_model(request):
    """Vista para configurar el tamaño del dataset"""
    global analyzer

    # Obtener configuración actual
    current_size = analyzer.subset_size if analyzer else 50000
    using_subset = analyzer.use_subset if analyzer else True

    # Límites según memoria disponible (estimado)
    memory_limits = {
        'safe': 50000,      # Muy seguro para Free
        'moderate': 75000,  # Puede funcionar en Free
        'risky': 100000,    # Límite máximo Free
        'paid': 150000,     # Requiere plan pagado
    }

    # Calcular porcentaje
    percentage = round((current_size / 631955) * 100, 1)

    context = {
        'current_size': current_size,
        'percentage': percentage,
        'using_subset': using_subset,
        'full_dataset_size': 631955,
        'memory_limits': memory_limits,
        'is_trained': analyzer is not None,
    }

    return render(request, 'configure.html', context)


def retrain_model(request):
    """Reentrenar el modelo con nuevo tamaño de dataset"""
    global analyzer

    if request.method == 'POST':
        try:
            # Obtener nuevo tamaño del formulario
            new_size = int(request.POST.get('dataset_size', 50000))

            # Validar límites
            if new_size < 5000:
                return JsonResponse({
                    'success': False,
                    'error': 'El tamaño mínimo es 5,000 filas'
                })

            if new_size > 631955:
                return JsonResponse({
                    'success': False,
                    'error': 'El tamaño máximo es 631,955 filas (dataset completo)'
                })

            # Advertencia si es muy grande para Free
            warning = None
            if new_size > 100000:
                warning = 'Advertencia: Este tamaño puede causar errores de memoria en plan Free'

            # Reiniciar el analizador
            print(f"🔄 Reentrenando modelo con {new_size:,} filas...")

            analyzer = None  # Limpiar instancia anterior

            # Crear nuevo analizador con el tamaño especificado
            local_dataset_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'dataset',
                'TotalFeatures-ISCXFlowMeter.csv'
            )

            use_subset = new_size < 631955

            if os.path.exists(local_dataset_path):
                analyzer = MalwareAnalyzer(
                    dataset_path=local_dataset_path,
                    use_subset=use_subset,
                    subset_size=new_size
                )
            else:
                file_id = getattr(settings, 'GDRIVE_FILE_ID', None)
                folder_id = getattr(settings, 'GDRIVE_FOLDER_ID', None)
                analyzer = MalwareAnalyzer(
                    gdrive_file_id=file_id,
                    gdrive_folder_id=folder_id,
                    use_subset=use_subset,
                    subset_size=new_size
                )

            # Entrenar
            print("Iniciando reentrenamiento...")
            analyzer.run_full_analysis()
            print("✓ Reentrenamiento completado")

            return JsonResponse({
                'success': True,
                'message': f'Modelo reentrenado exitosamente con {new_size:,} filas',
                'warning': warning,
                'new_metrics': {
                    'classification': {
                        'test_accuracy': float(analyzer.clf_metrics['test']['accuracy']),
                        'test_f1': float(analyzer.clf_metrics['test']['f1_score']),
                    },
                    'regression': {
                        'test_r2': float(analyzer.reg_metrics['test']['r2']),
                        'test_rmse': float(analyzer.reg_metrics['test']['rmse']),
                    }
                }
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error durante el reentrenamiento: {str(e)}'
            })

    return JsonResponse({'success': False, 'error': 'Método no permitido'})



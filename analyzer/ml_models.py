import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import (
    f1_score, accuracy_score, precision_score, recall_score,
    classification_report, confusion_matrix,
    mean_squared_error, r2_score, mean_absolute_error
)
import warnings
import os
import gdown

warnings.filterwarnings('ignore')


class MalwareAnalyzer:
    def __init__(self, dataset_path=None, gdrive_folder_id=None, gdrive_file_id=None, use_subset=False, subset_size=50000):
        self.dataset_path = dataset_path
        self.gdrive_folder_id = gdrive_folder_id
        self.gdrive_file_id = gdrive_file_id
        self.use_subset = use_subset  # Usar solo subset para ahorrar memoria
        self.subset_size = subset_size  # Tamaño del subset (default 50,000)
        self.df = None
        self.classifier = None
        self.regressor = None
        self.scaler = RobustScaler()

        # Datos de clasificación
        self.X_train_clf = None
        self.X_val_clf = None
        self.X_test_clf = None
        self.y_train_clf = None
        self.y_val_clf = None
        self.y_test_clf = None

        # Datos de regresión
        self.X_train_reg = None
        self.X_val_reg = None
        self.X_test_reg = None
        self.y_train_reg = None
        self.y_val_reg = None
        self.y_test_reg = None

        # Métricas
        self.clf_metrics = {}
        self.reg_metrics = {}

    def download_dataset_from_gdrive(self):
        """Descargar dataset desde Google Drive"""
        if not self.gdrive_folder_id and not self.gdrive_file_id:
            raise ValueError("No se proporcionó el ID de Google Drive (folder_id o file_id)")

        # Crear directorio temporal si no existe
        temp_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'temp_data')
        os.makedirs(temp_dir, exist_ok=True)

        # Ruta donde se guardará el archivo
        output_path = os.path.join(temp_dir, 'TotalFeatures-ISCXFlowMeter.csv')

        # Si el archivo ya existe, no descargarlo de nuevo
        if os.path.exists(output_path):
            print(f"Dataset ya existe en {output_path}")
            return output_path

        # Método 1: Si tenemos file_id, usar descarga directa (MÁS CONFIABLE)
        if self.gdrive_file_id:
            print(f"Descargando dataset desde Google Drive (File ID: {self.gdrive_file_id})...")
            try:
                file_url = f"https://drive.google.com/uc?id={self.gdrive_file_id}"
                gdown.download(file_url, output_path, quiet=False, fuzzy=True)

                if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                    print(f"✓ Dataset descargado exitosamente en {output_path}")
                    print(f"  Tamaño: {os.path.getsize(output_path) / (1024*1024):.2f} MB")
                    return output_path
                else:
                    raise FileNotFoundError("El archivo descargado está vacío o no existe")

            except Exception as e:
                print(f"Error al descargar con file_id: {str(e)}")
                if not self.gdrive_folder_id:
                    raise
                print("Intentando método alternativo con folder_id...")

        # Método 2: Si tenemos folder_id, intentar descargar carpeta
        if self.gdrive_folder_id:
            print(f"Descargando dataset desde Google Drive (Folder ID: {self.gdrive_folder_id})...")

            try:
                folder_url = f"https://drive.google.com/drive/folders/{self.gdrive_folder_id}"
                print(f"Intentando descargar carpeta: {folder_url}")

                try:
                    gdown.download_folder(url=folder_url, output=temp_dir, quiet=False, use_cookies=False, remaining_ok=True)
                except:
                    # Si falla, intentar con autenticación de cookies
                    print("Intentando con cookies...")
                    gdown.download_folder(url=folder_url, output=temp_dir, quiet=False, use_cookies=True, remaining_ok=True)

                # Buscar el archivo CSV en el directorio descargado
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith('.csv'):
                            file_path = os.path.join(root, file)
                            # Si está en un subdirectorio, moverlo al directorio principal
                            if file_path != output_path:
                                import shutil
                                shutil.move(file_path, output_path)
                            print(f"✓ Dataset descargado exitosamente en {output_path}")
                            print(f"  Tamaño: {os.path.getsize(output_path) / (1024*1024):.2f} MB")
                            return output_path

                raise FileNotFoundError("No se encontró ningún archivo CSV en la carpeta descargada")

            except Exception as e:
                error_msg = f"""
╔════════════════════════════════════════════════════════════════════════════╗
║ Error al descargar el dataset desde Google Drive                          ║
╚════════════════════════════════════════════════════════════════════════════╝

Error: {str(e)}

SOLUCIÓN RECOMENDADA:
═══════════════════════════════════════════════════════════════════════════

Opción 1: Usar el FILE ID directamente (MÁS FÁCIL Y CONFIABLE)
───────────────────────────────────────────────────────────────────────────

1. Abre el archivo CSV en Google Drive
2. Haz clic en "Compartir" → "Cualquier persona con el enlace" → "Lector"
3. Copia el FILE_ID de la URL:
   https://drive.google.com/file/d/FILE_ID_AQUI/view
   
4. Actualiza malware_detector/settings.py:
   GDRIVE_FILE_ID = 'TU_FILE_ID_AQUI'

Opción 2: Compartir la carpeta públicamente
───────────────────────────────────────────────────────────────────────────

1. En Google Drive, haz clic derecho en la carpeta
2. "Compartir" → "Cambiar a cualquier persona con el enlace"
3. Asegúrate de que el rol sea "Lector"
4. Guarda los cambios

Opción 3: Usar dataset local para desarrollo
───────────────────────────────────────────────────────────────────────────

Coloca el archivo CSV en: dataset/TotalFeatures-ISCXFlowMeter.csv

═══════════════════════════════════════════════════════════════════════════
                """
                print(error_msg)
                raise Exception(error_msg)

    def load_data(self):
        """Cargar el dataset"""
        # Si se proporcionó un ID de Google Drive, descargar el dataset
        if self.gdrive_file_id or self.gdrive_folder_id:
            self.dataset_path = self.download_dataset_from_gdrive()

        if not self.dataset_path or not os.path.exists(self.dataset_path):
            raise FileNotFoundError(f"No se encontró el dataset en {self.dataset_path}")

        print(f"Cargando dataset desde: {self.dataset_path}")

        # Si use_subset es True, cargar solo una muestra para ahorrar memoria
        if self.use_subset:
            # Cargar solo subset_size filas (default 50,000 = 8% del dataset original)
            # Esto reduce el uso de memoria de ~800MB a ~64MB
            print(f"⚠️  Modo memoria limitada: Usando subset del dataset ({self.subset_size:,} filas)")
            self.df = pd.read_csv(self.dataset_path, nrows=self.subset_size)
            print(f"✓ Subset cargado: {len(self.df):,} filas, {len(self.df.columns)} columnas")
        else:
            self.df = pd.read_csv(self.dataset_path)
            print(f"✓ Dataset completo cargado: {len(self.df):,} filas, {len(self.df.columns)} columnas")

        return self.df

    def prepare_classification_data(self):
        """Preparar datos para clasificación de malware"""
        df_clf = self.df.copy()

        # Separar características y etiquetas
        X = df_clf.drop('calss', axis=1)
        y = df_clf['calss'].copy()

        # Eliminar columnas no numéricas si existen
        X = X.select_dtypes(include=[np.number])

        # Manejar valores infinitos y NaN
        X = X.replace([np.inf, -np.inf], np.nan)
        X = X.fillna(X.mean())

        # División de datos: 60% train, 20% val, 20% test
        X_train, X_temp, y_train, y_temp = train_test_split(
            X, y, test_size=0.4, random_state=42, stratify=y
        )
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp
        )

        # Escalar datos
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)
        X_test_scaled = self.scaler.transform(X_test)

        self.X_train_clf = X_train_scaled
        self.X_val_clf = X_val_scaled
        self.X_test_clf = X_test_scaled
        self.y_train_clf = y_train
        self.y_val_clf = y_val
        self.y_test_clf = y_test

        return X_train_scaled, X_val_scaled, X_test_scaled, y_train, y_val, y_test

    def train_classifier(self):
        """Entrenar Random Forest Classifier"""
        # Reducir n_estimators si usamos subset (para memoria limitada)
        n_trees = 20 if self.use_subset else 100

        self.classifier = RandomForestClassifier(
            n_estimators=n_trees,
            max_depth=15 if self.use_subset else None,  # Limitar profundidad
            random_state=42,
            n_jobs=1  # Cambiar de -1 a 1 para evitar usar todos los cores
        )
        print(f"Entrenando clasificador con {n_trees} árboles...")
        self.classifier.fit(self.X_train_clf, self.y_train_clf)

        # Predicciones
        y_train_pred = self.classifier.predict(self.X_train_clf)
        y_val_pred = self.classifier.predict(self.X_val_clf)
        y_test_pred = self.classifier.predict(self.X_test_clf)

        # Calcular métricas
        self.clf_metrics = {
            'train': {
                'accuracy': accuracy_score(self.y_train_clf, y_train_pred),
                'precision': precision_score(self.y_train_clf, y_train_pred, average='weighted'),
                'recall': recall_score(self.y_train_clf, y_train_pred, average='weighted'),
                'f1_score': f1_score(self.y_train_clf, y_train_pred, average='weighted'),
            },
            'validation': {
                'accuracy': accuracy_score(self.y_val_clf, y_val_pred),
                'precision': precision_score(self.y_val_clf, y_val_pred, average='weighted'),
                'recall': recall_score(self.y_val_clf, y_val_pred, average='weighted'),
                'f1_score': f1_score(self.y_val_clf, y_val_pred, average='weighted'),
            },
            'test': {
                'accuracy': accuracy_score(self.y_test_clf, y_test_pred),
                'precision': precision_score(self.y_test_clf, y_test_pred, average='weighted'),
                'recall': recall_score(self.y_test_clf, y_test_pred, average='weighted'),
                'f1_score': f1_score(self.y_test_clf, y_test_pred, average='weighted'),
            },
            'confusion_matrix': confusion_matrix(self.y_test_clf, y_test_pred).tolist(),
            'classification_report': classification_report(self.y_test_clf, y_test_pred, output_dict=True)
        }

        return self.clf_metrics

    def prepare_regression_data(self):
        """Preparar datos para regresión"""
        df_reg = self.df.copy()
        df_reg = df_reg.select_dtypes(include=[np.number])
        df_reg = df_reg.dropna()

        # Usar 'duration' como variable objetivo
        target_col = 'duration'

        # Características a eliminar para evitar data leakage
        features_to_drop = [
            target_col,
            'total_fiat', 'total_biat',
            'min_fiat', 'max_fiat', 'mean_fiat', 'std_fiat',
            'min_biat', 'max_biat', 'mean_biat', 'std_biat',
            'min_flowiat', 'max_flowiat', 'mean_flowiat', 'std_flowiat',
            'min_active', 'mean_active', 'max_active', 'std_active',
            'min_idle', 'mean_idle', 'max_idle', 'std_idle'
        ]

        # Filtrar solo columnas que existen
        cols_to_drop = [col for col in features_to_drop if col in df_reg.columns]

        X = df_reg.drop(cols_to_drop, axis=1)
        y = df_reg[target_col]

        # Manejar valores infinitos
        X = X.replace([np.inf, -np.inf], np.nan)
        X = X.fillna(X.mean())

        # División de datos
        X_train, X_temp, y_train, y_temp = train_test_split(
            X, y, test_size=0.4, random_state=42
        )
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=0.5, random_state=42
        )

        self.X_train_reg = X_train
        self.X_val_reg = X_val
        self.X_test_reg = X_test
        self.y_train_reg = y_train
        self.y_val_reg = y_val
        self.y_test_reg = y_test

        return X_train, X_val, X_test, y_train, y_val, y_test

    def train_regressor(self):
        """Entrenar Random Forest Regressor"""
        # Reducir n_estimators si usamos subset (para memoria limitada)
        n_trees = 20 if self.use_subset else 100

        self.regressor = RandomForestRegressor(
            n_estimators=n_trees,
            max_depth=15 if self.use_subset else None,  # Limitar profundidad
            random_state=42,
            n_jobs=1  # Cambiar de -1 a 1 para evitar usar todos los cores
        )
        print(f"Entrenando regresor con {n_trees} árboles...")
        self.regressor.fit(self.X_train_reg, self.y_train_reg)

        # Predicciones
        y_train_pred = self.regressor.predict(self.X_train_reg)
        y_val_pred = self.regressor.predict(self.X_val_reg)
        y_test_pred = self.regressor.predict(self.X_test_reg)

        # Calcular métricas
        self.reg_metrics = {
            'train': {
                'mse': mean_squared_error(self.y_train_reg, y_train_pred),
                'rmse': np.sqrt(mean_squared_error(self.y_train_reg, y_train_pred)),
                'mae': mean_absolute_error(self.y_train_reg, y_train_pred),
                'r2': r2_score(self.y_train_reg, y_train_pred),
            },
            'validation': {
                'mse': mean_squared_error(self.y_val_reg, y_val_pred),
                'rmse': np.sqrt(mean_squared_error(self.y_val_reg, y_val_pred)),
                'mae': mean_absolute_error(self.y_val_reg, y_val_pred),
                'r2': r2_score(self.y_val_reg, y_val_pred),
            },
            'test': {
                'mse': mean_squared_error(self.y_test_reg, y_test_pred),
                'rmse': np.sqrt(mean_squared_error(self.y_test_reg, y_test_pred)),
                'mae': mean_absolute_error(self.y_test_reg, y_test_pred),
                'r2': r2_score(self.y_test_reg, y_test_pred),
            }
        }

        return self.reg_metrics

    def get_feature_importance(self, model_type='classifier'):
        """Obtener importancia de características"""
        if model_type == 'classifier' and self.classifier:
            feature_names = [f"Feature_{i}" for i in range(len(self.classifier.feature_importances_))]
            importances = self.classifier.feature_importances_
        elif model_type == 'regressor' and self.regressor:
            feature_names = [f"Feature_{i}" for i in range(len(self.regressor.feature_importances_))]
            importances = self.regressor.feature_importances_
        else:
            return []

        # Ordenar por importancia
        indices = np.argsort(importances)[::-1][:20]  # Top 20

        return [
            {'feature': feature_names[i], 'importance': float(importances[i])}
            for i in indices
        ]

    def run_full_analysis(self):
        """Ejecutar análisis completo"""
        import gc

        # Cargar datos
        self.load_data()

        # Clasificación
        print("Preparando datos de clasificación...")
        self.prepare_classification_data()
        self.train_classifier()

        # Liberar memoria después de clasificación
        if self.use_subset:
            print("Liberando memoria...")
            gc.collect()

        # Regresión
        print("Preparando datos de regresión...")
        self.prepare_regression_data()
        self.train_regressor()

        # Liberar memoria final
        if self.use_subset:
            # Eliminar dataframe original para liberar memoria
            del self.df
            self.df = None
            gc.collect()
            print("✓ Memoria liberada")

        return {
            'classification': self.clf_metrics,
            'regression': self.reg_metrics
        }


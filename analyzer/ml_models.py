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

warnings.filterwarnings('ignore')


class MalwareAnalyzer:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
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

    def load_data(self):
        """Cargar el dataset"""
        self.df = pd.read_csv(self.dataset_path)
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
        self.classifier = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            n_jobs=-1
        )
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
        self.regressor = RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            n_jobs=-1
        )
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
        # Cargar datos
        self.load_data()

        # Clasificación
        self.prepare_classification_data()
        self.train_classifier()

        # Regresión
        self.prepare_regression_data()
        self.train_regressor()

        return {
            'classification': self.clf_metrics,
            'regression': self.reg_metrics
        }


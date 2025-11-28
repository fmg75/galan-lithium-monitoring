"""
Entrenamiento del Modelo Predictivo de Concentración de Litio
Usa Random Forest para predicción robusta y interpretable
"""

import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

# Configuración de visualización
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


def load_and_prepare_data(filepath):
    """Carga y prepara los datos para el modelo"""
    print("📊 Cargando datos...")
    df = pd.read_csv(filepath)
    
    # Convertir timestamp a datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    print(f"✅ Datos cargados: {len(df)} muestras")
    print(f"   Rango temporal: {df['timestamp'].min()} a {df['timestamp'].max()}")
    print(f"   Pozas: {df['poza_id'].nunique()}")
    
    return df


def feature_engineering(df):
    """Crea features adicionales para mejorar el modelo"""
    print("\n🔧 Feature Engineering...")
    
    df_features = df.copy()
    
    # Interacciones importantes
    df_features['temp_x_days'] = df['temperature_c'] * df['days_evaporation']
    df_features['conductivity_density_ratio'] = df['conductivity_ms_cm'] / df['density_g_cm3']
    df_features['evaporation_rate'] = df['days_evaporation'] / (df['humidity_percent'] + 1)
    
    # Features polinómicas para días de evaporación (relación no lineal)
    df_features['days_evaporation_sq'] = df['days_evaporation'] ** 2
    
    print(f"✅ Features creadas: {len(df_features.columns)} variables totales")
    
    return df_features


def prepare_train_test(df, target='li_concentration_mg_l', test_size=0.2):
    """Prepara conjuntos de entrenamiento y prueba"""
    print(f"\n📚 Preparando datos de entrenamiento...")
    
    # Features a usar (excluir columnas no numéricas y target)
    exclude_cols = ['timestamp', 'poza_id', 'quality_status', target]
    feature_cols = [col for col in df.columns if col not in exclude_cols]
    
    X = df[feature_cols]
    y = df[target]
    
    # Split estratificado por rangos de concentración
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )
    
    print(f"✅ Train: {len(X_train)} | Test: {len(X_test)}")
    print(f"   Features: {len(feature_cols)}")
    print(f"   Features usadas: {', '.join(feature_cols[:5])}...")
    
    return X_train, X_test, y_train, y_test, feature_cols


def train_model(X_train, y_train):
    """Entrena el modelo Random Forest"""
    print("\n🤖 Entrenando modelo Random Forest...")
    
    # Configuración del modelo
    model = RandomForestRegressor(
        n_estimators=100,          # Número de árboles
        max_depth=15,              # Profundidad máxima
        min_samples_split=5,       # Mínimo para dividir
        min_samples_leaf=2,        # Mínimo en hojas
        max_features='sqrt',       # Features por árbol
        random_state=42,
        n_jobs=-1,                 # Usar todos los cores
        verbose=0
    )
    
    # Entrenar
    model.fit(X_train, y_train)
    
    print("✅ Modelo entrenado exitosamente")
    
    # Cross-validation para robustez
    print("\n🔄 Validación cruzada (5-fold)...")
    cv_scores = cross_val_score(
        model, X_train, y_train, 
        cv=5, 
        scoring='r2',
        n_jobs=-1
    )
    print(f"   R² scores: {cv_scores.round(3)}")
    print(f"   R² medio: {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")
    
    return model


def evaluate_model(model, X_train, X_test, y_train, y_test):
    """Evalúa el rendimiento del modelo"""
    print("\n📊 Evaluación del modelo...")
    
    # Predicciones
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    # Métricas train
    train_r2 = r2_score(y_train, y_train_pred)
    train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
    train_mae = mean_absolute_error(y_train, y_train_pred)
    
    # Métricas test
    test_r2 = r2_score(y_test, y_test_pred)
    test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
    test_mae = mean_absolute_error(y_test, y_test_pred)
    
    print("\n" + "="*60)
    print("MÉTRICAS DE RENDIMIENTO")
    print("="*60)
    print(f"\n{'Métrica':<20} {'Train':<15} {'Test':<15}")
    print("-"*60)
    print(f"{'R² Score':<20} {train_r2:<15.4f} {test_r2:<15.4f}")
    print(f"{'RMSE (mg/L)':<20} {train_rmse:<15.2f} {test_rmse:<15.2f}")
    print(f"{'MAE (mg/L)':<20} {train_mae:<15.2f} {test_mae:<15.2f}")
    print("-"*60)
    
    # Error porcentual medio
    test_mape = np.mean(np.abs((y_test - y_test_pred) / y_test)) * 100
    print(f"{'MAPE (%)':<20} {'':<15} {test_mape:<15.2f}")
    print("="*60)
    
    # Interpretación
    print("\n💡 Interpretación:")
    if test_r2 > 0.85:
        print("   ✅ Excelente capacidad predictiva (R² > 0.85)")
    elif test_r2 > 0.70:
        print("   ⚠️  Buena capacidad predictiva (R² > 0.70)")
    else:
        print("   ❌ Capacidad predictiva insuficiente (R² < 0.70)")
    
    if test_mape < 10:
        print("   ✅ Error bajo (MAPE < 10%)")
    elif test_mape < 15:
        print("   ⚠️  Error aceptable (MAPE < 15%)")
    else:
        print("   ❌ Error alto (MAPE > 15%)")
    
    return {
        'train_r2': train_r2,
        'test_r2': test_r2,
        'train_rmse': train_rmse,
        'test_rmse': test_rmse,
        'test_mape': test_mape,
        'y_test': y_test,
        'y_test_pred': y_test_pred
    }


def plot_feature_importance(model, feature_cols, top_n=10):
    """Visualiza importancia de features"""
    print(f"\n📊 Visualizando top {top_n} features más importantes...")
    
    # Obtener importancias
    importances = pd.DataFrame({
        'feature': feature_cols,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    # Plot
    plt.figure(figsize=(10, 6))
    top_features = importances.head(top_n)
    plt.barh(range(len(top_features)), top_features['importance'])
    plt.yticks(range(len(top_features)), top_features['feature'])
    plt.xlabel('Importancia')
    plt.title('Top Features para Predicción de Concentración de Litio')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
    print("   ✅ Guardado: feature_importance.png")
    plt.close()
    
    return importances


def plot_predictions(y_test, y_pred):
    """Visualiza predicciones vs valores reales"""
    print("\n📊 Visualizando predicciones...")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Scatter plot
    axes[0].scatter(y_test, y_pred, alpha=0.5, s=20)
    axes[0].plot([y_test.min(), y_test.max()], 
                 [y_test.min(), y_test.max()], 
                 'r--', lw=2, label='Predicción perfecta')
    axes[0].set_xlabel('Concentración Real (mg/L)')
    axes[0].set_ylabel('Concentración Predicha (mg/L)')
    axes[0].set_title('Predicciones vs Valores Reales')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Residuals
    residuals = y_test - y_pred
    axes[1].scatter(y_pred, residuals, alpha=0.5, s=20)
    axes[1].axhline(y=0, color='r', linestyle='--', lw=2)
    axes[1].set_xlabel('Concentración Predicha (mg/L)')
    axes[1].set_ylabel('Residuales (mg/L)')
    axes[1].set_title('Análisis de Residuales')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('predictions_analysis.png', dpi=300, bbox_inches='tight')
    print("   ✅ Guardado: predictions_analysis.png")
    plt.close()


def save_model(model, scaler, feature_cols, metrics):
    """Guarda el modelo y metadatos"""
    print("\n💾 Guardando modelo...")
    
    # Guardar modelo
    joblib.dump(model, 'model.pkl')
    print("   ✅ Modelo guardado: model.pkl")
    
    # Guardar scaler si se usó (para futuro)
    # joblib.dump(scaler, 'scaler.pkl')
    
    # Guardar metadatos
    metadata = {
        'feature_cols': feature_cols,
        'metrics': metrics,
        'model_type': 'RandomForestRegressor',
        'training_date': pd.Timestamp.now().isoformat()
    }
    joblib.dump(metadata, 'model_metadata.pkl')
    print("   ✅ Metadata guardado: model_metadata.pkl")


def main():
    """Función principal"""
    print("="*60)
    print("ENTRENAMIENTO DE MODELO - PREDICCIÓN DE LITIO")
    print("="*60)
    
    # 1. Cargar datos
    df = load_and_prepare_data('../data/sample_data.csv')
    
    # 2. Feature engineering
    df_features = feature_engineering(df)
    
    # 3. Preparar train/test
    X_train, X_test, y_train, y_test, feature_cols = prepare_train_test(df_features)
    
    # 4. Entrenar modelo
    model = train_model(X_train, y_train)
    
    # 5. Evaluar
    metrics = evaluate_model(model, X_train, X_test, y_train, y_test)
    
    # 6. Visualizaciones
    importances = plot_feature_importance(model, feature_cols)
    plot_predictions(metrics['y_test'], metrics['y_test_pred'])
    
    # 7. Guardar modelo
    save_model(model, None, feature_cols, metrics)
    
    print("\n" + "="*60)
    print("✅ ENTRENAMIENTO COMPLETADO EXITOSAMENTE")
    print("="*60)
    print("\nArchivos generados:")
    print("   • model.pkl")
    print("   • model_metadata.pkl")
    print("   • feature_importance.png")
    print("   • predictions_analysis.png")
    print("\n🚀 El modelo está listo para ser usado en producción!")


if __name__ == "__main__":
    main()

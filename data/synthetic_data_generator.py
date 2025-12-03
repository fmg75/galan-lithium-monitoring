"""
Generador de Datos Sintéticos de Salmuera de Litio
Simula condiciones realistas del Salar del Hombre Muerto, Catamarca
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

def generate_brine_data(n_samples=1000):
    """
    Genera datos sintéticos de salmuera basados en condiciones reales
    del proceso de extracción de litio por evaporación.
    
    Parámetros basados en literatura técnica de salares argentinos.
    """
    
    data = []
    
    for i in range(n_samples):
        # Días de evaporación (30-180 días es el rango típico)
        days_evaporation = np.random.uniform(30, 180)
        
        # Temperatura (°C) - Salar del Hombre Muerto: -10°C a 30°C
        # Media: 23°C verano, 8°C invierno, con amplitud térmica día-noche de 20-25°C
        base_temp = 18  # Temperatura base promedio anual
        temp_variation = np.sin(days_evaporation / 30) * 8  # Variación estacional
        temperature = base_temp + temp_variation + np.random.normal(0, 3)
        temperature = np.clip(temperature, 5, 30)  # Rango operativo realista
        
        # Humedad relativa (%) - Clima árido: 10-40%
        humidity = np.random.uniform(10, 40)
        
        # pH - Típico de salmueras: 7.0-8.5
        ph = np.random.uniform(7.0, 8.5)
        
        # Conductividad eléctrica (mS/cm) - Aumenta con concentración
        base_conductivity = 80 + (days_evaporation / 180) * 40
        conductivity = base_conductivity + np.random.normal(0, 5)
        conductivity = np.clip(conductivity, 50, 150)
        
        # Densidad (g/cm³) - Aumenta con evaporación
        base_density = 1.10 + (days_evaporation / 180) * 0.15
        density = base_density + np.random.normal(0, 0.02)
        density = np.clip(density, 1.10, 1.25)
        
        # Ratio Mg/Li - Crítico para calidad (ideal < 6, problemático > 10)
        mg_li_ratio = np.random.uniform(3, 15)
        
        # Ratio Ca/Li - Afecta pureza
        ca_li_ratio = np.random.uniform(0.5, 3)
        
        # VARIABLE OBJETIVO: Concentración de Litio (mg/L)
        # Modelo simplificado: función de días de evaporación + factores
        base_concentration = 2000 + (days_evaporation - 30) * 25
        
        # Factores que afectan concentración
        temp_factor = (temperature - 25) * 15  # Mayor temperatura = más evaporación
        humidity_factor = -(humidity - 25) * 8  # Mayor humedad = menos evaporación
        conductivity_factor = (conductivity - 80) * 3
        
        # Penalización por contaminantes
        mg_penalty = -max(0, (mg_li_ratio - 6) * 50)
        ca_penalty = -max(0, (ca_li_ratio - 1.5) * 30)
        
        li_concentration = (base_concentration + 
                           temp_factor + 
                           humidity_factor + 
                           conductivity_factor + 
                           mg_penalty + 
                           ca_penalty + 
                           np.random.normal(0, 150))
        
        # Límites realistas: 200-6000 mg/L
        li_concentration = np.clip(li_concentration, 200, 6000)
        
        # Estado de calidad basado en concentración y pureza
        if li_concentration > 4500 and mg_li_ratio < 6:
            quality_status = "Óptimo"
        elif li_concentration > 3000 and mg_li_ratio < 10:
            quality_status = "Bueno"
        elif li_concentration > 2000:
            quality_status = "Aceptable"
        else:
            quality_status = "Bajo"
        
        # Timestamp simulado
        base_date = datetime(2025, 1, 1)
        timestamp = base_date + timedelta(hours=i*6)  # Medición cada 6 horas
        
        data.append({
            'timestamp': timestamp,
            'poza_id': f"POZA_{np.random.randint(1, 6)}",
            'days_evaporation': round(days_evaporation, 1),
            'temperature_c': round(temperature, 2),
            'humidity_percent': round(humidity, 2),
            'ph': round(ph, 2),
            'conductivity_ms_cm': round(conductivity, 2),
            'density_g_cm3': round(density, 3),
            'mg_li_ratio': round(mg_li_ratio, 2),
            'ca_li_ratio': round(ca_li_ratio, 2),
            'li_concentration_mg_l': round(li_concentration, 2),
            'quality_status': quality_status
        })
    
    df = pd.DataFrame(data)
    return df


def generate_summary_statistics(df):
    """Genera estadísticas descriptivas del dataset"""
    
    print("=" * 60)
    print("RESUMEN ESTADÍSTICO - DATOS DE SALMUERA")
    print("=" * 60)
    print(f"\nTotal de muestras: {len(df)}")
    print(f"Rango de fechas: {df['timestamp'].min()} a {df['timestamp'].max()}")
    print(f"\nPozas únicas: {df['poza_id'].nunique()}")
    print("\nDistribución por calidad:")
    print(df['quality_status'].value_counts())
    
    print("\n" + "=" * 60)
    print("ESTADÍSTICAS DE VARIABLES CLAVE")
    print("=" * 60)
    
    key_vars = ['li_concentration_mg_l', 'days_evaporation', 
                'temperature_c', 'mg_li_ratio']
    
    print(df[key_vars].describe().round(2))
    
    print("\n" + "=" * 60)
    print("CORRELACIONES CON CONCENTRACIÓN DE LITIO")
    print("=" * 60)
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    correlations = df[numeric_cols].corr()['li_concentration_mg_l'].sort_values(ascending=False)
    print(correlations.round(3))


if __name__ == "__main__":
    print("Generando datos sintéticos de salmuera de litio...")
    print("Basado en condiciones del Salar del Hombre Muerto, Catamarca\n")
    
    # Generar dataset
    df = generate_brine_data(n_samples=1000)
    
    # Guardar
    output_file = "sample_data.csv"
    df.to_csv(output_file, index=False)
    print(f"✅ Dataset guardado en: {output_file}")
    
    # Mostrar estadísticas
    generate_summary_statistics(df)
    
    # Mostrar primeras filas
    print("\n" + "=" * 60)
    print("PRIMERAS 5 MUESTRAS")
    print("=" * 60)
    print(df.head())
    
    print("\n✅ Generación completa!")
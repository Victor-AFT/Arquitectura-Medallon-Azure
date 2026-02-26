
# 🏗️ Arquitectura Medallón en Azure  
Implementación de un pipeline completo de ingeniería de datos siguiendo el **Medallion Architecture Pattern (Bronze → Silver → Gold)** utilizando la plataforma de datos de **Microsoft Azure**.

Este proyecto demuestra cómo construir un flujo moderno, escalable y gobernado para ingesta, procesamiento, transformación y consumo de datos en un Data Lake.

<img width="650" height="500" alt="Diagrama sin título drawio (2)" src="https://github.com/user-attachments/assets/1295a49d-ac6a-41d6-9649-4a46a914bfcf" />

## ☁️ Servicios de Azure Utilizados

| Servicio | Uso |
|---------|-----|
| **Azure Data Factory** | Orquestación de pipelines, ingestión y control de flujos |
| **Azure Data Lake Storage Gen2** | Almacenamiento de las capas Bronze, Silver y Gold |
| **Azure Databricks (PySpark)** | Procesamiento escalable y transformaciones |
| **Delta Lake** | Formato ACID para datos confiables |
| **Azure Key Vault (opcional)** | Protección de credenciales |
| **Azure SQL Server** | Servidor de base de datos  |
| **Azure SQL database** | Base de datos SQL |
| **Azure Function** | Azure function para las peticiones a la API web  |
| **Power BI / Synapse** | Análisis y visualización final |


---
## 🔄 Funcionamiento del Pipeline

### ⭐ 1. Bronze — *Raw*
La capa Bronze almacena los datos exactamente como llegan:

- Sin transformaciones  
- Esquema flexible  
- Auditabilidad completa  
- Ideal para reproducir procesos  

---

### ⭐ 2. Silver — *Clean*
La capa Silver realiza:

- Limpieza y normalización  
- Tipado correcto de columnas  
- Validación de valores y calidad de datos  

---

### ⭐ 3. Gold — *Business*
Optimizada para consumo:

- Datos agregados  
- KPIs listos para Power BI  

---

## 👤 Autor

**Víctor Fuentes Toledo**  
Proyecto técnico de referencia para arquitectura Medallón en Azure.  

---

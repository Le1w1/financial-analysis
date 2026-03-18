# Financial Analysis Dashboard

Dashboard de análisis financiero con datos reales de mercado, construido con Python, SQL Server y Power BI.

## Stack
- **Python** — extracción y transformación de datos
- **Alpha Vantage API** — datos históricos de precios de acciones
- **SQL Server** — almacenamiento de datos
- **Power BI** — visualización y dashboard

## Estructura del proyecto
```
financial-analysis/
├── data/
├── etl/
│   ├── extract.py       # Extracción de datos desde Alpha Vantage API
│   └── transform.py     # Transformación, métricas y carga a SQL Server
├── notebooks/
│   ├── 01_extract.ipynb
│   └── 02_transform.ipynb
├── reports/
│   └── financial_analysis_dashboard.pbix
├── .env                 # Variables de entorno (no versionado)
├── .gitignore
└── README.md
```

## Pipeline
1. `extract.py` consume la API de Alpha Vantage y carga precios históricos en SQL Server
2. `transform.py` calcula métricas (MA20, MA50, retorno diario) y las carga en SQL Server
3. Power BI se conecta a SQL Server y visualiza los datos

## Dashboard
- Precio de cierre con medias móviles (MA20, MA50)
- Retorno diario
- KPIs: precio máximo, precio mínimo, retorno promedio
- Filtro interactivo por fecha

## Cómo ejecutar
1. Clonar el repositorio
2. Crear un archivo `.env` con `API_KEY=tu_api_key`
3. Ejecutar `py etl/transform.py`
4. Abrir `reports/financial_analysis_dashboard.pbix` en Power BI Desktop
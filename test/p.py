# CONCEPTO NUEVO
if area == "Analítica de Contraloría" or area == "Admin":
        lista_concepto_nuevo = df.iloc[:,22].dropna().drop_duplicates().tolist()
    elif area == "Control de Operaciones":
        lista_concepto_nuevo = df.iloc[:,38].dropna().drop_duplicates().tolist()
    elif area == "Administrativa":
        lista_concepto_nuevo = df.iloc[:,10].dropna().drop_duplicates().tolist()
    elif area == "Riesgos y Cumplimiento":
        lista_concepto_nuevo = df.iloc[:,50].dropna().drop_duplicates().tolist()
    elif area == "Impuestos":
        lista_concepto_nuevo = df.iloc[:,46].dropna().drop_duplicates().tolist()
    elif area == "Contabilidad":
        lista_concepto_nuevo = df.iloc[:,30].dropna().drop_duplicates().tolist()
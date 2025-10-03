# === EXPORTADOR S14: crea los CSV finales de entrega ===
import os, zipfile, glob
import numpy as np
import pandas as pd

OUT = "salidas"
os.makedirs(OUT, exist_ok=True)

generated = []   # iremos guardando rutas de los CSV generados

# ------------------------------
# 1) OPERADORES (ineficacia)  -> s14_operadores_ineficaces_metrics.csv
#     Requiere: op_flags (del Bloque 5)
# ------------------------------
if "op_flags" in globals():
    cols_show = [
        "user_id","operator_id","active_days","in_assigned_total","in_ans_calls","in_miss_post_calls",
        "missed_rate_post","avg_wait_in_ans",
        "out_ext_calls","out_median_daily","out_share_days","out_avg_daily","expected_outbound",
        "flag_miss_high","flag_wait_high","flag_out_low","enough_volume","ineffective"
    ]
    cols_present = [c for c in cols_show if c in op_flags.columns]
    # Orden sugerido: user_id, ineffective desc, missed desc, wait desc
    sort_keys = [k for k in ["user_id","ineffective","missed_rate_post","avg_wait_in_ans"] if k in op_flags.columns]

    ineff_table_sorted = (
        op_flags[cols_present]
        .sort_values(sort_keys, ascending=[True, False, False, False] if len(sort_keys)==4 else True)
    )
    fp = os.path.join(OUT, "s14_operadores_ineficaces_metrics.csv")
    ineff_table_sorted.to_csv(fp, index=False, float_format="%.6f")
    generated.append(fp)
    print(f"✅ Exportado: {fp}")
else:
    print("⚠️ No encontré 'op_flags' en memoria. Omite s14_operadores_ineficaces_metrics.csv")

# ------------------------------
# 2) COLA / CONTEXTO (cliente) -> s14_queue_context_por_cliente.csv
#     Usa 'queue_summary' si existe; si no, lo reconstruye a partir de 'calls_win' (Bloque 6)
# ------------------------------
queue_summary_sorted = None

if "queue_summary" in globals():
    queue_summary_sorted = queue_summary.sort_values(["user_id"]) if "user_id" in queue_summary.columns else queue_summary.copy()
elif "queue_summary2" in globals():
    # versión extendida: si existe, la adaptamos a un CSV simple
    qs2 = queue_summary2.copy()
    # si trae columnas extendidas, deja nombres amistosos
    rename_map = {}
    if "pre_avg_wait_weighted" in qs2.columns and "pre_avg_wait" not in qs2.columns:
        rename_map["pre_avg_wait_weighted"] = "pre_avg_wait"
    queue_summary_sorted = qs2.rename(columns=rename_map)
    # deja columnas clave si existen
    keep_cols = [c for c in ["user_id","inbound_calls","pre_missed_calls","pre_avg_wait","pre_abandon_rate"] if c in queue_summary_sorted.columns]
    if keep_cols:
        queue_summary_sorted = queue_summary_sorted[keep_cols].sort_values(["user_id"])
else:
    # reconstrucción mínima desde calls_win (si existe)
    if "calls_win" in globals():
        cw = calls_win.copy()
        # Asegura columnas esperadas
        expected = {"user_id","date","calls_count","total_call_duration","is_inbound"}
        if not expected.issubset(set(cw.columns)):
            print("⚠️ 'calls_win' no tiene todas las columnas esperadas para reconstruir queue_summary; se omite.")
        else:
            # pre (abandono en cola)
            is_pre = cw.get("miss_stage", pd.Series([np.nan]*len(cw))).eq("pre")
            queue_daily = (
                cw[is_pre]
                .groupby(["user_id","date"], as_index=False)
                .agg(pre_missed_calls=("calls_count","sum"),
                     pre_wait_sum=("total_call_duration","sum"))
            )
            # inbound total
            inbound_daily = (
                cw[cw["is_inbound"]==True]
                .groupby(["user_id","date"], as_index=False)
                .agg(inbound_calls=("calls_count","sum"))
            )
            qd = inbound_daily.merge(queue_daily, on=["user_id","date"], how="left")
            qd["pre_missed_calls"] = qd["pre_missed_calls"].fillna(0)
            qd["pre_avg_wait"] = np.where(qd["pre_missed_calls"]>0, qd["pre_wait_sum"]/qd["pre_missed_calls"], np.nan)

            queue_summary_sorted = qd.groupby("user_id", as_index=False).agg(
                inbound_calls=("inbound_calls","sum"),
                pre_missed_calls=("pre_missed_calls","sum"),
                pre_avg_wait=("pre_avg_wait","mean")
            ).sort_values(["user_id"])
    else:
        print("⚠️ No encontré 'queue_summary' ni 'queue_summary2' ni 'calls_win'. Omite s14_queue_context_por_cliente.csv")

if queue_summary_sorted is not None:
    fp = os.path.join(OUT, "s14_queue_context_por_cliente.csv")
    queue_summary_sorted.to_csv(fp, index=False, float_format="%.6f")
    generated.append(fp)
    print(f"✅ Exportado: {fp}")

# ------------------------------
# 3) DIARIO (trazabilidad)     -> s14_daily_base_operador.csv
#     Requiere: daily (Bloque 3/4)
# ------------------------------
if "daily" in globals():
    # orden amistoso si existen esas columnas
    sort_keys = [k for k in ["user_id","operator_id","date"] if k in daily.columns]
    daily_sorted = daily.sort_values(sort_keys) if sort_keys else daily.copy()
    fp = os.path.join(OUT, "s14_daily_base_operador.csv")
    daily_sorted.to_csv(fp, index=False, float_format="%.6f")
    generated.append(fp)
    print(f"✅ Exportado: {fp}")
else:
    print("⚠️ No encontré 'daily' en memoria. Omite s14_daily_base_operador.csv")

# ------------------------------
# 4) (Opcional) versión “latino” del primero si existe
# ------------------------------
try:
    if "ineff_table_sorted" in globals():
        fp_lat = os.path.join(OUT, "s14_operadores_ineficaces_metrics_latino.csv")
        ineff_table_sorted.to_csv(fp_lat, index=False, sep=";", decimal=",")
        generated.append(fp_lat)
        print(f"✅ Exportado: {fp_lat}")
except Exception as e:
    print(f"ℹ️ Salté versión latino por: {e}")

# ------------------------------
# 5) Empaquetar ZIP
# ------------------------------
if generated:
    zip_path = os.path.join(OUT, "s14_entregables.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in generated:
            z.write(f, arcname=os.path.basename(f))
    print(f"📦 Paquete ZIP listo: {zip_path}")
else:
    print("⚠️ No se generó ningún CSV (faltaron dataframes base). Revisa mensajes anteriores.")

# Changelog

## v1.1 — Perbaikan konsistensi pipeline
- **Fix:** `Orchestra.ipynb` gagal total karena `pd.to_datetime(..., format='mixed')`
  tanpa `dayfirst=True`. Diperbaiki dengan menggabungkan `format='mixed'`
  dan `dayfirst=True`.
- **Add:** step Validate ditambahkan ke `Extraction.ipynb` (sebelumnya
  langsung Extract → Transform → Load, tidak konsisten dengan penjelasan
  Validation Gate di halaman 6 PDF portofolio).
- **Add:** `etl_pipeline.py` — logic ETL disatukan jadi satu module,
  dipakai bersama oleh `orchestrator.py` dan `dags/etl_ecommerce_dag.py`.
- **Add:** `dags/etl_ecommerce_dag.py` — DAG Airflow production-ready
  sesuai struktur GitHub yang direncanakan di halaman 9 PDF.
- **Add:** `raw_orders.csv` disertakan (sebelumnya tidak ada di folder
  submission, sehingga pipeline tidak bisa dijalankan ulang).
- **Add:** `DATA_DICTIONARY.md`, `PROJECT_LEARNINGS.md`, `CHANGELOG.md`
  sesuai struktur GitHub yang sudah direncanakan sebelumnya.
- **Cleanup:** menghapus duplikat `Portofolio link file(1).txt`.

## v1.0 — Draf awal
- `Extraction.ipynb` — Extract, Transform, Load (tanpa Validate)
- `Orchestra.ipynb` — mini orchestrator (gagal jalan karena bug tanggal)
- `yazitzy.pdf` — presentasi 11 halaman

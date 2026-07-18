# ETL Pipeline Portfolio — E-Commerce Orders
**Oleh Yazitzy** — Workshop "ETL Architecture, Orchestration & Career Advancement"

Presentasi lengkap: `yazitzy.pdf`

## Struktur folder

```
.
├── yazitzy.pdf   # Presentasi 11 halaman
├── etl_design.md              # Pendamping teknis presentasi (kode & keputusan desain)
├── DATA_DICTIONARY.md
├── PROJECT_LEARNINGS.md
├── CHANGELOG.md
├── Extraction.ipynb            # Walkthrough: Extract → Transform → Validate → Load
├── Orchestra.ipynb             # Mini orchestrator — simulasi Airflow
├── etl_pipeline.py             # Logic ETL sebagai module (dipakai notebook, orchestrator, & DAG)
├── orchestrator.py             # Versi script dari Orchestra.ipynb
├── dags/
│   ├── etl_ecommerce_dag.py    # DAG Airflow production-ready
│   └── etl_pipeline.py         # salinan (Airflow butuh ini di folder dags/)
├── screenshots/
│   ├── pipeline_success.png    # screenshot terminal run sukses (data asli)
│   └── airflow_dag_design.png  # diagram desain graph view DAG Airflow
├── data/
│   ├── raw_orders.csv
│   └── raw_products.csv
├── raw_orders.csv / raw_products.csv   # data mentah (juga di root untuk notebook)
├── orders_clean.csv            # hasil Load
├── summary_report.csv          # hasil Report
├── pipeline_log.txt            # log run terakhir (SUCCESS)
└── yazitzy-link-file.txt    # link Notion
```

## Yang diperbaiki dari draf sebelumnya

Detail lengkap ada di `CHANGELOG.md` dan `PROJECT_LEARNINGS.md`. Ringkasnya:

1. **`Orchestra.ipynb` tadinya gagal total** — parsing tanggal pakai
   `format='mixed'` tanpa `dayfirst=True`, pipeline crash setelah 3x
   retry. Sudah diperbaiki dan sudah dijalankan ulang sampai sukses
   (`pipeline_log.txt` sekarang menunjukkan `COMPLETED`, bukan `FAILED`).
2. **`Extraction.ipynb` tadinya tidak punya step Validate**, padahal PDF
   portofolio menjelaskan Validation Gate secara detail di halaman 6.
   Sudah ditambahkan.
3. **`raw_orders.csv` tadinya tidak ikut ter-upload**, jadi pipeline
   tidak bisa dijalankan ulang oleh orang lain. Sudah disertakan.
4. Kode ETL disatukan ke `etl_pipeline.py` supaya notebook, mini
   orchestrator, dan DAG Airflow semuanya konsisten — tidak ada versi
   yang diam-diam berbeda.

## Cara menjalankan

**Notebook (paling cepat):**
```bash
jupyter notebook Extraction.ipynb   # atau Orchestra.ipynb
```

**Script:**
```bash
pip install pandas numpy
python orchestrator.py
```

**Airflow (opsional):**
DAG ada di `dags/etl_ecommerce_dag.py`, sudah pakai `etl_pipeline.py`
yang sama dengan versi lokal.

## Ringkasan hasil

- 130 baris mentah → 110 baris bersih
- Elektronik: 81 order, Rp 435.180.000
- Furniture: 29 order, Rp 127.350.000
- Total revenue: Rp 562.530.000
- 5/5 quality check PASSED

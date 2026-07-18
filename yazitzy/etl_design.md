# ETL Pipeline Design: E-Commerce Orders

**Dibuat oleh:** Yazitzy
**Bagian dari:** Portofolio Data Engineering — Workshop "ETL Architecture, Orchestration & Career Advancement"
**Rujukan:** `yazitzy.pdf` (presentasi lengkap 11 halaman)

## 1. Business Problem & Objectives

**Masalah data mentah:** data duplikat, missing email dan harga, harga
negatif akibat error input, format tanggal campur, kota dan channel tidak
konsisten.

**Tujuan pipeline:** membersihkan data transaksi, membuat data siap
analisis, mencegah data kotor masuk output, membuat summary report
otomatis.

**Nilai portofolio:** ETL development, data quality mindset, basic
orchestration, dokumentasi GitHub.

## 2. Dataset & Initial Audit

| Masalah | Contoh | Dampak |
|---|---|---|
| Duplikasi | 10 baris duplikat | Order/revenue terhitung ganda |
| Missing email | ~20 baris | Identitas pelanggan tidak lengkap |
| Missing total | ~5 baris | Revenue tidak akurat |
| Harga negatif | ~5 baris | Data error memengaruhi laporan |
| Tanggal campur | `2024-06-15`, `15/06/2024`, `Jun 15, 2024` | Analisis waktu gagal |
| Channel/kota inkonsisten | `mobile_app` vs `MOBILE_APP` | Group-by tidak konsisten |

**Insight penting:** masalah cleaning di latihan ini adalah masalah nyata
Data Engineer. Di industri, prosesnya harus otomatis dan terjadwal.

## 3. ETL Architecture

```
EXTRACT   → Baca raw_orders.csv dan raw_products.csv
TRANSFORM → Deduplicate, fill missing, standardize date/text, create features
VALIDATE  → Quality gate: no duplicates, no nulls, valid datetime, no negative price
LOAD      → Simpan orders_clean.csv dan summary_report.csv
```

**Prinsip:** data tidak boleh di-load sebelum lolos validasi.

## 4. Transform: Cleaning Rules

```python
# Hapus duplikasi dan data error
orders = orders.drop_duplicates()
orders = orders[orders['total_harga'] >= 0]

# Isi missing values
orders['customer_email'] = orders['customer_email'].fillna('unknown@placeholder.com')
orders['total_harga'] = orders['total_harga'].fillna(orders['total_harga'].median())

# Standarkan tanggal campur
orders['tanggal_order'] = pd.to_datetime(
    orders['tanggal_order'],
    format='mixed',
    dayfirst=True
)

# Standarkan teks
orders['kota'] = orders['kota'].str.strip().str.title()
orders['channel'] = orders['channel'].str.strip().str.lower().str.replace(' ', '_')
```

**Catatan Tanggal — Feature Engineering:** kolom `tanggal_order` punya 3
format berbeda dalam satu kolom, jadi butuh `format='mixed'` supaya
pandas menebak format per baris, dikombinasikan dengan `dayfirst=True`
karena datanya memakai konvensi Indonesia DD/MM/YYYY.

**Update dari versi awal:** draf pertama pipeline ini (di `Orchestra.ipynb`)
memakai `dayfirst=True` tanpa `format='mixed'`. Ini menyebabkan pipeline
gagal total setelah 3x retry dengan error `time data ... does not match
format`, karena pandas mencoba menerapkan satu format tetap ke seluruh
kolom yang isinya sebenarnya campuran 3 format berbeda. Kombinasi
`format='mixed'` + `dayfirst=True` bersama-sama adalah perbaikan yang
robust dan sudah diverifikasi jalan ulang tanpa error.

## 5. Validation Gate & Outputs

**Quality checks:**
- Tidak ada duplikat
- Tidak ada missing value
- Tidak ada harga negatif
- Tanggal tipe datetime
- Channel konsisten

**Output:**
- `orders_clean.csv` — dataset bersih siap analisis
- `summary_report.csv` — ringkasan order dan revenue per kategori

**Jika validasi gagal:** pipeline berhenti, load tidak dijalankan, error
dicatat ke `pipeline_log.txt` untuk troubleshooting.

## 6. Orchestration Concept

**Task flow / dependency:**
`extract >> transform >> validate >> load >> report >> notify`

Validate berfungsi sebagai gate — jika gagal, task load, report, dan
notify tidak dijalankan.

| Retry | Logging | Validation Gate | Alert |
|---|---|---|---|
| MAX_RETRIES = 3, backoff saat gagal | `pipeline_log.txt`, status per task | Clean data wajib lolos quality check sebelum load | Notify saat pipeline selesai atau gagal |

**Airflow-style DAG artifact:**
```python
extract >> transform >> validate >> load >> report >> notify
schedule='0 6 * * *'  # daily 06:00
```

## 7. Cloud Data Engineering Overview

| Google Cloud | AWS | Microsoft Azure |
|---|---|---|
| Cloud Storage | S3 | Blob Storage |
| BigQuery | Redshift | Synapse |
| Dataflow | Glue | Data Factory |
| Composer / Airflow | MWAA / Airflow | Monitor |

**Generic cloud architecture:** App/CSV/API → Cloud Storage → Transform → Warehouse → Dashboard

## 8. Skills Demonstrated & Future Improvements

**Skills demonstrated:** Data Cleaning, Data Transformation, Data
Validation, Feature Engineering, ETL Development, Workflow Orchestration,
Logging & Monitoring, Documentation.

**Future improvements:**
- Integrasi Google BigQuery
- Deploy Airflow via Docker
- Slack/email notification
- Unit test data quality

**Business value:** data transaksi siap analisis, report kategori
otomatis, error tracking via log, quality gate sebelum load.

**Recruiter signal:** end-to-end ownership, clean GitHub structure,
readable documentation, production-aware mindset.

## 9. Key Takeaways

- Cleaning harus otomatis dan repeatable
- Validasi wajib sebelum load
- Logging mempercepat troubleshooting
- Dokumentasi membuat project layak portofolio
- **Ditambahkan dari proses perbaikan:** kode yang "kelihatan benar" tetap
  perlu dites ulang setelah perubahan environment/versi library — bug
  `format='mixed'` di atas baru ketahuan setelah dijalankan ulang, bukan
  saat pertama kali ditulis.

---
*Presentasi lengkap dengan visual ada di
`yazitzy.pdf`. Dokumen ini adalah
pendamping teknis yang merinci kode dan keputusan desain di baliknya.*

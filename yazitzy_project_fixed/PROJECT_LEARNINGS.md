# Project Learnings

## Apa yang berjalan baik

- Memahami pola ETL standar (Extract → Transform → Validate → Load) dan
  kenapa validation gate penting: mencegah data kotor sampai ke warehouse.
- Mendesain quality checks yang konkret dan bisa diaudit (5 kriteria
  jelas, bukan sekadar "cek data bagus").
- Mendokumentasikan arsitektur dan trade-off dalam bentuk presentasi yang
  bisa dibaca orang lain, bukan cuma kode.

## Bug yang ditemukan (dan kenapa ini pembelajaran penting)

Draf awal `Orchestra.ipynb` memakai
`pd.to_datetime(df['tanggal_order'], format='mixed')` **tanpa**
`dayfirst=True`. Ini menyebabkan pipeline gagal total setelah 3x retry:

```
[transform] [FAILED] Error: time data '11/07/2024' does not match format 'mixed' (match)
[pipeline] [FAILED] Pipeline gagal: time data '11/07/2024' does not match format 'mixed' (match)
```

Sementara itu, `Extraction.ipynb` memakai `dayfirst=True` **tanpa**
`format='mixed'` dan berhasil di satu environment, tapi ternyata rapuh —
gagal di environment/versi pandas lain karena data punya 3 format
berbeda dalam satu kolom (ISO, slash, teks), dan tanpa `format='mixed'`
pandas mencoba menerapkan satu format tetap untuk seluruh kolom.

**Pelajaran:** kombinasi `format='mixed'` + `dayfirst=True` bersama-sama
adalah solusi yang benar-benar robust — bukan salah satu saja. Kode yang
"kelihatan jalan" di satu percobaan belum tentu jalan di kondisi lain;
perlu diuji ulang, bukan diasumsikan benar karena tidak ada error saat
ditulis pertama kali.

## Yang akan dilakukan berbeda ke depannya

- Menjalankan ulang notebook dari awal (restart kernel + run all) sebelum
  menganggap sebuah versi pipeline "selesai", supaya bug seperti ini
  ketahuan sebelum di-submit, bukan sesudah.
- Menyatukan logic Extract/Transform/Validate/Load ke satu module
  (`etl_pipeline.py`) yang dipakai bersama oleh notebook eksplorasi,
  mini orchestrator, dan DAG Airflow — supaya tidak ada 2 versi kode yang
  bisa diam-diam tidak sinkron satu sama lain.
- Menyertakan `raw_orders.csv` di setiap submission — draf sebelumnya
  sempat tidak menyertakan file ini, yang berarti pipeline tidak bisa
  dijalankan ulang oleh orang lain tanpa file itu.

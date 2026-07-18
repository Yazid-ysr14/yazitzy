# Data Dictionary

## `orders_clean.csv`

| Kolom | Tipe | Deskripsi |
|---|---|---|
| order_id | string | ID unik transaksi |
| product_id | string | ID produk, relasi ke `raw_products.csv` |
| product_name | string | Nama produk |
| kategori | string | Elektronik / Furniture |
| quantity | int | Jumlah unit dibeli |
| total_harga | float | Total harga transaksi (Rupiah) |
| tanggal_order | datetime | Tanggal transaksi, distandarkan ke `datetime64` |
| kota | string | Kota tujuan, title case |
| channel | string | website / mobile_app / marketplace |
| status | string | Status order |
| customer_email | string | Email pelanggan (`unknown@placeholder.com` jika kosong di data mentah) |
| bulan | string | Nama bulan, diturunkan dari `tanggal_order` |
| kategori_harga | string | kecil (< Rp500rb) / sedang (Rp500rb–2jt) / besar (> Rp2jt) |

## `summary_report.csv`

| Kolom | Tipe | Deskripsi |
|---|---|---|
| kategori | string | Elektronik / Furniture |
| total_orders | int | Jumlah order per kategori |
| total_revenue | float | Total revenue per kategori (Rupiah) |
| avg_revenue | float | Rata-rata revenue per order |

## `raw_orders.csv` (sumber, sebelum cleaning)

Sama seperti `orders_clean.csv` tapi tanpa kolom `bulan`/`kategori_harga`,
dan sebelum dibersihkan (masih ada duplikat, missing value, harga
negatif, format tanggal/teks tidak konsisten).

## `raw_products.csv`

| Kolom | Tipe | Deskripsi |
|---|---|---|
| product_id | string | ID unik produk |
| product_name | string | Nama produk |
| kategori | string | Elektronik / Furniture |
| harga_satuan | int | Harga satuan produk (Rupiah) |

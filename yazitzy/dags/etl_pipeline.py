"""
etl_pipeline.py
Versi script dari Extraction.ipynb -- Extract, Transform, Validate, Load.

Perbaikan dari Extraction.ipynb asli: menambahkan step VALIDATE (quality
gate) sebelum Load, supaya konsisten dengan yang dijelaskan di halaman 6
yazitzy.pdf ("Validation Gate & Outputs").
Sebelumnya notebook langsung lompat dari Transform ke Load tanpa gate ini.
"""

import pandas as pd
import numpy as np

INPUT_ORDERS = "raw_orders.csv"
INPUT_PRODUCTS = "raw_products.csv"
OUTPUT_FILE = "orders_clean.csv"
REPORT_FILE = "summary_report.csv"


def extract():
    """EXTRACT: baca data dari sumber (simulasi: file CSV)."""
    orders = pd.read_csv(INPUT_ORDERS)
    products = pd.read_csv(INPUT_PRODUCTS)

    print("=== ORDERS INFO ===")
    print(f"Jumlah baris: {len(orders)}")
    print(f"Duplikasi: {orders.duplicated().sum()}")
    print(f"Harga negatif: {(orders['total_harga'] < 0).sum()}")
    print(f"Channel unik: {orders['channel'].unique()}")
    return orders, products


def transform(orders):
    """TRANSFORM: bersihkan duplikasi, harga error, missing value, dan
    standarkan format tanggal/teks."""
    before = len(orders)
    orders = orders.drop_duplicates()
    print(f"Sebelum: {before} baris -> setelah hapus duplikat: {len(orders)} baris")

    orders = orders[orders["total_harga"] >= 0]
    print(f"Setelah hapus harga negatif: {len(orders)} baris")

    orders["customer_email"] = orders["customer_email"].fillna("unknown@placeholder.com")
    median_harga = orders["total_harga"].median()
    orders["total_harga"] = orders["total_harga"].fillna(median_harga)
    print(f"Missing values setelah fillna: {orders.isnull().sum().sum()}")

    # Standarkan format tanggal.
    # PENTING: kolom ini punya 3 format berbeda dalam satu kolom (ISO
    # '2024-06-15', slash '15/06/2024', teks 'Jun 15, 2024'), jadi
    # dibutuhkan format='mixed' supaya pandas menebak format per baris --
    # dayfirst=True saja (tanpa format='mixed') memang jalan di beberapa
    # versi pandas yang lebih toleran, tapi di versi lain akan error
    # persis seperti yang terjadi di Orchestra.ipynb versi lama:
    # "time data ... doesn't match format" -- karena pandas mencoba satu
    # format tetap untuk seluruh kolom. format='mixed' + dayfirst=True
    # bersama-sama adalah kombinasi yang robust di semua versi pandas.
    orders["tanggal_order"] = pd.to_datetime(
        orders["tanggal_order"], format="mixed", dayfirst=True
    )
    print(f"Tipe tanggal: {orders['tanggal_order'].dtype}")

    orders["kota"] = orders["kota"].str.strip().str.title()
    orders["channel"] = orders["channel"].str.strip().str.lower().str.replace(" ", "_")
    print(f"Channel setelah standarisasi: {orders['channel'].unique()}")

    orders["bulan"] = orders["tanggal_order"].dt.month_name()
    orders["kategori_harga"] = np.where(
        orders["total_harga"] < 500_000, "kecil",
        np.where(orders["total_harga"] <= 2_000_000, "sedang", "besar"),
    )
    print(f"Distribusi kategori harga:\n{orders['kategori_harga'].value_counts()}")
    return orders


def validate(orders):
    """VALIDATE: quality gate sebelum data dimuat ke warehouse.
    (Ditambahkan -- lihat catatan perbaikan di docstring modul.)"""
    checks = {
        "Tidak ada duplikat": orders.duplicated().sum() == 0,
        "Tidak ada missing value": orders.isnull().sum().sum() == 0,
        "Tidak ada harga negatif": (orders["total_harga"] < 0).sum() == 0,
        "Tanggal tipe datetime": str(orders["tanggal_order"].dtype).startswith("datetime"),
        "Channel konsisten": len(orders["channel"].unique()) <= 3,
    }
    print("=== VALIDASI DATA BERSIH ===")
    for check, passed in checks.items():
        print(f"  {'PASS' if passed else 'FAIL'} - {check}")

    failed = [k for k, v in checks.items() if not v]
    if failed:
        raise ValueError(f"VALIDASI GAGAL: {failed}")
    print("Hasil: SEMUA LOLOS")
    return orders


def load(orders):
    """LOAD: simpan data bersih + summary report."""
    orders_clean = orders[[
        "order_id", "product_id", "product_name", "kategori",
        "quantity", "total_harga", "tanggal_order", "kota",
        "channel", "status", "customer_email", "bulan", "kategori_harga",
    ]]
    orders_clean.to_csv(OUTPUT_FILE, index=False)
    print(f"Data bersih disimpan: {OUTPUT_FILE} ({len(orders_clean)} baris)")

    summary = orders_clean.groupby("kategori").agg(
        total_orders=("order_id", "count"),
        total_revenue=("total_harga", "sum"),
        avg_revenue=("total_harga", "mean"),
    ).round(0)
    summary.to_csv(REPORT_FILE)
    print(f"\n=== SUMMARY PER KATEGORI ===\n{summary}")
    print(f"\nSummary disimpan: {REPORT_FILE}")
    return orders_clean, summary


if __name__ == "__main__":
    orders, products = extract()
    orders = transform(orders)
    orders = validate(orders)
    load(orders)

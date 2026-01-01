from django.shortcuts import render
import pandas as pd
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent.parent

def dashboard_view(request):
    df = pd.read_csv(BASE_DIR / 'data' / 'car price data.csv')

    # Filter
    fuel = request.GET.get('fuel')
    if fuel:
        df = df[df['Fuel_Type'] == fuel]

    # KPIs
    kpis = {
        "total_cars": len(df),
        "avg_price": round(df['Selling_Price'].mean(), 2) if len(df) else 0,
        "max_price": df['Selling_Price'].max() if len(df) else 0,
    }

    # -------------------------
    # 1️⃣ Avg Selling Price by Fuel
    fuel_price = df.groupby('Fuel_Type')['Selling_Price'].mean().round(2)

    # -------------------------
    # 2️⃣ Crosstab: Fuel vs Transmission (COUNT)
    fuel_trans = pd.crosstab(df['Fuel_Type'], df['Transmission'])

    # -------------------------
    # 3️⃣ Crosstab: Fuel vs Seller Type (COUNT)
    fuel_seller = pd.crosstab(df['Fuel_Type'], df['Seller_Type'])

    # -------------------------
    # 4️⃣ Pivot: Avg Selling & Present Price
    price_pivot = (
        df.pivot_table(
            index='Fuel_Type',
            columns='Transmission',
            values=['Selling_Price', 'Present_Price'],
            aggfunc='mean'
        )
        .round(2)
    )

    context = {
        "kpis": kpis,

        # Chart 1
        "fuel_labels": json.dumps(fuel_price.index.tolist()),
        "fuel_values": json.dumps(fuel_price.values.tolist()),

        # Chart 2
        "fuel_trans_labels": json.dumps(fuel_trans.index.tolist()),
        "fuel_trans_manual": json.dumps(fuel_trans['Manual'].tolist() if 'Manual' in fuel_trans else []),
        "fuel_trans_auto": json.dumps(fuel_trans['Automatic'].tolist() if 'Automatic' in fuel_trans else []),

        # Chart 3
        "fuel_seller_labels": json.dumps(fuel_seller.index.tolist()),
        "fuel_seller_dealer": json.dumps(fuel_seller['Dealer'].tolist() if 'Dealer' in fuel_seller else []),
        "fuel_seller_individual": json.dumps(fuel_seller['Individual'].tolist() if 'Individual' in fuel_seller else []),

        "fuel_list": df['Fuel_Type'].unique(),
        "years": sorted(df['Year'].unique()),
    }

    return render(request, "dashboard/dashboard.html", context)


def summary_view(request):
    df = pd.read_csv(BASE_DIR/'data'/'car price data.csv')

    # Pivot table: Fuel vs Transmission
    table = (
        df.pivot_table(
            index='Fuel_Type',
            columns='Transmission',
            values='Selling_Price',
            aggfunc='mean'
        )
        .round(2)
        .reset_index()
    )

    return render(request, "dashboard/summary.html", {
        "table": table.to_html(classes='table table-bordered', index=False)
    })

def data_view(request):
    df = pd.read_csv(BASE_DIR/'data'/'car price data.csv')

    # Year filter
    year = request.GET.get('year')
    if year:
        df = df[df['Year'] == int(year)]

    return render(request, "dashboard/data.html", {
        "data": df.head(100).to_html(classes='table table-striped', index=False),
        "years": sorted(df['Year'].unique())
    })

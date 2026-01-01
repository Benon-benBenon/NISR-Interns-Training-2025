![DashBoard Picture](https://github.com/Benon-benBenon/NISR-Interns-Training-2025/blob/main/dashboard.png)

*If you want to have this dashboard, please follow the steps as mentioned below:*

# **Firtst Method**
---

### `STEP 1:` Install necessary library
### copy and paste the following command:

```bash
pip install numpy
pip install pandas
pip install Django
```

### `STEP 2:` Create Django project & app

```bash
django-admin startproject car_dashboard
cd car_dashboard
python manage.py startapp dashboard
```
### `STEP 3:` Add/register your `app` to the `project` inside setting.py file under `INSTALLED_APPS` by adding this in a given list of apps:

```bash
'dashboard'
```
### `STEP 4:` Inside setting.py register templates under `TEMPLATES` inside empty `[]` paste the following

```bash
BASE_DIR / 'templates'
```

### `STEP 5:` Inside `dashboard` app create file and name it `urls.py` the paste the following command:

```bash
# dashboard/urls.py
from django.urls import path
from .views import dashboard_view, summary_view, data_view

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('summary/', summary_view, name='summary'),
    path('data/', data_view, name='data'),
]

```

### `STEP 6:` Inside `dashboard` app. add the following command in the file called `views.py`

```bash
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

```

### `STEP 7:` Inside `car_dashboard` project,`urls.py` copy and paste the following commands:

```bash
from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('dashboard.urls')),
]
```

### `STEP 8:` Go to Desktop where in the folder you created in working directory `(directory containing manage.py)`, then add these unzipped folders I sent to you

```bash
templates folder
data folder
```

### `STEP 9:` Then in the terminal inside `working directory` run the following command.
```bash
python manage.py runserver
```
---
---
# **Second Method**
---
### `STEP 1:` Install necessary library
### copy and paste the following command:

```bash
pip install numpy
pip install pandas
pip install Django
```
### `STEP 2:` Clone the project and then open cloned directory then delete a `Jupyter notebook` file.

```bash
https://github.com/Benon-benBenon/NISR-Interns-Training-2025.git
```
##### **And then open that directory in `code editor` (eg, VS Code, etc)** [for Datasgboard] but if you want to learn basic python, please keep and consider `Juyter notebook file`.

### `STEP 3:` Then in the terminal inside `working directory` run the following command.
```bash
python manage.py runserver
```
---
### END.
### You will see your dashboard.
---

 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load dataset
df = pd.read_csv("Data/mg_car_sales_2025.csv")

print("Original Dataset:", df.shape)

# 2. Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# 3. Remove duplicate records
df = df.drop_duplicates()

# 4. Remove extra spaces
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].str.strip()

# 5. Convert columns into numeric format
df["units_sold"] = pd.to_numeric(
    df["units_sold"], errors="coerce"
)

df["estimated_revenue_inr_crore"] = pd.to_numeric(
    df["estimated_revenue_inr_crore"], errors="coerce"
)

# 6. Remove rows with missing sales values
df = df.dropna(
    subset=["units_sold", "estimated_revenue_inr_crore"]
)

# 7. Check cleaned data
print("\nCleaned Dataset:", df.shape)

print("\nRemaining Missing Values:")
print(df.isnull().sum())

# 8. Save cleaned dataset
df.to_csv("Data/cleaned_data.csv", index=False)

print("\nData Cleaning Completed Successfully!")


# ==================================
# STEP 3: BUSINESS DATA ANALYSIS
# ==================================

print("\n========== MG CAR SALES ANALYSIS ==========")

# 1. Total cars sold
total_cars = df["units_sold"].sum()
print("\nTotal Cars Sold:", total_cars)

# 2. Total estimated revenue
total_revenue = df["estimated_revenue_inr_crore"].sum()
print("Total Estimated Revenue:", round(total_revenue, 2), "Crore")

# 3. Best-selling car model
model_sales = df.groupby("model")["units_sold"].sum()
best_model = model_sales.idxmax()

print("\nBest-Selling Model:", best_model)
print("Units Sold:", model_sales.max())

# 4. Model-wise sales
print("\nModel-Wise Sales:")
print(model_sales.sort_values(ascending=False))

# 5. Month-wise sales
monthly_sales = df.groupby("month_number")["units_sold"].sum()

print("\nMonth-Wise Sales:")
print(monthly_sales)

# 6. Fuel type analysis
fuel_sales = df.groupby("fuel_type")["units_sold"].sum()

print("\nFuel Type Sales:")
print(fuel_sales.sort_values(ascending=False))

# ==================================
# STEP 4: DATA VISUALIZATION
# ==================================

from pathlib import Path

# Create Charts folder if it doesn't exist
Path("Charts").mkdir(exist_ok=True)

# Chart 1: Model-wise sales
plt.figure(figsize=(10, 6))
model_sales = df.groupby("model")["units_sold"].sum().sort_values(ascending=False)
sns.barplot(x=model_sales.index, y=model_sales.values)
plt.title("MG Model-Wise Sales - 2025")
plt.xlabel("Car Model")
plt.ylabel("Units Sold")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("Charts/model_sales.png")
plt.show()

# Chart 2: Monthly sales trend
plt.figure(figsize=(10, 6))
monthly_sales = df.groupby("month_number")["units_sold"].sum()
sns.lineplot(x=monthly_sales.index, y=monthly_sales.values, marker="o")
plt.title("Monthly Sales Trend - 2025")
plt.xlabel("Month Number")
plt.ylabel("Units Sold")
plt.xticks(range(1, 13))
plt.tight_layout()
plt.savefig("Charts/monthly_sales.png")
plt.show()

# Chart 3: Fuel type sales
plt.figure(figsize=(8, 6))
fuel_sales = df.groupby("fuel_type")["units_sold"].sum()
plt.pie(fuel_sales.values, labels=fuel_sales.index, autopct="%1.1f%%")
plt.title("Sales by Fuel Type")
plt.tight_layout()
plt.savefig("Charts/fuel_type_sales.png")
plt.show()

# Chart 4: Revenue by car model
plt.figure(figsize=(10, 6))
revenue = df.groupby("model")["estimated_revenue_inr_crore"].sum().sort_values(ascending=False)
sns.barplot(x=revenue.index, y=revenue.values)
plt.title("Estimated Revenue by MG Model")
plt.xlabel("Car Model")
plt.ylabel("Estimated Revenue (INR Crore)")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("Charts/revenue_by_model.png")
plt.show()

# Chart 5: Vehicle segment sales
plt.figure(figsize=(8, 6))
segment_sales = df.groupby("vehicle_segment")["units_sold"].sum().sort_values(ascending=False)
sns.barplot(x=segment_sales.index, y=segment_sales.values)
plt.title("Sales by Vehicle Segment")
plt.xlabel("Vehicle Segment")
plt.ylabel("Units Sold")
plt.tight_layout()
plt.savefig("Charts/segment_sales.png")
plt.show()

print("\nAll 5 charts saved successfully in the Charts folder!")

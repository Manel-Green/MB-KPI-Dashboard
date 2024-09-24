import pandas as pd

df = pd.read_csv("/Users/manelrahmouni/Documents/Dashboard KPI/OR_Sales_KPI copy.csv")
print(df)

df1 = df.sort_values(["order_year", "order_month"])
print(df1)
df1= df1.groupby(["order_year", "order_month"])["count"].sum().reset_index(name = "Sum")
print(df1)
df1["YTD Sales"] = df1["Sum"].cumsum()
print(df1)

print(df1["YTD Sales"].values[3])
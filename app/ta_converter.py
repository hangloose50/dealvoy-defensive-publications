from app import csv

with open("multi_category_asins.csv", newline="", encoding="utf-8") as infile, open("ta_ready_asins.csv", "w", newline="", encoding="utf-8") as outfile:
    reader = csv.DictReader(infile)
    writer = csv.writer(outfile)
    writer.writerow(["ASIN"])

    for row in reader:
        writer.writerow([row["ASIN"]])

print("📦 ASINs exported to ta_ready_asins.csv for Tactical Arbitrage upload.")
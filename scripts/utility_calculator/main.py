#!/usr/bin/env python3

from utilities.appconfig import appconfig
from utilities.chart import Chart
from decimal import Decimal


def main():
    # Get Script Config
    args, cfg = appconfig()

    # Set Data Trackers
    meta, data = {}, {}
    meta["amounts"], meta["total"] = {}, {}
    meta["total"]["amount"] = Decimal(0)
    meta["total"]["sqft"] = Decimal(0)

    # Declare Total Trackers
    for key, value in args:
        meta["amounts"][key] = value
        meta["total"]["amount"] += value

    # Get Square Feet for Entities
    for key, value in cfg.entities:
        meta["total"]["sqft"] += value.square_feet
        data[key] = {}
        data[key]["sqft"] = value.square_feet
        data[key]["split"] = value.split
        data[key]["exemptions"] = sum(
            [meta["amounts"].get(x, 0) for x in value.exemptions]
        )

    # Track Data for Table
    headers = ["Entity", "Split", "Total", "Per Person"]
    table = []

    for key, value in data.items():
        # Calculate Weights and Amounts
        bill_amount = meta["total"]["amount"] - data[key]["exemptions"]
        data[key]["weight"] = Decimal(
            data[key]["sqft"] / meta["total"]["sqft"]
        )
        data[key]["total"] = Decimal(
            bill_amount * data[key]["weight"]
        )
        data[key]["total_per"] = Decimal(
            data[key]["total"] / data[key]["split"]
        )

        # Track Entity Data
        table.append([
            key.title(),
            data[key]['split'],
            f"${round(data[key]['total'], 2)}",
            f"${round(data[key]['total_per'], 2)}",
        ])

    # Print Table
    table = Chart(headers, table)
    print(table)


if __name__ == "__main__":
    main()

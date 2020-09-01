from typing import List


def matrix_table(
    headers: List[str],
    table: List[str],
    align: str = "center"
) -> str:
    # Init Column Length Map
    columns = {}

    # Ensure Headers Match Table Sublists
    for sublist in table:
        if len(sublist) != len(headers):
            raise Exception("headers do match the length of table items")
        else:
            for i in range(len(sublist)):
                # Determine Column Length
                data_len = len(str(sublist[i]))
                if columns.get(i) is None:
                    columns[i] = data_len

                # Adjust for Headers
                if len(headers[i]) > columns[i]:
                    columns[i] = len(headers[i])

    # Alignment and Delimiters
    delims = {
        "down_horizontal": u"\u2500\u252C\u2500",
        "horizontal": u"\u2500",
        "vertical": u" \u2502 ",
        "vertical_horizontal": u"\u2500\u253C\u2500",
        "up_horizontal": u"\u2500\u2534\u2500",
    }
    alignment = {
        "center": "^",
        "left": "<",
        "right": ">",
    }

    # Build Format Template Slots
    t_row, t_header, t_border = [], [], []
    for i in range(len(headers)):
        t_row.append("{{{index}:{alignment}{padding}}}".format(
            index=i,
            alignment=alignment.get(align, "^"),
            padding=columns[i]
        ))
        t_header.append("{{{index}:{alignment}{padding}}}".format(
            index=i,
            alignment=alignment.get("center"),
            padding=columns[i]
        ))
        t_border.append(delims["horizontal"] * (columns[i]))

    # Build Full Format Tempaltes
    t_row = delims["vertical"].join(t_row)
    t_header = delims["vertical"].join(t_header)

    # Initialize Chart
    chart = "{topline}\n{headers}\n{border}\n".format(
        topline=delims["down_horizontal"].join(t_border),
        headers=t_header.format(*headers),
        border=delims["vertical_horizontal"].join(t_border)
    )

    # Construct String Table
    for sublist in table:
        chart = "".join([chart, t_row.format(*sublist), "\n"])
    else:
        chart = "".join([chart, delims["up_horizontal"].join(t_border)])

    return chart

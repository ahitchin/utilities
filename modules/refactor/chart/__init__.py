from typing import Dict, List


class NoInstance(type):
    """Metaclass to call class.__call__ instead of __new__ and __init__."""
    def __call__(
        cls,
        headers: List[str],
        table: List[str],
        align: str = "center"
    ) -> str:
        """When class is instantiated, only call the cls.__call__."""
        return cls.__call__(cls, headers, table, align)

    @property
    def alignment(self) -> Dict[str, str]:
        return {
            "center": "^",
            "left": "<",
            "right": ">",
        }

    @property
    def delims(self) -> Dict[str, str]:
        return{
            "down_horizontal": u"\u2500\u252C\u2500",
            "horizontal": u"\u2500",
            "vertical": u" \u2502 ",
            "vertical_horizontal": u"\u2500\u253C\u2500",
            "up_horizontal": u"\u2500\u2534\u2500",
            "down_right": u"\u250C\u2500",
            "down_left": u"\u2500\u2510",
            "up_right": u"\u2514\u2500",
            "up_left": u"\u2500\u2518",
            "vertical_right": u"\u251C\u2500",
            "vertical_left": u"\u2500\u2524",
        }


class Chart(object, metaclass=NoInstance):
    def __call__(
        self,
        headers: List[str],
        table: List[str],
        align: str = "center"
    ) -> str:
        """Create a table from a list of headers and matrix of data.

        :param headers: list of strings with headers for columns
        :param table: matrix of data to fill table with
        :param align: alignment of strings inside cells
        :return str: table representation of headers/matrix
        """
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

        # Build Format Template Slots
        t_row, t_header, t_border = [], [], []
        for i in range(len(headers)):
            t_header.append("{{{index}:{alignment}{padding}}}".format(
                index=i,
                alignment=self.alignment.get("center"),
                padding=columns[i]
            ))
            t_border.append(self.delims["horizontal"] * (columns[i]))
            t_row.append("{{{index}:{alignment}{padding}}}".format(
                index=i,
                alignment=self.alignment.get(align, "^"),
                padding=columns[i]
            ))

        # Build Full Format Tempaltes
        t_row = self.delims["vertical"].join(t_row)
        t_header = self.delims["vertical"].join(t_header)

        # Initialize Chart
        chart = "{topline}\n{headers}\n{border}\n".format(
            topline="{0}{1}{2}".format(
                self.delims["down_right"],
                self.delims["down_horizontal"].join(t_border),
                self.delims["down_left"]
            ),
            headers="{0}{1}{2}".format(
                self.delims["vertical"][1:],
                t_header.format(*headers),
                self.delims["vertical"][:-1],
            ),
            border="{0}{1}{2}".format(
                self.delims["vertical_right"],
                self.delims["vertical_horizontal"].join(t_border),
                self.delims["vertical_left"],
            )
        )

        # Construct String Table
        for sublist in table:
            chart = "{chart}{lborder}{row}{rborder}\n".format(
                chart=chart,
                lborder=self.delims["vertical"][1:],
                row=t_row.format(*sublist),
                rborder=self.delims["vertical"][:-1],
            )
        else:
            chart = "{chart}{lborder}{row}{rborder}".format(
                chart=chart,
                lborder=self.delims["up_right"],
                row=self.delims["up_horizontal"].join(t_border),
                rborder=self.delims["up_left"],
            )

        return chart

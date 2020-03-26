def create_table(headers, table, separator=None):
    #Get Headers Length
    headers_length = len(headers)

    #Column Length Map
    column_lengths = dict()
    for i in range(len(headers)):
        column_lengths[str(i)] = None

    #Ensure Headers Match Table Sublists
    for sublist in table:
        if len(sublist) != headers_length:
            raise Exception("Headers do not match the length of table items")
        else:
            for i in range(len(sublist)):
                index_str = str(i)
                sublist_str = str(sublist[i])
                if column_lengths[index_str] == None:
                    column_lengths[index_str] = len(sublist_str)
                elif len(sublist_str) > column_lengths[index_str]:
                    column_lengths[index_str] = len(sublist_str)

    #Change Length if Headers Bigger than Row Data
    for i in range(len(headers)):
        if len(headers[i]) > column_lengths[str(i)]:
            column_lengths[str(i)] = len(headers[i])

    #Declare Final String
    print_str = ""
    column_delimiter = separator if separator else "   "
    delimiter_length = len(column_delimiter)
    header_delimiter = " " * delimiter_length

    #Create Row Template
    row_template = column_delimiter.join(["{{{0}:<{1}}}".format(x, column_lengths[str(x)]) for x in range(len(headers))])
    header_template = header_delimiter.join(["{{{0}:<{1}}}".format(x, column_lengths[str(x)]) for x in range(len(headers))])
    border_template = header_delimiter.join(["-" * column_lengths[str(x)] for x in range(len(headers))])

    #Add Headers
    print_str += "{0}\n{1}\n".format(header_template.format(*headers), border_template)

    #Construct String
    for i, sublist in enumerate(table):
        print_str += row_template.format(*sublist)
        if (i+1) < len(table):
            print_str += "\n"

    return print_str
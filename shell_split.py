def shell_split(string, braces=False, brackets=False, parentheses=False):
    """Splits String in UNIX Style Manner
    """
    from string import whitespace
    def contains_whitespace(string):
        for char in string:
            if char in whitespace:
                return True
        return False
    
    #Tracking Variables
    opener  = []    #Track Defined Open Characters
    parts   = []    #Track Parts of Input String
    tracked = ""    #Track Current String
    counter = 0     #Track Iterations

    #Open/Release Character Map
    release = {
        "\"": "\"",
        "'": "'"
    }

    #Update With Extra Openers (Braces/Brackets/Parentheses)
    if braces == True:
        tmp = {"{": "}"}
        release.update(tmp)
    if brackets == True:
        tmp = {"[": "]"}
        release.update(tmp)
    if parentheses == True:
        tmp = {"(": ")"}
        release.update(tmp)

    while counter <= len(string):
        #On Last Iteration
        if counter == len(string):
            #Prepend Unclosed Char to Tracked if 'opener' has Items
            if len(opener) > 0:
                unclosed_char = opener.pop()
                tracked = unclosed_char + tracked

            #Append to String Parts
            if len(tracked) > 0:
                parts.append(tracked)
            break
        else:
            #Get Character and Increment Counter
            char = string[counter]
            counter += 1

        #On All Iters Except Last
        if len(opener) > 0:
            #Release String if Current Chacter is a Close Character
            if char == release[opener[0]]:
                parts.append(tracked)
                opener.pop()
                tracked = ""
            else:
                #Append Character to 'tracked'
                tracked = tracked + char
        elif char in release.keys():
            #If Char is an Open Character, Append Open Char to 'opener'
            opener.append(char)

            #Reset 'tracked'
            tracked = ""
        elif char.isspace():
            #If Whitespace in String
            if contains_whitespace(tracked) != True:
                has_no_space = True
            else:
                has_no_space = False

            #If String is Empty
            is_not_empty = True if len(tracked) > 0 else False

            #Append If Previous Chars are not Whitespace 
            if all([has_no_space, is_not_empty]):
                parts.append(tracked)
                tracked = ""
        else:
            #Append Character to 'tracked'
            tracked = tracked + char

    return parts

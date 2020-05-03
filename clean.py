# returns unparenthesized character string
def balanced_parens(s):
    open_parens = len(s) - len(s.replace("(", ""))
    closed_parens = len(s) - len(s.replace(")", ""))

    if (open_parens == closed_parens):
        return True
    else:
        return False
        


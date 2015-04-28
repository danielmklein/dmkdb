

class ResultWriter(object):

    def __init__(self, output):
        self.output = output

    '''
    Write given result to whatever output we've specificed.
    '''
    def write_result(self, col_names, rows):
        if (col_names is None or rows is None):
            return

        header = ""
        num_underscores = 0
        for col in col_names:
            header += "{0:>7}".format(col)
            num_underscores += 7
        header += "\n"
        header += "-" * num_underscores + "\n"

        self.output.write(header)

        for row in rows:
            row_string = "".join("{0: >7}".format(k) for k in row) + "\n"
            self.output.write(row_string)

        self.output.write("\n")

        return
    # end write_result
            
                

        
        

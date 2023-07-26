

class QSConfig:
    def __init__(self,filename) -> None:
        self.filename = filename
        self.configuration = {}
        self.read_input_file()

    #read an qsc_in.* file and convert it to a python dictionary 
    def read_input_file(self):
        configuration = {}
        current_dir = None
        #open the file
        with open(self.filename, "r") as f:
            for line in f:
                #ignore comments
                if line[0] == "#" or line == "\n":
                    continue
                
                # save set parameters to the dictionary
                param_parts = line.split("=")
                parameter = param_parts[0].strip()
                
                #print(len(param_parts))
                if(len(param_parts) < 2):
                    #this is a parent dictionary
                    configuration[parameter] = {}
                    current_dir = parameter
                else:
                    #print(param_parts)
                    #convert parameter value to the correct type of object
                    value = param_parts[1].strip()
                    print(parameter)
                    print(value)
                    
                    if  value.isnumeric():
                        #dealing with int type
                        value = int(value)

                    elif '[' in value:
                        #dealing with arr type
                        value = value[1:-1]
                        value = value.split(", ")
                        value = [float(x) for x in value]

                    elif value.replace(".", "", 1).isdigit():
                        # decimal
                        value = float(value)
                    else:
                        #for now lets asssume this case means a string
                        value = value.replace('"', "").replace("'", "").rstrip()
                        if value == "true":
                            value = True
                        elif value == "false":
                            value = False
                        
                    print(type(value))
                    #set the parameter either top level or in the sub level
                    if(not current_dir):
                       configuration[parameter] = value
                    else:
                        configuration[current_dir][parameter] = value
                #print(configuration)
        self.configuration = configuration
        print(configuration)


if __name__ == "__main__":
    config = QSConfig("qsc_in.random_scan_small")



class QSConfig:
    def __init__(self,filename) -> None:
        self.filename = filename
        self.configuration = {}
        self.read_input_file()


    def __getitem__(self, key):
        if key in self.configuration.keys():
            return self.configuration[key]
        else:
            for maybe_dir in self.configuration.keys():
                if type(self.configuration[maybe_dir]) == dict:
                    if key in self.configuration[maybe_dir].keys():
                        return self.configuration[maybe_dir][key]
                                    
            raise KeyError(f"'QSConfig' object does not have a key named '{key}'")
    
    def __setitem__(self, key, value):
        if key in self.configuration.keys():
            self.configuration[key] = value
        else:
            for maybe_dir in self.configuration.keys():
                if type(self.configuration[maybe_dir]) == dict:
                    print(self.configuration[maybe_dir].keys())
                    if key in self.configuration[maybe_dir].keys():
                        #print(self.configuration[maybe_dir].keys())
                        self.configuration[maybe_dir][key] = value
                        return
            raise KeyError(f"'QSConfig' object does not have an key named '{key}'")
    

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
                    #print(parameter)
                    #print(value)
                    
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
                        try:
                            value = float(value)
                        except:  
                            #for now lets asssume this case means a string
                            value = value.replace('"', "").replace("'", "").rstrip()
                            if value == "true":
                                value = True
                            elif value == "false":
                                value = False
                        
                    #print(type(value))
                    #set the parameter either top level or in the sub level
                    if(not current_dir):
                       configuration[parameter] = value
                    else:
                        configuration[current_dir][parameter] = value
                #print(configuration)
        self.configuration = configuration
        #print(configuration)

    def write_input_file(self,output_filename, tabbed=False):
        indentation = ""
        if tabbed:
            indentation = "\t"

        with open(output_filename, "w") as writer:
            writer.write("# This is a auto-generated input file from NEARSURVEY. Any errors here most likely indicate a problem with the QSC_Config Class\n")

            # we traverse through all the keys writing out the subdirectories if needed
            for key in self.configuration.keys():

                if type(self.configuration[key]) != dict:
                    # there does not exists a subdirectory, toplevel variable
                    if type(self.configuration[key]) == str:
                        #top level variables do not need indentation
                        writer.write(f"\n{key} = '{self.configuration[key]}'\n")
                    elif type(self.configuration[key]) == bool:
                            if self.configuration[key]:
                                writer.write(f'{key} = true\n')
                            else:
                                 writer.write(f'{key} = false\n')
                    else:
                        writer.write(f"\n{key} = {self.configuration[key]}\n")
                else:
                    
                    # put heading and then two newlines (this seems standard across qsc inputs)
                    writer.write(f"\n{key}\n\n")
                    current_dir = key
                    for sub_key in self.configuration[key]:
                        #sub level variables need indentation
                        # in regcoil files there is the option 'load_bnorm' which must be outputted as .t. without quotes
                        if type(self.configuration[key][sub_key]) == str and self.configuration[key][sub_key][0] != ".":

                            writer.write(f"{indentation}{sub_key} = '{self.configuration[key][sub_key]}'\n")
                        elif type(self.configuration[key][sub_key]) == bool:
                            if self.configuration[key][sub_key]:
                                writer.write(f'{indentation}{sub_key} = true\n')
                            else:
                                 writer.write(f'{indentation}{sub_key} = false\n')
                        else:
                            writer.write(f"{indentation}{sub_key} = {self.configuration[key][sub_key]}\n")
                        
        print(f"Wrote to output file: {output_filename}")


if __name__ == "__main__":
    config = QSConfig("regcoil_in.TEST")
    print(config.configuration)
    config['bnorm_filename'] = 'testfile_bnorm'
    config['nescin_filename'] = 'testfile_nescin'
    config['wout_filename'] = 'testfile_wout'
    #config['general_option'] = "multiopt"
    config.write_input_file("regcoil_in_EXPERIMENT.TEST", tabbed=True)
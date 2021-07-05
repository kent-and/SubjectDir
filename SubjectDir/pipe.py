
import os

class Pipe: 
    def __init__(self, function, input_files, output_files, outputdir, parameters): 
        self._function = function
        self._input_files = input_files
        self._output_files = output_files
        self._output_dir = outputdir
        self._parameters = parameters
        self._counter = 0 

    def counter(self): return self.counter

    def run(self, root, dirs, files, max_counter):
        print ("in pipe.run ", root, dirs, files, max_counter)
        print ("in pipe.run ",  files)
        if self._counter < max_counter:  
            print ("input files ", self._input_files)
            found = set(files).intersection(set(self._input_files)) 
            print ("input files found ", found)
            output_found = set(files).intersection(set(self._output_files))
            print ("output files found ", output_found)
            if len(output_found) == len(self._output_files): return 0  
            elif len(found) == len(self._input_files): 
                print ("FOUND ", found) 
                odir = root + "/" + self._output_dir
                if not os.path.isdir(odir): os.mkdir(odir)
                self._function(root, self._input_files, odir, self._output_files, self._parameters)
                self._counter += 1 

         

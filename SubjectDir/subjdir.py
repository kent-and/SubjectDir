

class SubjectDir: 
    def __init__(self, subject_dir_path): 
        self.subject_dir_path = subject_dir_path

    def run(self, pipes, pipeflags, num_subj):
        import os 
        for i, pipe in enumerate(pipes): 
            if pipeflags[i]:   
                for root, dirs, files in os.walk(self.subject_dir_path, topdown=False):
                    print (root, dirs, files) 
                    pipe.run(root, dirs, files, num_subj)
        


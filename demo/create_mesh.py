

import SubjectDir as subjd  

def create_stl(input_dir, input_files_dict, output_dir, output_files_dict, parameter_dict):
    import os  
    lh_pial = input_dir  + "/" + input_files_dict["lh.pial"]
    lh_stl  = output_dir + "/" + output_files_dict["lh.stl"]
    print ("mris_convert %s %s"% (lh_pial, lh_stl))   
    os.system("mris_convert %s %s"% (lh_pial, lh_stl))   

    rh_pial = input_dir  + "/" + input_files_dict["rh.pial"]
    rh_stl  = output_dir + "/" + output_files_dict["rh.stl"]
    print("mris_convert %s %s"% (rh_pial, rh_stl))   
    os.system("mris_convert %s %s"% (rh_pial, rh_stl))   
 

def create_mesh(input_dir, input_files_dict, output_dir, output_files_dict, parameter_dict):
    import SVMTK as svm
    # get input files 
    lh_file  = input_dir + "/" + input_files_dict["lh.stl"]
    rh_file  = input_dir + "/" + input_files_dict["rh.stl"]

    print ("inputfiles ", lh_file, " ", rh_file) 

    # create surfaces
    lh_surf = svm.Surface(lh_file)
    rh_surf = svm.Surface(rh_file)

    smap = svm.SubdomainMap()
    smap.add("10",1)
    smap.add("01",1)

    surface = [lh_surf, rh_surf]
    domain = svm.Domain(surface)

    Ns = parameter_dict["Ns"]   
    for N in Ns: 
        outputfile = output_dir + "/" + output_files_dict["Mesh"] % N
        print ("starting ", N, outputfile)
        domain.create_mesh(N) 
        domain.save(outputfile)



sd = subjd.SubjectDir("../../tmp/DataLocker")
print (dir(sd))
input_files_dict = {"lh.pial" : "lh.pial", "rh.pial" : "rh.pial"}
output_files_dict = {"lh.stl" : "lh.stl", "rh.stl" : "rh.stl"}
parameter_dict = { }
pipe1 = subjd.Pipe(create_stl, input_files_dict, output_files_dict, "fenics", parameter_dict)


input_files_dict = {"lh.stl" : "lh.stl", "rh.stl" : "rh.stl"}
output_files_dict = { "Mesh" : "Mesh%d.mesh" }   
parameter_dict = { "Ns" : [16, 32] }
pipe2 = subjd.Pipe(create_mesh, input_files_dict, output_files_dict, "", parameter_dict)

# run first pipe on 3 subjects
sd.run(pipes = [pipe1, pipe2], pipeflags=(1,0), num_subj = 3) 
# run second pipe on 3 subjects
sd.run(pipes = [pipe1, pipe2], pipeflags=(0,1), num_subj = 3) 




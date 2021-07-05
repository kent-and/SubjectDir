import os 
from dolfin import *
import SubjectDir as subjd  
import meshio 

def mesh_convert(input_dir, input_files_dict, output_dir, output_files_dict, parameter_dict):
    mesh = meshio.read(input_dir + "/" + input_files_dict["Mesh16.mesh"])
    meshio.dolfin.write(output_dir + "/" + output_files_dict["Mesh16.xml"], mesh)

    mesh = meshio.read(input_dir + "/" + input_files_dict["Mesh32.mesh"])
    meshio.dolfin.write(output_dir + "/" + output_files_dict["Mesh32.xml"], mesh)


def run_simulation(input_dir, input_files_dict, output_dir, output_files_dict, parameter_dict):

    for meshfile in input_files_dict.values():
        meshfile = input_dir + "/" + meshfile  
        print ("reading meshfile ", meshfile) 
        mesh = Mesh(meshfile) 
        V = FunctionSpace(mesh, "CG", 1) 

        u = TrialFunction(V)
        v = TestFunction(V)

        def boundary(x, on_boundary): return on_boundary

        bc = DirichletBC(V, Constant(0), boundary)

        a = inner(grad(u), grad(v))*dx 
        L = Constant(1)*v*dx 

        u = Function(V)
        solve(a==L, u, bc)

        print ("min ", u.vector().min())
        print ("max ", u.vector().max())

        f = File(meshfile[:-4]+"/u.pvd")
        f << u 



sd = subjd.SubjectDir(os.environ["SUBJECTS_DIR"])

print (dir(sd))
input_files_dict = {"Mesh16.mesh" : "Mesh16.mesh", "Mesh32.mesh": "Mesh32.mesh"}
output_files_dict = {"Mesh16.xml" : "Mesh16.xml", "Mesh32.xml": "Mesh32.xml"}
parameter_dict = { }
pipe1 = subjd.Pipe(mesh_convert, input_files_dict, output_files_dict, "", parameter_dict)




print (dir(sd))
input_files_dict = {"Mesh16.xml" : "Mesh16.xml", "Mesh32.xml": "Mesh32.xml"}
output_files_dict = {"u.pvd" : "u.pvd"}
parameter_dict = { }
pipe2 = subjd.Pipe(run_simulation, input_files_dict, output_files_dict, "", parameter_dict)

# run first pipe on 3 subjects
sd.run(pipes = [pipe1, pipe2], pipeflags=(1,0), num_subj = 3) 
# run second pipe on 3 subjects
sd.run(pipes = [pipe1, pipe2], pipeflags=(0,1), num_subj = 3) 





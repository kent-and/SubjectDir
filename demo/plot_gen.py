import pyvista as pv 
import SubjectDir as subjd  

def gen_pngs(input_dir, input_files_dict, output_dir, output_files_dict, parameter_dict):

    ufile = input_dir + "/" + input_files_dict["u.pvd"]
    u = pv.read(ufile)
    u_slice = u.slice(normal=(0,0,1))

    plotter = pv.Plotter(off_screen=True)
    plotter.camera_position = [(0,0,300), (0, 0, 0), (0, 0, 0)]
#        plotter.add_mesh_slice_orthogonal(u)
    plotter.add_mesh(u_slice)
    plotter.update_scalar_bar_range([0,300])
    plotter.screenshot(output_dir + "/" + output_files_dict["u.png"])


sd = subjd.SubjectDir("../../tmp/DataLocker")
print (dir(sd))
input_files_dict = {"u.pvd" : "u000000.vtu"}
output_files_dict = {"u.png" : "u.png"}
parameter_dict = { }
pipe1 = subjd.Pipe(gen_pngs, input_files_dict, output_files_dict, "", parameter_dict)


sd.run(pipes = [pipe1], pipeflags=(1,), num_subj = 3) 




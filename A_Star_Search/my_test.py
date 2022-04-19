import os
from student_impl.eid_xz7622 import A_Star_Search
eid = "xz7622"

for i in range(0,1):
    idx = i
    benchmark_path = f"benchmarks/example_{idx}.txt"
    output_root = "output"
    output_root = os.path.join(output_root, eid)
    if not os.path.isdir(output_root):
        os.mkdir(output_root)

    output_path = os.path.join(output_root, os.path.basename(benchmark_path))
    solver = A_Star_Search()
    solver.read_benchmark(benchmark_path)
    solution = solver.solve()
    solver.plot_solution(solution, os.path.join(output_root, f"example_{idx}_sol.png"))
    profiling = solver.profile(n_runs=3) # ignore memory for now. runtime will be graded
    solver.dump_output_file(*solution, *profiling, output_path)

    # read solutions
    # solution_path = f"output/xz7622/example_{idx}.txt"
    f_solution = open(f"output/xz7622/example_{idx}.txt", "r")
    solution_content = f_solution.readlines()

    f_testbench = open(f"benchmarks/example_{idx + 1}.txt", "a")
    # testbench_content = f_testbench.readlines()

    for j in range(1, len(solution_content)):
        print(j)
        if len(solution_content[j]) == 1:
            break
        else:
            if solution_content[j][0] == solution_content[j][2]: # verticle path, size_x = 1,
                new_block = "b1 " + str(solution_content[j][0]) + ' ' + str(min(solution_content[j][1], solution_content[j][3])) + ' 1 ' + str(abs(eval(solution_content[j][1]) - eval(solution_content[j][3])))
            else: # horizontal path, size_y = 1, 1=3
                # print(solution_content[j][0])
                # print(min(solution_content[j][0], solution_content[j][2]))
                # print(abs(eval(solution_content[j][0]) - eval(solution_content[j][2])))
                new_block = "b1 " + str(min(solution_content[j][0], solution_content[j][2])) + ' ' + str(solution_content[j][1]) + ' ' + str(abs(eval(solution_content[j][0]) - eval(solution_content[j][2]))) + ' 1'
            
            f_testbench.write(new_block)
    
    f_solution.close()
    f_testbench.close()

    # print(solution_content[1][0])
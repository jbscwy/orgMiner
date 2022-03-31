# # 将转换好的bpmn文件保存到指定目录
# from pm4py.visualization.bpmn.visualizer import save
# from pm4py.visualization.bpmn import visualizer as bpmn_visualizer
# import pm4py
#
# def save_bpmn_model(input_file_path,output_file_path):
#     log = pm4py.read_xes(input_file_path)
#     process_tree = pm4py.discover_tree_inductive(log)
#     bpmn_model = pm4py.convert_to_bpmn(process_tree)
#     parameters = bpmn_visualizer.Variants.CLASSIC.value.Parameters
#     gviz = bpmn_visualizer.apply(bpmn_model, parameters={parameters.FORMAT: "png"})
#     save(gviz,output_file_path)
#
#
# if __name__ == '__main__':
#     input_file_path=""
#     output_file_path=""
#     save_bpmn_model()
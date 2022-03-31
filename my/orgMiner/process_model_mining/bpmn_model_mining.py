import os
from os.path import join

import pm4py
from flask import Blueprint, session, render_template
from pm4py.visualization.bpmn.visualizer import save
from pm4py.visualization.bpmn import visualizer as bpmn_visualizer

# from my import APP_ROOT
from my.orgMiner import APP_ROOT
from my.orgMiner.forms import XesLogForm
from my.orgMiner.utilities import get_file_extension

bp = Blueprint('bpmn_model_mining', __name__)


xes_file=os.path.join(os.path.dirname(APP_ROOT),'orgMiner','.xes')
process_model_file=os.path.join(os.path.dirname(APP_ROOT),'static','process_model')

@bp.route('/bpmn_model_mining',methods=['GET','POST'])
def bpmn_model_mining():
    xes_log=XesLogForm()
    if xes_log.validate_on_submit():
        from werkzeug.utils import secure_filename
        # 客户端，获取上传的文件名
        fn_client = secure_filename(xes_log.f_log.data.filename)
        # 最近上传的文件名
        session['last_upload_xes_log'] = fn_client
        # 获取文件扩展名
        file_ext = get_file_extension(fn_client)
        fn_server = '{}.log.{}'.format(session.sid[:32], file_ext)
        # 将多个路径组合后返回
        xes_log.f_log.data.save(
            join(xes_file, fn_server)
        )
        output_file_path = join(process_model_file, str(fn_client) + ".png")
        save_bpmn_model(join(xes_file, fn_server),output_file_path)
        png_name=str(fn_client)+'.png'
        return render_template('process_model_mining.html',
                               has_xes_log=True,
                               xes_log=xes_log,
                               png_name=png_name)
    return render_template('process_model_mining.html',
                           has_xes_log=False,
                           xes_log=xes_log)





# 将转换好的bpmn文件保存到指定目录
def save_bpmn_model(input_file_path,output_file_path):
    log = pm4py.read_xes(input_file_path)
    process_tree = pm4py.discover_tree_inductive(log)
    bpmn_model = pm4py.convert_to_bpmn(process_tree)
    parameters = bpmn_visualizer.Variants.CLASSIC.value.Parameters
    gviz = bpmn_visualizer.apply(bpmn_model, parameters={parameters.FORMAT: "png"})
    save(gviz,output_file_path)
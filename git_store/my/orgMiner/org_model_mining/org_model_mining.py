import os
from os.path import join

from flask import *
from werkzeug.utils import secure_filename

from my.orgMiner import APP_ROOT
from my.orgMiner.forms import LogUploadForm, ResourceLogForm, OrganizeModelMiningAttributes
from my.orgMiner.new_index import clear_session_data
from my.orgMiner.org_model_mining.main import org_model_mining_function
from my.orgMiner.utilities import get_file_extension

bp = Blueprint('org_model_mining', __name__)


resource_log_file=os.path.join(os.path.dirname(APP_ROOT),'orgMiner','.resource')

@bp.route('/org_model_mining', methods=['GET','POST'])
def org_model_mining():

    resource_log=ResourceLogForm()
    if request.method=='GET':
        # 清除session数据，也就是说一个会话结束
        clear_session_data()
        # 渲染模板
        return render_template('org_model_mining.html',
                               has_event_log=False,
                               resource_log=resource_log,
                               )

    org_model_mining_attributes = OrganizeModelMiningAttributes()
    if resource_log.validate_on_submit() or org_model_mining_attributes.organization_model_mining_method.data not in ['',None]:
        if resource_log.validate_on_submit():
            # 获取上传的文件名
            fn_client = secure_filename(resource_log.f_log.data.filename)
            # 最近上传的文件名
            session['last_upload_resource_log_client'] = fn_client
            # 获取文件扩展名
            file_ext = get_file_extension(fn_client)
            print("file_ext:" + str(file_ext))
            # 服务器
            fn_server = '{}.log.{}'.format(session.sid[:32], file_ext)
            session['last_upload_resource_log_server'] = fn_server
            # 将多个路径组合后返回
            resource_log.f_log.data.save(
                join(resource_log_file, fn_server)
            )
            return render_template("org_model_mining.html",
                                   has_resource_log=True,
                                   org_model_mining_attributes=org_model_mining_attributes)
        else:
            if org_model_mining_attributes.organization_model_mining_method.data not in ['',None]:
                organization_model_mining_method=org_model_mining_attributes.organization_model_mining_method.data
                resource_similarity_method=org_model_mining_attributes.resource_similarity_method.data
                group_num_range=org_model_mining_attributes.group_num_range.data
                assign_execution_mode_method=org_model_mining_attributes.assign_execution_mode_method.data
                w1=org_model_mining_attributes.w1.data
                w2=org_model_mining_attributes.w2.data
                resource_log_path=join(resource_log_file, session['last_upload_resource_log_server'])
                log_info=org_model_mining_function(resource_log_path, organization_model_mining_method, resource_similarity_method, group_num_range,
                                 assign_execution_mode_method, w1, w2)
                session['org_model']=log_info['org_model']
                session['fitness'] = log_info['fitness']
                session['precision'] = log_info['precision']
                session['resource_functional_similarity'] = log_info['resource_functional_similarity']
                print('org_model'+str(session['org_model']))
                print('fitness' + str(session['fitness']))
                print('precision' + str(session['precision']))
                print('resource_functional_similarity' + str(session['resource_functional_similarity']))
                return redirect(url_for('visual_org_model.visual_org_model'))

    return render_template("org_model_mining.html",
                           has_resource_log=False,
                           resource_log=resource_log)


@bp.route('/reset_resource_log',methods=['GET'])
def reset_event_log():
    clear_session_data()
    return redirect(url_for('.org_model_mining'))





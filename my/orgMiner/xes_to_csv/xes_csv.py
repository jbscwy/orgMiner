import os
from os.path import join

from flask import *

from my.orgMiner import APP_ROOT
from my.orgMiner.forms import LogUploadForm
from my.orgMiner.new_index import clear_session_data
from my.orgMiner.utilities import get_file_extension
from my.orgMiner.xes_to_csv.xes_parse import dic_storage_log, generate_csv_file


bp = Blueprint('xes_csv', __name__)


xes_file=os.path.join(os.path.dirname(APP_ROOT),'orgMiner','.xes')
csv_file=os.path.join(os.path.dirname(APP_ROOT),'orgMiner','.csv')
@bp.route('/xes_to_csv', methods=['GET','POST'])
def index():
    reset_xes_log()
    log_upload_form = LogUploadForm()
    print("log_upload_form:"+str(log_upload_form.validate_on_submit()))
    print("temp:" + str(xes_file))
    # 验证上传表单
    if log_upload_form.validate_on_submit():
        from werkzeug.utils import secure_filename
        # 客户端，获取上传的文件名
        fn_client = secure_filename(log_upload_form.f_log.data.filename)
        print("fn_client:" + str(fn_client))
        # 最近上传的文件名
        session['last_upload_event_log_xes'] = fn_client
        print("session['last_upload_event_log_xes']:"+session['last_upload_event_log_xes'])
        # 获取文件扩展名
        file_ext = get_file_extension(fn_client)
        fn_server = '{}.log.{}'.format(session.sid[:32], file_ext)
        # 将多个路径组合后返回
        log_upload_form.f_log.data.save(
            join(xes_file, fn_server)
        )
        fn_file = join(xes_file,fn_server)
        print("fn_file:"+str(fn_file))
        fout_file=join(csv_file,str(fn_client)+".csv")
        print("fout_file:" + str(fout_file))
        attributes, log_dic = dic_storage_log(fn_file)
        generate_csv_file(fout_file, attributes, log_dic)
        session['fout_file']=fout_file
        if os.path.isfile(os.path.join(csv_file, str(fn_client)+".csv")):
            return send_file(fout_file,as_attachment=True)

        # log_info = {
        #     'filename': session['last_upload_event_log_xes']
        # }
        # if request.method == 'POST':
        #     flash('Successfully converse xes log file ' +
        #         '<mark>{}</mark>'.format(log_info['filename']),
        #         category='success')
    return render_template('xes_csv.html',
                           log_upload_form=LogUploadForm())


def reset_xes_log():
    clear_session_data()


@bp.route('/clean')
def clean():
    clear_session_data()
    return redirect(url_for('.xes_to_csv'))

# @bp.route('/download/<filename>')
# def download(filename):
#     print("结果："+str(isinstance(filename,str)))
#     if os.path.isfile(os.path.join(csv_file, filename)):
#         print("filename：" + filename+"...")
#         return send_from_directory(csv_file,filename,as_attachment=False)
#
#
# @bp.route('/test')
# def test():
#     print('1')
#     filename="orgMiner\\.csv\\Running-example.xes.csv"
#     return send_file(filename,as_attachment=True,attachment_filename='Running-example.csv')



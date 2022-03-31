from os.path import join

from flask import Blueprint, session, flash, redirect, url_for, render_template, request
from werkzeug.utils import secure_filename

from my.orgMiner import APP_ROOT
from my.orgMiner.forms import EventLogForm, GetResourceProperties, Test
import os

from my.orgMiner.new_index import clear_session_data
from my.orgMiner.resource_log.event_to_resource import event_to_resource
from my.orgMiner.utilities import get_file_extension

bp = Blueprint('get_resource_log', __name__)
model_file=os.path.join(os.path.dirname(APP_ROOT), 'orgMiner', '.event','GoogleNews-vectors-negative300.bin')
event_log_path = os.path.join(os.path.dirname(APP_ROOT), 'orgMiner', '.event')
resource_log_path = os.path.join(os.path.dirname(APP_ROOT), 'orgMiner', '.resource')
timestamp_format = '%d-%m-%Y:%H.%M'

@bp.route('/upload_event_log',methods=['GET','POST'])
def upload_event_log():
    # 上传事件日志
    event_log_upload_form = EventLogForm()
    if request.method == 'GET':
        # 清除session数据，也就是说一个会话结束
        clear_session_data()
        # 渲染模板
        return render_template('get_resource_log.html',
                               has_event_log=False,
                               event_log_upload_form=event_log_upload_form,
                               )
    elif request.method=='POST':
        get_resource_properties = GetResourceProperties()
        if event_log_upload_form.validate_on_submit() or get_resource_properties.resource_column.data not in ['',None]:
            if event_log_upload_form.validate_on_submit():
                # 获取上传的文件名
                fn_client = secure_filename(event_log_upload_form.f_log.data.filename)
                # 最近上传的文件名
                session['last_upload_event_log_client'] = fn_client
                # 获取文件扩展名
                file_ext = get_file_extension(fn_client)
                print("file_ext:" + str(file_ext))
                # 服务器
                fn_server = '{}.log.{}'.format(session.sid[:32], file_ext)
                session['last_upload_event_log_server'] = fn_server
                # 将多个路径组合后返回
                event_log_upload_form.f_log.data.save(
                    join(event_log_path, fn_server)
                )
                return render_template('get_resource_log.html',
                                       has_event_log=True,
                                       get_resource_properties=get_resource_properties
                                       )
            else:
                if get_resource_properties.resource_column.data in ['',None]:
                    print("resource_column:" + str(get_resource_properties.resource_column.data))
                    return render_template('get_resource_log.html',
                                           has_event_log=True,
                                           get_resource_properties=get_resource_properties
                                           )
                else:
                    resource_column = get_resource_properties.resource_column.data
                    print("resource_column:" + str(resource_column))

                    case_type_column = get_resource_properties.case_type.data
                    print("case_type:" + str(case_type_column))

                    activity_column = get_resource_properties.activity_column.data
                    print("activity_column:" + str(activity_column))

                    activity_type_method = get_resource_properties.get_activity_type_method.data
                    print("activity_type_method:" + str(activity_type_method))

                    activity_type_group_num = get_resource_properties.activity_type_group_num.data
                    print("activity_type_group_num:" + str(activity_type_group_num))

                    timestamp_column = get_resource_properties.timestamp_column.data
                    print("timestamp_column:" + str(timestamp_column))

                    time_type_method = get_resource_properties.time_type_method.data
                    print("time_type_method:" + str(time_type_method))

                    is_event_frequency = get_resource_properties.is_event_frequency.data
                    print("is_event_frequency:" + str(is_event_frequency))

                    normal_frequency_range = get_resource_properties.normal_frequency_range.data
                    normal_frequency_range = normal_frequency_range[1:-1].split(',')
                    # normal_frequency_range = list(range(int(normal_frequency_range[0]), int(normal_frequency_range[1])))
                    normal_frequency_range_list=[]
                    normal_frequency_range_list.append(int(normal_frequency_range[0]))
                    normal_frequency_range_list.append(int(normal_frequency_range[1]))
                    print("normal_frequency_range:" + str(normal_frequency_range))
                    print("timestamp_format:"+str(timestamp_format))

                    # 获取资源日志
                    event_to_resource(join(event_log_path, session['last_upload_event_log_server']), join(resource_log_path, 'resource.log'), resource_column, case_type_column, activity_column,
                                      activity_type_method, timestamp_column, timestamp_format, time_type_method,
                                      is_event_frequency,
                                      normal_frequency_range,
                                      activity_type_group_num,
                                      model_file)
                    return render_template('get_resource_log.html',
                                           has_event_log=True,
                                           get_resource_properties=get_resource_properties
                                           )
    else:
        os.abort(405)
    return render_template('get_resource_log.html',
                           has_event_log=False,
                           event_log_upload_form=event_log_upload_form)



@bp.route('/reset_event_log',methods=['GET'])
def reset_event_log():
    clear_session_data()
    return redirect(url_for('.upload_event_log'))

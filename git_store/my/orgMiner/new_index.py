'''Functions
'''
import os
from os.path import join

from flask import session, app, Blueprint, redirect, url_for

bp = Blueprint('new_index', __name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
temp=os.path.join(os.path.dirname(APP_ROOT),'.event')


# redirect url
@bp.route('/', methods=['GET','POST'])
def index():
    # Default: the session will be deleted when the browser closes
    # TODO: redirecting to discovery before more entries are added
    return redirect(url_for('xes_csv.index'))


def clear_session_data():
    from os import walk, remove
    from os.path import isfile
    import re
    l_data_files_rm = list()
    patt = re.compile(session.sid[:32])
    for root, dirs, files in walk(temp):
        l_data_files_rm.extend([
            join(temp, fn) for fn in files if patt.match(fn)
        ])
    for fp in l_data_files_rm:
        if isfile(fp):
            remove(fp)

    if 'last_upload_event_log_xes' in session:
        del session['last_upload_event_log_xes']
    if 'last_upload_event_log_csv' in session:
        del session['last_upload_event_log_csv']
    if 'event_log_csv' in session:
        del session['event_log_csv']
    if 'last_upload_event_log_client' in session:
        del session['last_upload_event_log_client']
    if 'last_upload_event_log_server' in session:
        del session['last_upload_event_log_server']
    if 'last_upload_resource_log_client' in session:
        del session['last_upload_resource_log_client']
    if 'last_upload_resource_log_server' in session:
        del session['last_upload_resource_log_server']
    if 'org_model' in session:
        del session['org_model']
    if 'fitness' in session:
        del session['fitness']
    if 'precision' in session:
        del session['precision']
    if 'resource_functional_similarity' in session:
        del session['resource_functional_similarity']
    if 'fout_file' in session:
        del session['fout_file']
    if 'last_upload_resource_log_server' in session:
        del session['last_upload_resource_log_server']
    if 'org_model' in session:
        del session['org_model']
    if 'fitness' in session:
        del session['fitness']
    if 'precision' in session:
        del session['precision']
    if 'resource_functional_similarity' in session:
        del session['resource_functional_similarity']
from flask import Blueprint, render_template, session

bp = Blueprint('visual_org_model', __name__)

@bp.route('/visual_org_model',methods=['GET','POST'])
def visual_org_model():

    return render_template('visual_org_model.html',
                           fitness_org_model=session['fitness'],
                           precision_org_model=session['precision'],
                           resource_functional_similarity=session['resource_functional_similarity'])
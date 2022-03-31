import wtforms
from flask_wtf import FlaskForm, Form
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import Required



class LogUploadForm(FlaskForm):
    f_log = FileField(
        u'Select an event log file with one of the extensions below',
        validators=[
            FileRequired(),
            FileAllowed(['xes'],
                'Incompatible file extension. Please check again')
        ]
    )
    submit = wtforms.SubmitField(
        u'Upload'
    )


class RequiredEqualsTo:
    ''' A validator which makes a field required if another field is set
        and has a desired value, otherwise a None value is accepted.
        link: https://stackoverflow.com/a/8464478/3359917
        link: https://stackoverflow.com/a/25402311/3359917
    '''
    # *将tuple或者list中的元素进行unpack，分开传入，作为多个参数
    # **作用把dict类型的数据作为参数传入
    def __init__(self,other_field_name, other_field_values, stop_validation=False,*args, **kwargs):
        self.dep_field_name = other_field_name
        self.dep_field_values = other_field_values
        self.stop_validation = stop_validation
        super(RequiredEqualsTo, self).__init__(*args, **kwargs)
    # 使类可以像普通方法一样被调用
    def __call__(self, form, field):
        dep_field = form._fields.get(self.dep_field_name)

        if dep_field is not None \
            and dep_field.data in self.dep_field_values:
            wtforms.validators.InputRequired.__call__(self, form, field)
        else:
            wtforms.validators.Optional.__call__(self, form, field)

        if self.stop_validation:
            raise wtforms.validators.StopValidation


from abc import ABC, abstractmethod
class MethodConfigForm(ABC):
    # Define an inner class 'form' inheriting flask_wtf.FlaskForm

    @classmethod
    def init_config(cls):
        from collections import defaultdict
        return defaultdict(lambda: {
            'method': None,
            'params': dict()
        })

    @classmethod
    @abstractmethod
    def parse_form(form):
        raise NotImplementedError


class EventLogForm(FlaskForm):
    f_log = FileField(
        u'Select an event log file with one of the extensions below',
        validators=[
            FileRequired(),
            FileAllowed(['csv'],
                'Incompatible file extension. Please check again')
        ]
    )
    submit = wtforms.SubmitField(
        u'Upload'
    )


class GetResourceProperties(FlaskForm):
        resource_column=wtforms.StringField('resource_column', validators=[Required()])

        case_type = wtforms.StringField('case_type_column', validators=[Required()])

        activity_column= wtforms.StringField('activity_column',validators=[Required()])

        get_activity_type_method=wtforms.SelectField('Get activity type methods from activity columns',
                                                     choices=[
                                                         (None, '(select a method)'),
                                                         ('0', 'an activity is an activity type'),
                                                         ('1', 'semantic similarity clustering')
                                                     ],
                                                     validators=[wtforms.validators.InputRequired()],
                                                     render_kw={
                                                         'config_type': 'method',
                                                         'config_id': 'gatm',
                                                     })

        activity_type_group_num=wtforms.StringField('the number of activity type group',
                                                    validators=[
                                                        RequiredEqualsTo(
                                                            'activity_type_method',
                                                            ['1']),
                                                    ],
                                                    render_kw={
                                                        'config_type': 'param',
                                                        'config_id': 'activity_type_group_num',
                                                        'prerequisite_id': 'gatm',
                                                        'prerequisite_value': '1',
                                                    })


        timestamp_column = wtforms.StringField('timestamp_column', validators=[Required()])

        time_type_method = wtforms.SelectField('time_type_method',
                                               choices=[
                                                   (None, '(select a method)'),
                                                   ('0', "year"),
                                                   ('1', 'quarter'),
                                                   ('2','month'),
                                                   ('3','week'),
                                                   ('4','day'),
                                                   ('5','hour')
                                               ],
                                               validators=[Required()])

        is_event_frequency=wtforms.SelectField('is event frequency',
                                               choices=[
                                                   (None, '(select)'),
                                                   ('1', "yes"),
                                                   ('0', 'no')
                                               ],
                                               validators=[wtforms.validators.InputRequired()],
                                               render_kw={
                                                   'config_type': 'method',
                                                   'config_id': 'normal_frequency_range',
                                               })

        normal_frequency_range=wtforms.StringField('normal frequency range(eg:[10,20))',
                                                   validators=[
                                                       RequiredEqualsTo(
                                                           'activity_type_method',
                                                           ['1']),
                                                   ],
                                                   render_kw={
                                                       'config_type': 'param',
                                                       'config_id': 'normal_frequency_range',
                                                       'prerequisite_id': 'normal_frequency_range',
                                                       'prerequisite_value': '1',
                                                   }
                                                   )
        submit = wtforms.SubmitField(
            u'Obtain'
        )


class Test(FlaskForm):
    resource_column = wtforms.StringField('resource_column', validators=[Required()])

    submit = wtforms.SubmitField(
        u'Obtain'
    )



class ResourceLogForm(FlaskForm):
    f_log = FileField(
        u'Select an event log file with one of the extensions below',
        validators=[
            FileRequired(),
            FileAllowed(['csv'],
                'Incompatible file extension. Please check again')
        ]
    )
    submit = wtforms.SubmitField(
        u'Upload'
    )


class OrganizeModelMiningAttributes(FlaskForm):

    organization_model_mining_method=wtforms.SelectField('organization model mining method',
                                                         choices=[
                                                           (None, '(select a method)'),
                                                           ('0', "k-means"),
                                                           ('1', 'AHC: Hierarchical Organizational Mining')
                                                                ],
                                                         validators=[Required()])

    resource_similarity_method = wtforms.SelectField('resource similarity method',
                                                   choices=[
                                                       (None, '(select a method)'),
                                                       ('0', "Euclidean_distance"),
                                                       ('1', 'Hamming_Distance'),
                                                       ('2', 'pearson_r'),
                                                       ('3', 'spatial_difference'),
                                                       ('4', 'cosine'),
                                                   ],
                                                   validators=[Required()])

    group_num_range = wtforms.StringField('the range of k values (e.g. [low, high))',
                                                  validators=[Required()])



    assign_execution_mode_method = wtforms.SelectField('assign execution mode method',
                                             choices=[
                                                 (None, '(select)'),
                                                 ('full_recall', 'fullRecall'),
                                                 ('overall_score', 'overallScore')
                                             ],
                                             validators=[wtforms.validators.InputRequired()],
                                             render_kw={
                                                   'config_type': 'method',
                                                   'config_id': 'assign_exec_modes',
                                             }
                                             )

    w1 = wtforms.StringField('the overScore property w1',
                        validators=[
                            RequiredEqualsTo(
                                'method_assign_exec_modes',
                                ['overall_score']),
                            wtforms.validators.NumberRange(0, 1.0),

                        ],
                         render_kw={
                             'config_type': 'param',
                             'config_id': 'w1',
                             'prerequisite_id': 'assign_exec_modes',
                             'prerequisite_value': 'overall_score',
                         }
                             )

    w2 = wtforms.StringField('the overScore property w2',
                             validators=[
                                 RequiredEqualsTo(
                                     'method_assign_exec_modes',
                                     ['overall_score'],),
                                 wtforms.validators.NumberRange(0, 1.0),
                             ],
                             render_kw={
                                 'config_type': 'param',
                                 'config_id': 'w2',
                                 'prerequisite_id': 'assign_exec_modes',
                                 'prerequisite_value': 'overall_score',
                             }
                             )

    submit = wtforms.SubmitField(
        u'Obtain'
    )

class XesLogForm(FlaskForm):
    f_log = FileField(
        u'Select an xes log file with one of the extensions below',
        validators=[
            FileRequired(),
            FileAllowed(['xes'],
                        'Incompatible file extension. Please check again')
        ]
    )
    submit = wtforms.SubmitField(
        u'Upload'
    )







from flask import Response, render_template, flash, request, redirect, url_for
from app import app, db
from models import Devices, Tokens, Args, Devicerules, Tokentypes


# import logging to see queries executed through peewee
import logging
logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

# variables to store created token and device when navigating b/t routes
added_token = {}
added_device = {}
added_rules = {}

# landing page
@app.route('/')
def index():
    return render_template('index.html')


'''
   subroutine for when listing device rules for device/token combinations
'''
@app.route('/getdevicerules/<params>', methods=['GET'])
def getrules(params):
    def generate():
        params_list = params.split(',')
	if int(params_list[0]) == 0 and int(params_list[1]) == 0:
            db_query = [dict(rid=drule.ruleid, did=Devices.get(Devices.deviceid==drule.deviceid.deviceid).devicename, tid=Tokens.get(Tokens.tokenid==drule.tokenid.tokenid).token, rule=drule.ruleline, condition=drule.cond, config=drule.configcommand) for drule in Devicerules.select()]
        elif int(params_list[0]) == 0:
            db_query = [dict(rid=drule.ruleid, did=Devices.get(Devices.deviceid==drule.deviceid.deviceid).devicename, tid=Tokens.get(Tokens.tokenid==drule.tokenid.tokenid).token, rule=drule.ruleline, condition=drule.cond, config=drule.configcommand) for drule in Devicerules.select().where(Devicerules.tokenid==params_list[1])]
        elif int(params_list[1]) == 0:
            db_query = [dict(rid=drule.ruleid, did=Devices.get(Devices.deviceid==drule.deviceid.deviceid).devicename, tid=Tokens.get(Tokens.tokenid==drule.tokenid.tokenid).token, rule=drule.ruleline, condition=drule.cond, config=drule.configcommand) for drule in Devicerules.select().where(Devicerules.deviceid==params_list[0])]
        else:
            db_query = [dict(rid=drule.ruleid, did=Devices.get(Devices.deviceid==drule.deviceid.deviceid).devicename, tid=Tokens.get(Tokens.tokenid==drule.tokenid.tokenid).token, rule=drule.ruleline, condition=drule.cond, config=drule.configcommand) for drule in Devicerules.select().where(Devicerules.deviceid==params_list[0], Devicerules.tokenid==params_list[1])]
        table_start = '<table class="table table-condensed"><tr><th>Device</th><th>Token</th><th>Rule line</th><th>Condition</th><th>Configuration command</th></tr>'
        q = ''
        for each in db_query:
            q += '<tr>'
            q += '<td>' + str(each.get('did')) + '</td>'
            q += '<td>' + str(each.get('tid')) + '</td>'
            q += '<td>' + str(each.get('rule')) + '</td>'
            q += '<td>' + str(each.get('condition')) + '</td>'
            q += '<td>' + str(each.get('config')) + '</td>'
            q += '</tr>'
        table_end = '</table>'
        res = table_start + q + table_end
        yield res
    return Response(generate(), mimetype='text/csv')


'''
   helper template to select devices/tokens in order to create a device rule

@app.route('/add_rule/<param>', methods=['GET'])
def add_rule(param):
    error = None
    # select device
    devices = [dict(did=device.deviceid, dname=device.devicename) for device in Devices.select()]
    # select token
    tokens = [dict(tid=each.tokenid, tname=each.token) for each in Tokens.select()]
    if param == 'device':
        return render_template('addrule_devicetoken.html', entries=[devices, tokens])
    elif param == 'token':
        return render_template('addrule_tokendevice.html', entries=[devices, tokens])
    else:
        error = "Invalid route"
        return render_template('index.html', error=error)       
'''

'''
   helper template to pull out devices and tokens from db
'''
@app.route('/list_devicerules', methods=['GET'])
def list_devicerules():
    # select device
    devices = [dict(did=device.deviceid, dname=device.devicename) for device in Devices.select()]
    # select token
    tokens = [dict(tid=each.tokenid, tname=each.token) for each in Tokens.select()]
    return render_template('list_devicerules.html', entries=[devices, tokens])


'''
   show all device rules that are present in database

@app.route('/showall_devicerules', methods=['GET'])
def showall_devicerules():
    entries = [dict(rid=drule.ruleid, did=Devices.get(Devices.deviceid==drule.deviceid.deviceid).devicename, tid=Tokens.get(Tokens.tokenid==drule.tokenid.tokenid).token, rule=drule.ruleline, condition=drule.cond, config=drule.configcommand) for drule in Devicerules.select()]
    return render_template('showall_devicerules.html', entries=[entries])
'''

'''
   list devices that are present in database
'''
@app.route('/show_devices', methods=['GET'])
def show_devices():
    entries = [dict(did=device.deviceid, dname=device.devicename, ddescr=device.description, dver=device.version) for device in Devices.select()]
    return render_template('show_devices.html', entries=entries)


'''
   list args that are present in a database
'''
@app.route('/show_args', methods=['GET'])
def show_args():
    entries = [dict(argid=arg.argid, argname=arg.argname, argnum=arg.argnumber, ttype=arg.arg_tokentype, hasrestr=arg.hasrestriction, restr=arg.restriction, tokenid=Tokens.get(Tokens.tokenid==arg.tokenid.tokenid).token) for arg in Args.select()]
    return render_template('show_args.html', entries=entries)


'''
   list tokens that are present in database

@app.route('/show_tokens', methods=['GET'])
def show_tokens():
    entries = [dict(tid=each.tokenid, ttype=(Tokentypes.get(Tokentypes.tokentypeid==each.tokentypeid.tokentypeid)).tokentype, ttoken=each.token, tdescr=each.description, tres=each.result, targs=each.args) for each in Tokens.select()]
    return render_template('show_tokens.html', entries=entries)
'''

'''
   remove or update a token
'''
@app.route('/edit_tokens', methods=['GET', 'POST'])
def edit_tokens():
    
    if request.method == 'POST':
        try:
            # check if this is remove vs update POST request
            action = request.form.getlist('action')
            if action[0] == 'remove':
                # read in the content of a present click
                list_value = request.form.getlist('id')
                # if list is not empty - content has gone through
                if len(list_value) > 0:
                    value = int(list_value[0])
                    # token exists since we delete from the dropdown from the db
                    token = Tokens.get(Tokens.tokenid == value)
                    # delete recursively - all dependencies incl. nullable
                    token.delete_instance(recursive=True,delete_nullable=True)
        except socket.error:
            pass  
    entries = [dict(tid=each.tokenid, ttype=(Tokentypes.get(Tokentypes.tokentypeid==each.tokentypeid.tokentypeid)).tokentype, ttypeid=each.tokentypeid.tokentypeid, ttoken=each.token, tdescr=each.description, tres=each.result, targs=each.args) for each in Tokens.select()]
    return render_template('edit_tokens.html', entries=entries)


'''
   show, update, remove devices
'''
@app.route('/edit_devices', methods=['GET', 'POST'])
def edit_devices():
    error = None
    
    if request.method == 'POST':
        # check if this is remove vs update POST request
        action = request.form.getlist('action')
        if action[0] == 'remove':
            # read in the content of a present click
            list_value = request.form.getlist('id')
            # if list is not empty - content has gone through
            if len(list_value) > 0:
                value = int(list_value[0])
                # find device and rules associated with it
                device = Devices.get(Devices.deviceid == value)
                # recursively - delete all dependencies incl. nullable
                device.delete_instance(recursive=True,delete_nullable=True)

        elif action[0] == 'update':
            # read in the content of a present click
            list_id_value = request.form.getlist('id')
            print list_id_value
            # if list is not empty - content has gone through
            if len(list_id_value) > 0:
                id_value = int(list_id_value[0])
                print "value is", id_value
                # find device and rules associated with it
                device = Devices.get(Devices.deviceid == id_value)
                list_name_value = request.form.getlist('name')
                list_descr_value = request.form.getlist('descr')
                list_ver_value = request.form.getlist('ver')
                if list_name_value[0] != '':
                    if list_name_value[0] != device.devicename:
                        device.devicename = list_name_value[0]
                    elif list_descr_value[0] != device.description:
                        device.description = list_descr_value[0]
                    elif list_ver_value[0] != device.version:
                        device.version = list_ver_value[0]
                    device.save()
                else:
                    error = 'Name cannot be empty'
    
    else:
        # list devices
        entries = [dict(did=device.deviceid, dname=device.devicename, ddescr=device.description, dver=device.version) for device in Devices.select()]
        return render_template('edit_devices.html', error=error, entries=entries)


'''
   add device
'''
@app.route('/add_device', methods=['POST', 'GET'])
def add_device():
    error = None
    if request.method == 'POST':
        _devicename = request.form['devicename'].strip()
        _description = request.form['description'].strip()
        _version = request.form['version'].strip()

        # validate the recieved values
        if _devicename:
            # make sure device doesn't exist already
            try:
                device = Devices.get(Devices.devicename==_devicename)
                if device:
                    error = 'Device "' + _devicename + '" already exists'
            except Devices.DoesNotExist:
                device = Devices(devicename=_devicename, description=_description, version=_version)
                device.save()
                global added_device
                added_device = {'object': device, 'deviceid': device.deviceid, 'devicename': _devicename, 'description': _description, 'version': _version}
                # add a successful completion mark
                flash('Device "' + _devicename + '" was successfully added.')
                return redirect(url_for('index'))
        else:
            error = 'Enter the required fields'
    
    return render_template('add_device.html', error=error)       

'''
# select tokens 
@app.route('/select_tokens', methods=['GET', 'POST'])
def select_tokens():              
    entries = [dict(tid=each.tokenid, ttype=(Tokentypes.get(Tokentypes.tokentypeid==each.tokentypeid.tokentypeid)).tokentype, ttoken=each.token, tdescr=each.description, tres=each.result, targs=each.args) for each in Tokens.select()]
    return render_template('select_tokens.html', entries=entries)
'''

'''
   add device rule

@app.route('/add_devicerule', methods=['POST', 'GET'])
def add_devicerule():
    devices = request.form.getlist('devices')
    tokens = request.form.getlist('tokens')
    # data has selected devices, split and create rules for each one
    devices_ids = devices[0].split(',')
    tokens_ids = tokens[0].split(',')
    # we have a few devices, split and create rules for each one 
    if len(devices_ids) > 1:
        token = Tokens.get(Tokens.tokenid==tokens_ids[0])
        _ruleline = 0
        for each in devices_ids:
            _ruleline += 1
            device = Devices.get(Devices.deviceid==each)
            devicerule = Devicerules(deviceid=device, tokenid=token, ruleline=_ruleline, configcommand='ToDo')
            devicerule.save(force_insert=True)
            added_rules.append(devicerule)
            flash('Device rule was successfully added.')
    # we have a few tokens, split and create rules for each one 
    elif len(tokens_ids) > 1:
        device = Devices.get(Devices.deviceid==devices_ids[0])
        for each in tokens_ids:
            token = Tokens.get(Tokens.tokenid==each)
            devicerule = Devicerules(deviceid=device, tokenid=token, ruleline=1, configcommand='ToDo')
            devicerule.save(force_insert=True)
            flash('Device rule was successfully added.')
            added_rules.append(devicerule)
    else:
        token = Tokens.get(Tokens.tokenid==tokens_ids[0])
        device = Devices.get(Devices.deviceid==devices_ids[0])
        devicerule = Devicerules(deviceid=device, tokenid=token, ruleline=1, configcommand='ToDo')
        devicerule.save(force_insert=True)
        flash('Device rule was successfully added.')
        added_rules.append(devicerule)

    # select device
    devices = [dict(did=device.deviceid, dname=device.devicename) for device in Devices.select()]
    # select token
    tokens = [dict(tid=each.tokenid, tname=each.token) for each in Tokens.select()]
    return render_template('list_devicerules.html', entries=[devices, tokens])
'''

'''
   update device rule
   have to remember added device rules

@app.route('/update_rules', methods=['GET', 'POST'])
def update_rules():
    entries = [dict(rid=rule.ruleid, rline=rule.ruleline, rcond=rule.cond, rcommand=rule.configcommand) for rule in added_rules]
    return render_template('update_rules.html', entries=entries)
'''

'''
   add token

@app.route('/add_token/<t_type>', methods=['POST', 'GET'])
def add_token(t_type):
    error = None
   
    if request.method == 'POST':
        _tokenname = request.form['tokenname'].strip()
        _description = request.form['description'].strip()
        _result = request.form['result'].strip()
        _args = request.form['args'].strip()
    
        # format args string to fit into db style (tokenname "arg" "arg" etc.)
        args_list = _args.strip().split(' ')
        str_toadd = ''
        for each in args_list:
            each = '"' + each + '"'
            str_toadd += ' ' + each

        # validate the received values
        if _tokenname:
            # make sure same token doesn't exist already
            try:
                token = Tokens.get(Tokens.token==_tokenname)
                if token:
                    error = 'Token with the specified name already exists'
            
            except Tokens.DoesNotExist:
                # check if user selected the token type
                if t_type == "none":
                    error = "Select token type"
                # look up token type id, no exception since types are hard coded
                else:
                    # look up token type
                    token_type = Tokentypes.get(Tokentypes.tokentype==t_type)
                    token = Tokens(tokentypeid=token_type, token=_tokenname, description=_description, result=_result, args=_tokenname+str_toadd)
                    token.save(force_insert=True)
                    token_withid = Tokens.get(Tokens.tokentypeid==token.tokentypeid, Tokens.args==token.args, Tokens.description==token.description)
                    # update added_token info with created token
                    global added_token
                    added_token = {'object': token_withid, 'tokenid': token_withid.tokenid, 'tokentypeid': token_type.tokentypeid, 'token': _tokenname, 'tokentype': t_type, 'description': _description, 'result': _result, 'args': _args}
                    # add a successful completion mark
                    flash("Token '" + _tokenname + "' was successfully added.")
                    return redirect(url_for('edit_args'))
        else:
            error = 'Enter the required fields'
    
    return render_template('add_token.html', error=error)       
'''

'''
   edit args
   reorder arguments before creation by dragging
   have to remember newly created token

# edit args
@app.route('/edit_args', methods=['GET', 'POST'])
def edit_args():
    #if request.method == "GET":
    #    args_list = ['marina', 'carina', 'nelly', 'julia']
    args = added_token.get('args')
    if args == None:
        args_list = []
    else:
        args_list = [arg.strip() for arg in args.split(' ')]
        return render_template('edit_args.html', entries=args_list)
'''

'''
   add restriction
   step 2 of adding a new token to the Tokens table
   have to remember newly added token
   1. creates arguments
   2. allows adding ("updating") restriction (actual routine is "update_restr")

# add restriction
@app.route('/add_restr', methods=['GET', 'POST'])
def add_restr():
    if request.method == 'POST':
        # the final order of args was submitted, create them
        args = request.form.getlist('args')
        args = [arg.strip() for arg in args[0].split(' ')]
        args_list = filter(None, args)
        keys = range(1, (len(args_list) + 1))
        args_dict = dict(zip(keys, args_list))
        # create arguments
        for key, value in args_dict.items():
            arg = Args(argname=value, argnumber=int(key), arg_tokentype=int(added_token.get('tokentypeid')), hasrestriction=0, tokenid=added_token.get('object'))
            arg.save(force_insert=True)
    
    else:
        # list arguments
        entries = [dict(argid=arg.argid, arg=arg.argname, argnum=arg.argnumber, restr=arg.restriction) for arg in Args.select().where(Args.tokenid==added_token.get('tokenid'))]
        return render_template('add_restr.html', entries=entries)
'''

'''
   update restriction
   sub routine of adding arguments
   updates ("creates") restriction if needed   

@app.route('/update_restr', methods=['POST'])
def update_restr():
    # initially all arguments have 0 for has_restriction and empty str for restriction
    # find argument with posted id
    argid = request.form.getlist('id')
    restr = request.form.getlist('restr')
    num = request.form.getlist('num')
    # no exception since we are updating existing table
    arg = Args.get(Args.argid==argid[0])
    # if not empty update
    if restr[0] == "":
        arg.restriction = None
        arg.has_restriction = 0
    else:
        arg.restriction = restr[0].strip()
        arg.has_restriction = 1
    arg.save()
'''

'''
   select devices
   step 3 of adding a new Token to a token table
   have to remember a newly created token to be executed

@app.route('/select_devices', methods=['GET', 'POST'])
def select_devices():
    entries = [dict(did=device.deviceid, dname=device.devicename, ddescr=device.description, dver=device.version) for device in Devices.select()]
    return render_template('select_devices.html', entries=entries)
'''

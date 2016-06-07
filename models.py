from peewee import *

from app import db


class UnknownField(object):
    pass

class BaseModel(Model):
    class Meta:
        database = db

class Tokentypes(BaseModel):
    description = CharField(db_column='Description', null=True)
    tokentype = CharField(db_column='TokenType', unique=True)
    tokentypeid = PrimaryKeyField(db_column='TokenTypeID')

    class Meta:
        db_table = 'TokenTypes'

class Tokens(BaseModel):
    args = CharField(db_column='Args', null=True)
    description = CharField(db_column='Description', null=True)
    result = CharField(db_column='Result')
    token = CharField(db_column='Token', unique=True)
    tokenid = IntegerField(db_column='TokenID')
    tokentypeid = ForeignKeyField(db_column='TokenTypeID', rel_model=Tokentypes, to_field='tokentypeid')

    class Meta:
        db_table = 'Tokens'
        indexes = (
            (('tokenid', 'tokentypeid'), True),
        )
        primary_key = CompositeKey('tokenid', 'tokentypeid')

class Args(BaseModel):
    argid = PrimaryKeyField(db_column='ArgID')
    argname = CharField(db_column='ArgName')
    argnumber = IntegerField(db_column='ArgNumber')
    arg_tokentype = IntegerField(db_column='Arg_TokenType')
    hasrestriction = IntegerField(db_column='HasRestriction')
    restriction = CharField(db_column='Restriction', null=True)
    tokenid = ForeignKeyField(db_column='TokenID', rel_model=Tokens, to_field='tokenid')

    class Meta:
        db_table = 'Args'

class Devices(BaseModel):
    description = CharField(db_column='Description', null=True)
    deviceid = PrimaryKeyField(db_column='DeviceID')
    devicename = CharField(db_column='DeviceName', unique=True)
    version = CharField(db_column='Version', null=True)

    class Meta:
        db_table = 'Devices'
   
    @classmethod
    def public(cls):
        return (Devices.select().where(Devices.deviceid >= 1))

 
class Devicerules(BaseModel):
    cond = CharField(db_column='Cond', null=True)
    configcommand = CharField(db_column='ConfigCommand')
    deviceid = ForeignKeyField(db_column='DeviceID', rel_model=Devices, to_field='deviceid')
    ruleid = IntegerField(db_column='RuleID')
    ruleline = IntegerField(db_column='RuleLine')
    tokenid = ForeignKeyField(db_column='TokenID', rel_model=Tokens, to_field='tokenid')

    class Meta:
        db_table = 'DeviceRules'
        indexes = (
            (('ruleid', 'deviceid', 'tokenid'), True),
        )
        primary_key = CompositeKey('deviceid', 'ruleid', 'tokenid')

class Globalvariables(BaseModel):
    issequence = IntegerField(db_column='IsSequence', null=True)
    value = TextField(db_column='Value', null=True)
    varid = PrimaryKeyField(db_column='VarID')
    varname = CharField(db_column='VarName')

    class Meta:
        db_table = 'GlobalVariables'

class Tokensandargs(BaseModel):
    argname = CharField(db_column='ArgName', null=True)
    argnumber = IntegerField(db_column='ArgNumber', null=True)
    args = CharField(db_column='Args', null=True)
    restriction = CharField(db_column='Restriction', null=True)
    token = CharField(db_column='Token')
    tokenid = IntegerField(db_column='TokenID')
    tokentype = CharField(db_column='TokenType')

    class Meta:
        db_table = 'TokensAndArgs'

class Tokensandtypes(BaseModel):
    args = CharField(db_column='Args', null=True)
    description = CharField(db_column='Description', null=True)
    result = CharField(db_column='Result')
    token = CharField(db_column='Token')
    tokenid = IntegerField(db_column='TokenID')
    tokentype = CharField(db_column='TokenType')

    class Meta:
        db_table = 'TokensAndTypes'


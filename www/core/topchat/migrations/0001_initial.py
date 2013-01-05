# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'HoldingPageNotification'
        db.create_table('topchat_holdingpagenotification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email_address', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal('topchat', ['HoldingPageNotification'])


    def backwards(self, orm):
        # Deleting model 'HoldingPageNotification'
        db.delete_table('topchat_holdingpagenotification')


    models = {
        'topchat.holdingpagenotification': {
            'Meta': {'object_name': 'HoldingPageNotification'},
            'email_address': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['topchat']
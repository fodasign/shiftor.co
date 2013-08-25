# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BartendProfile'
        db.create_table(u'supervisor_bartendprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('birthday', self.gf('django.db.models.fields.DateField')()),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('student', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('photo', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('wk_name_1', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('wk_type_1', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('wk_name_2', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('wk_type_2', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('wk_name_3', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('wk_type_3', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('wk_name_4', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('wk_type_4', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('wk_name_5', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('wk_type_5', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('years_exp', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('work_sports', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('work_wine', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('work_club', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('work_lounge', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('work_high', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('work_event', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('available_mon', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('available_tue', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('available_wed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('available_thu', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('available_fri', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('available_sat', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('available_sun', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('work_pref_1', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('work_pref_2', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('work_pref_3', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('work_pref_4', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('licensed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('licensed_upload', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('pitch', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'supervisor', ['BartendProfile'])

        # Adding model 'BarProfile'
        db.create_table(u'supervisor_barprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('venue_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('website', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('logo', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address_1', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address_2', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('photo', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('venue_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('facebook_link', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('twitter_link', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('instagram_link', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'supervisor', ['BarProfile'])


    def backwards(self, orm):
        # Deleting model 'BartendProfile'
        db.delete_table(u'supervisor_bartendprofile')

        # Deleting model 'BarProfile'
        db.delete_table(u'supervisor_barprofile')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'supervisor.barprofile': {
            'Meta': {'object_name': 'BarProfile'},
            'address_1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'address_2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'facebook_link': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instagram_link': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'logo': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'photo': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'twitter_link': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'venue_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'venue_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'supervisor.bartendprofile': {
            'Meta': {'object_name': 'BartendProfile'},
            'available_fri': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'available_mon': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'available_sat': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'available_sun': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'available_thu': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'available_tue': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'available_wed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'birthday': ('django.db.models.fields.DateField', [], {}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'licensed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'licensed_upload': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'photo': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pitch': ('django.db.models.fields.TextField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'student': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wk_name_1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'wk_name_2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'wk_name_3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'wk_name_4': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'wk_name_5': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'wk_type_1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'wk_type_2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'wk_type_3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'wk_type_4': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'wk_type_5': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'work_club': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'work_event': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'work_high': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'work_lounge': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'work_pref_1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'work_pref_2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'work_pref_3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'work_pref_4': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'work_sports': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'work_wine': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'years_exp': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'supervisor.user': {
            'Meta': {'ordering': "['-date_joined']", 'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_bar': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_bartend': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'singly_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '36', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'singly_token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "'America/New_York'", 'max_length': '255'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['supervisor']
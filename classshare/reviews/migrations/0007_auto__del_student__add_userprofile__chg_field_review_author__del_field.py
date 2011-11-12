# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Student'
        db.delete_table('reviews_student')

        # Adding model 'UserProfile'
        db.create_table('reviews_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('is_student', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_alumnus', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('reviews', ['UserProfile'])

        # Changing field 'Review.author'
        db.alter_column('reviews_review', 'author_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True))

        # Deleting field 'Course.ccn'
        db.delete_column('reviews_course', 'ccn')

        # Deleting field 'Department.id'
        db.delete_column('reviews_department', 'id')

        # Changing field 'Department.abb'
        db.alter_column('reviews_department', 'abb', self.gf('django.db.models.fields.CharField')(max_length=10, primary_key=True))

        # Adding unique constraint on 'Department', fields ['abb']
        db.create_unique('reviews_department', ['abb'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Department', fields ['abb']
        db.delete_unique('reviews_department', ['abb'])

        # Adding model 'Student'
        db.create_table('reviews_student', (
            ('user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('is_alumnus', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('reviews', ['Student'])

        # Deleting model 'UserProfile'
        db.delete_table('reviews_userprofile')

        # Changing field 'Review.author'
        db.alter_column('reviews_review', 'author_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.Student'], null=True))

        # Adding field 'Course.ccn'
        db.add_column('reviews_course', 'ccn', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Adding field 'Department.id'
        db.add_column('reviews_department', 'id', self.gf('django.db.models.fields.AutoField')(default=0, primary_key=True), keep_default=False)

        # Changing field 'Department.abb'
        db.alter_column('reviews_department', 'abb', self.gf('django.db.models.fields.CharField')(max_length=10))


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'reviews.class': {
            'Meta': {'ordering': "['-year']", 'object_name': 'Class'},
            'ccn': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reviews.Course']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reviews.Instructor']", 'null': 'True', 'blank': 'True'}),
            'semester': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'reviews.course': {
            'Meta': {'object_name': 'Course'},
            'department': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reviews.Department']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['reviews.Tag']", 'null': 'True', 'blank': 'True'})
        },
        'reviews.department': {
            'Meta': {'ordering': "['abb']", 'object_name': 'Department'},
            'abb': ('django.db.models.fields.CharField', [], {'max_length': '10', 'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'reviews.instructor': {
            'Meta': {'object_name': 'Instructor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'reviews.review': {
            'Meta': {'ordering': "['-timestamp']", 'object_name': 'Review'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_anonymous': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reviewed_class': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reviews.Class']"}),
            'thumbs_up': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'reviews.tag': {
            'Meta': {'ordering': "['name']", 'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'reviews.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_alumnus': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_student': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['reviews']

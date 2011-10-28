# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'ISchooler'
        db.delete_table('reviews_ischooler')

        # Adding model 'Instructor'
        db.create_table('reviews_instructor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('reviews', ['Instructor'])

        # Adding model 'Student'
        db.create_table('reviews_student', (
            ('user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('is_current_student', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('reviews', ['Student'])

        # Adding model 'Class'
        db.create_table('reviews_class', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.Course'])),
            ('instructor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.Instructor'])),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('semester', self.gf('django.db.models.fields.CharField')(max_length=6)),
        ))
        db.send_create_signal('reviews', ['Class'])

        # Adding model 'Department'
        db.create_table('reviews_department', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('abb', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('reviews', ['Department'])

        # Adding field 'Review.thumbs_up'
        db.add_column('reviews_review', 'thumbs_up', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Changing field 'Review.author'
        db.alter_column('reviews_review', 'author_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.Student'], null=True))

        # Changing field 'Review.course'
        db.alter_column('reviews_review', 'course_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.Class']))

        # Adding field 'Course.description'
        db.add_column('reviews_course', 'description', self.gf('django.db.models.fields.TextField')(null=True, blank=True), keep_default=False)

        # Adding field 'Course.department'
        db.add_column('reviews_course', 'department', self.gf('django.db.models.fields.related.ForeignKey')(default='EECS', to=orm['reviews.Department']), keep_default=False)

        # Adding field 'Course.number'
        db.add_column('reviews_course', 'number', self.gf('django.db.models.fields.IntegerField')(default='001'), keep_default=False)

        # Adding field 'Course.ccn'
        db.add_column('reviews_course', 'ccn', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Adding model 'ISchooler'
        db.create_table('reviews_ischooler', (
            ('is_current_student', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('reviews', ['ISchooler'])

        # Deleting model 'Instructor'
        db.delete_table('reviews_instructor')

        # Deleting model 'Student'
        db.delete_table('reviews_student')

        # Deleting model 'Class'
        db.delete_table('reviews_class')

        # Deleting model 'Department'
        db.delete_table('reviews_department')

        # Deleting field 'Review.thumbs_up'
        db.delete_column('reviews_review', 'thumbs_up')

        # Changing field 'Review.author'
        db.alter_column('reviews_review', 'author_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.ISchooler'], null=True))

        # Changing field 'Review.course'
        db.alter_column('reviews_review', 'course_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.Course']))

        # Deleting field 'Course.description'
        db.delete_column('reviews_course', 'description')

        # Deleting field 'Course.department'
        db.delete_column('reviews_course', 'department_id')

        # Deleting field 'Course.number'
        db.delete_column('reviews_course', 'number')

        # Deleting field 'Course.ccn'
        db.delete_column('reviews_course', 'ccn')


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
            'Meta': {'object_name': 'Class'},
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reviews.Course']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reviews.Instructor']"}),
            'semester': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'reviews.course': {
            'Meta': {'object_name': 'Course'},
            'ccn': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'department': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reviews.Department']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['reviews.Instructor']", 'through': "orm['reviews.Class']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'number': ('django.db.models.fields.IntegerField', [], {})
        },
        'reviews.department': {
            'Meta': {'object_name': 'Department'},
            'abb': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'reviews.instructor': {
            'Meta': {'object_name': 'Instructor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'reviews.review': {
            'Meta': {'object_name': 'Review'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reviews.Student']", 'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reviews.Class']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_anonymous': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thumbs_up': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'reviews.student': {
            'Meta': {'object_name': 'Student', '_ormbases': ['auth.User']},
            'is_current_student': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['reviews']

# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Tag'
        db.create_table('reviews_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('reviews', ['Tag'])

        # Deleting field 'Review.course'
        db.delete_column('reviews_review', 'course_id')

        # Adding field 'Review.reviewed_class'
        db.add_column('reviews_review', 'reviewed_class', self.gf('django.db.models.fields.related.ForeignKey')(default='test', to=orm['reviews.Class']), keep_default=False)

        # Deleting field 'Student.is_current_student'
        db.delete_column('reviews_student', 'is_current_student')

        # Adding field 'Student.is_alumnus'
        db.add_column('reviews_student', 'is_alumnus', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Class.ccn'
        db.add_column('reviews_class', 'ccn', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Changing field 'Class.instructor'
        db.alter_column('reviews_class', 'instructor_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['reviews.Instructor'], null=True))

        # Deleting field 'Course.ccn'
        db.delete_column('reviews_course', 'ccn')

        # Adding M2M table for field tags on 'Course'
        db.create_table('reviews_course_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm['reviews.course'], null=False)),
            ('tag', models.ForeignKey(orm['reviews.tag'], null=False))
        ))
        db.create_unique('reviews_course_tags', ['course_id', 'tag_id'])

        # Changing field 'Course.number'
        db.alter_column('reviews_course', 'number', self.gf('django.db.models.fields.CharField')(max_length=12))

        # Changing field 'Department.name'
        db.alter_column('reviews_department', 'name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))


    def backwards(self, orm):
        
        # Deleting model 'Tag'
        db.delete_table('reviews_tag')

        # Adding field 'Review.course'
        db.add_column('reviews_review', 'course', self.gf('django.db.models.fields.related.ForeignKey')(default='test', to=orm['reviews.Class']), keep_default=False)

        # Deleting field 'Review.reviewed_class'
        db.delete_column('reviews_review', 'reviewed_class_id')

        # Adding field 'Student.is_current_student'
        db.add_column('reviews_student', 'is_current_student', self.gf('django.db.models.fields.BooleanField')(default=True), keep_default=False)

        # Deleting field 'Student.is_alumnus'
        db.delete_column('reviews_student', 'is_alumnus')

        # Deleting field 'Class.ccn'
        db.delete_column('reviews_class', 'ccn')

        # Changing field 'Class.instructor'
        db.alter_column('reviews_class', 'instructor_id', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['reviews.Instructor']))

        # Adding field 'Course.ccn'
        db.add_column('reviews_course', 'ccn', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True), keep_default=False)

        # Removing M2M table for field tags on 'Course'
        db.delete_table('reviews_course_tags')

        # Changing field 'Course.number'
        db.alter_column('reviews_course', 'number', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'Department.name'
        db.alter_column('reviews_department', 'name', self.gf('django.db.models.fields.CharField')(default=0, max_length=200))


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
            'Meta': {'object_name': 'Department'},
            'abb': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_anonymous': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reviewed_class': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['reviews.Class']"}),
            'thumbs_up': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'reviews.student': {
            'Meta': {'object_name': 'Student', '_ormbases': ['auth.User']},
            'is_alumnus': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'reviews.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['reviews']

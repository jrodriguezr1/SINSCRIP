# Generated by Django 4.2.2 on 2023-08-30 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asistira',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('cve_estud', models.BigIntegerField()),
                ('cve_curso', models.CharField(max_length=6)),
                ('gpo_670', models.CharField(blank=True, max_length=2, null=True)),
                ('califica', models.FloatField()),
                ('creditos', models.IntegerField(blank=True, null=True)),
                ('periodo', models.CharField(max_length=9)),
                ('agno', models.IntegerField()),
                ('observa', models.CharField(blank=True, max_length=7, null=True)),
                ('registro', models.DateField(blank=True, null=True)),
                ('per_vi_cur', models.CharField(max_length=9)),
                ('ano_vi_cur', models.IntegerField()),
                ('no_periodo', models.IntegerField()),
                ('isevaluated', models.IntegerField(blank=True, db_column='IsEvaluated', null=True)),
            ],
            options={
                'db_table': 'asistira',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Capcurs',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('cve_program', models.CharField(max_length=3)),
                ('nombre', models.CharField(max_length=120)),
                ('nom_academic', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=100)),
                ('participacion', models.CharField(max_length=20)),
                ('creditos', models.IntegerField()),
                ('aula', models.CharField(blank=True, max_length=100, null=True)),
                ('observaciones', models.CharField(blank=True, max_length=120, null=True)),
                ('lunes_ini', models.TimeField(blank=True, null=True)),
                ('lunes_fin', models.TimeField(blank=True, null=True)),
                ('martes_ini', models.TimeField(blank=True, null=True)),
                ('martes_fin', models.TimeField(blank=True, null=True)),
                ('miercoles_fin', models.TimeField(blank=True, null=True)),
                ('miercoles_ini', models.TimeField(blank=True, null=True)),
                ('jueves_ini', models.TimeField(blank=True, null=True)),
                ('jueves_fin', models.TimeField(blank=True, null=True)),
                ('viernes_fin', models.TimeField(blank=True, null=True)),
                ('viernes_ini', models.TimeField(blank=True, null=True)),
                ('periodo', models.CharField(max_length=9)),
                ('agno', models.IntegerField(blank=True, null=True)),
                ('lunes_inip', models.TimeField(blank=True, null=True)),
                ('lunes_finp', models.TimeField(blank=True, null=True)),
                ('martes_inip', models.TimeField(blank=True, null=True)),
                ('martes_finp', models.TimeField(blank=True, null=True)),
                ('miercoles_inip', models.TimeField(blank=True, null=True)),
                ('miercoles_finp', models.TimeField(blank=True, null=True)),
                ('jueves_inip', models.TimeField(blank=True, null=True)),
                ('jueves_finp', models.TimeField(blank=True, null=True)),
                ('viernes_inip', models.TimeField(blank=True, null=True)),
                ('viernes_finp', models.TimeField(blank=True, null=True)),
                ('aulap', models.TextField(blank=True, null=True)),
                ('observacionesp', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'capcurs',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CapcursappAcademic',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('num_emplea', models.BigIntegerField(blank=True, null=True)),
                ('cve_academic', models.CharField(max_length=6)),
                ('nombres', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=100)),
                ('cve_sexo', models.CharField(max_length=9)),
                ('cve_campus', models.CharField(max_length=3)),
                ('cve_institu', models.CharField(max_length=3)),
                ('cve_program', models.CharField(max_length=3)),
                ('grado', models.CharField(blank=True, max_length=12, null=True)),
                ('activo', models.CharField(blank=True, max_length=1, null=True)),
                ('externo', models.CharField(blank=True, max_length=1, null=True)),
                ('no_oficina', models.CharField(blank=True, max_length=5, null=True)),
                ('edificio', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.CharField(max_length=60)),
                ('extension', models.CharField(blank=True, max_length=6, null=True)),
            ],
            options={
                'db_table': 'capcursapp_academic',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Catacurs',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('cve_campus', models.CharField(blank=True, max_length=3, null=True)),
                ('cve_program', models.CharField(blank=True, max_length=3, null=True)),
                ('cve_curso', models.CharField(blank=True, max_length=6, null=True, unique=True)),
                ('gpo_670', models.CharField(blank=True, max_length=2, null=True)),
                ('nombre', models.CharField(blank=True, max_length=120, null=True)),
                ('credimi', models.IntegerField(blank=True, null=True)),
                ('credima', models.IntegerField(blank=True, null=True)),
                ('vigente', models.CharField(blank=True, max_length=2, null=True)),
                ('es_tecno', models.CharField(blank=True, max_length=1, null=True)),
                ('periodo', models.CharField(blank=True, max_length=9, null=True)),
                ('agno', models.IntegerField(blank=True, null=True)),
                ('hay_credi', models.CharField(blank=True, max_length=2, null=True)),
                ('hay_calif', models.CharField(blank=True, max_length=2, null=True)),
                ('tipo', models.CharField(blank=True, max_length=16, null=True)),
                ('isevaluated', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'catacurs',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.PositiveSmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Imparegu',
            fields=[
                ('id_auto', models.AutoField(primary_key=True, serialize=False)),
                ('num_emplea', models.BigIntegerField(blank=True, null=True)),
                ('cve_academic', models.CharField(max_length=6)),
                ('cve_curso', models.CharField(max_length=6)),
                ('gpo_670', models.CharField(max_length=2)),
                ('periodo', models.CharField(max_length=9)),
                ('agno', models.IntegerField()),
                ('participa', models.CharField(max_length=11)),
                ('registro', models.DateField()),
                ('per_vi_cur', models.CharField(max_length=9)),
                ('ano_vi_cur', models.IntegerField()),
                ('dis_cre', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'imparegu',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='InscripEstudian',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('cve_estud', models.BigIntegerField(blank=True, null=True)),
                ('nombres', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=100)),
                ('cve_campus', models.CharField(max_length=3)),
                ('cve_institu', models.CharField(max_length=3)),
                ('cve_program', models.CharField(max_length=3)),
                ('periingr', models.CharField(max_length=9)),
                ('fechingr', models.DateField(blank=True, null=True)),
                ('cve_sexo', models.CharField(max_length=9)),
                ('e_mail', models.CharField(max_length=50)),
                ('username', models.CharField(blank=True, max_length=50, null=True)),
                ('password', models.CharField(max_length=128)),
                ('cont_veces', models.IntegerField()),
                ('cont_final', models.IntegerField()),
            ],
            options={
                'db_table': 'inscrip_estudian',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Coordinaciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('cve_campus', models.CharField(max_length=3)),
                ('cve_posgrad', models.CharField(max_length=6)),
                ('nom_posgra', models.CharField(max_length=60)),
                ('cve_program', models.CharField(max_length=3)),
                ('nom_program', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('cont_veces', models.IntegerField(default=0)),
                ('cont_final', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Academic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_emplea', models.BigIntegerField()),
                ('cve_academic', models.CharField(max_length=6, unique=True)),
                ('nombres', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=100)),
                ('cve_sexo', models.CharField(max_length=9)),
                ('cve_campus', models.CharField(max_length=3)),
                ('cve_institu', models.CharField(max_length=3)),
                ('cve_program', models.CharField(max_length=3)),
                ('grado', models.CharField(max_length=12)),
                ('activo', models.CharField(max_length=1)),
                ('externo', models.CharField(max_length=1)),
                ('no_oficina', models.CharField(max_length=5)),
                ('edificio', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=60)),
                ('extension', models.CharField(max_length=6)),
            ],
            options={
                'db_table': 'academic',
                'managed': True,
            },
        ),
    ]

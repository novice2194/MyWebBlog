## 简介

### 创建项目

```shell
$ django-admin startproject HelloWorld
```

#### 目录说明

- **HelloWorld:** 项目的容器。
- **manage.py:** 一个实用的命令行工具，可让你以各种方式与该 Django 项目进行交互。
- **HelloWorld/__init__.py:** 一个空文件，告诉 Python 该目录是一个 Python 包。
- **HelloWorld/asgi.py:** 一个 ASGI 兼容的 Web 服务器的入口，以便运行你的项目。
- **HelloWorld/settings.py:** 该 Django 项目的设置/配置。
- **HelloWorld/urls.py:** 该 Django 项目的 URL 声明; 一份由 Django 驱动的网站"目录"。
- **HelloWorld/wsgi.py:** 一个 WSGI 兼容的 Web 服务器的入口，以便运行你的项目。

### 启动服务器

```shell
$ python manage.py runserver
```

#### 更换端口

默认情况下，[`runserver`](https://docs.djangoproject.com/zh-hans/3.2/ref/django-admin/#django-admin-runserver) 命令会将服务器设置为监听本机内部 IP 的 8000 端口。

如果你想更换服务器的监听端口，请使用命令行参数。下面的命令会使服务器监听 8080 端口：

```shell
$ python manage.py runserver 8080
```

如果你想要修改服务器监听的IP，在端口之前输入新的。比如，为了监听所有服务器的公开IP（这你运行 Vagrant 或想要向网络上的其它电脑展示你的成果时很有用），使用：

```shell
$ python manage.py runserver 0:8000
```

**0** 是 **0.0.0.0** 的简写。完整的关于开发服务器的文档可以在 [:djamdin:`runserver`](https://docs.djangoproject.com/zh-hans/3.2/intro/tutorial01/#id1) 参考文档中找到。

##### 设置公网访问

修改setting文件：

```python
ALLOWED_HOSTS = ['主机ip']
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False
```

### 创建应用

```shell
$ python manage.py startapp polls
```

这将会创建一个 `polls` 目录，它的目录结构大致如下：

```
polls/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    views.py
```

这个目录结构包括了应用的全部内容。 

### 改变模型

- 编辑 `models.py` 文件，改变模型。
- 运行 [`python manage.py makemigrations`](https://docs.djangoproject.com/zh-hans/3.2/ref/django-admin/#django-admin-makemigrations) 为模型的改变生成迁移文件。
- 运行 [`python manage.py migrate`](https://docs.djangoproject.com/zh-hans/3.2/ref/django-admin/#django-admin-migrate) 来应用数据库迁移。

**文件：`polls/models.py`**

```python
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```

#### makemigrations

```shell
$ python manage.py makemigrations polls
```

**输出：**

```shell
Migrations for 'polls':
  polls/migrations/0001_initial.py
    - Create model Question
    - Create model Choice
```

通过运行 `makemigrations` 命令，Django 会检测你对模型文件的修改（在这种情况下，你已经取得了新的），并且把修改的部分储存为一次 *迁移*。

迁移是 Django 对于模型定义（也就是你的数据库结构）的变化的储存形式 - 它们其实也只是一些你磁盘上的文件。如果你想的话，你可以阅读一下你模型的迁移数据，它被储存在 `polls/migrations/0001_initial.py` 里。别担心，你不需要每次都阅读迁移文件，但是它们被设计成人类可读的形式，这是为了便于你手动调整 Django 的修改方式。

Django 有一个自动执行数据库迁移并同步管理你的数据库结构的命令 - 这个命令是 [`migrate`](https://docs.djangoproject.com/zh-hans/3.2/ref/django-admin/#django-admin-migrate)，我们马上就会接触它 - 但是首先，让我们看看迁移命令会执行哪些 SQL 语句。[`sqlmigrate`](https://docs.djangoproject.com/zh-hans/3.2/ref/django-admin/#django-admin-sqlmigrate) 命令接收一个迁移的名称，然后返回对应的 SQL：

```shell
$ python manage.py sqlmigrate polls 0001
```

**输出：**

```shell
BEGIN;
--
-- Create model Question
--
CREATE TABLE "polls_question" (
    "id" serial NOT NULL PRIMARY KEY,
    "question_text" varchar(200) NOT NULL,
    "pub_date" timestamp with time zone NOT NULL
);
--
-- Create model Choice
--
CREATE TABLE "polls_choice" (
    "id" serial NOT NULL PRIMARY KEY,
    "choice_text" varchar(200) NOT NULL,
    "votes" integer NOT NULL,
    "question_id" integer NOT NULL
);
ALTER TABLE "polls_choice"
  ADD CONSTRAINT "polls_choice_question_id_c5b4b260_fk_polls_question_id"
    FOREIGN KEY ("question_id")
    REFERENCES "polls_question" ("id")
    DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "polls_choice_question_id_c5b4b260" ON "polls_choice" ("question_id");

COMMIT;
```

请注意以下几点：

- 输出的内容和你使用的数据库有关，上面的输出示例使用的是 PostgreSQL。
- 数据库的表名是由应用名(`polls`)和模型名的小写形式( `question` 和 `choice`)连接而来。（如果需要，你可以自定义此行为。）
- 主键(IDs)会被自动创建。(当然，你也可以自定义。)
- 默认的，Django 会在外键字段名后追加字符串 `"_id"` 。（同样，这也可以自定义。）
- 外键关系由 `FOREIGN KEY` 生成。你不用关心 `DEFERRABLE` 部分，它只是告诉 PostgreSQL，请在事务全都执行完之后再创建外键关系。
- 生成的 SQL 语句是为你所用的数据库定制的，所以那些和数据库有关的字段类型，比如 `auto_increment` (MySQL)、 `serial` (PostgreSQL)和 `integer primary key autoincrement` (SQLite)，Django 会帮你自动处理。那些和引号相关的事情 - 例如，是使用单引号还是双引号 - 也一样会被自动处理。
- 这个 [`sqlmigrate`](https://docs.djangoproject.com/zh-hans/3.2/ref/django-admin/#django-admin-sqlmigrate) 命令并没有真正在你的数据库中的执行迁移 - 相反，它只是把命令输出到屏幕上，让你看看 Django 认为需要执行哪些 SQL 语句。这在你想看看 Django 到底准备做什么，或者当你是数据库管理员，需要写脚本来批量处理数据库时会很有用。

如果你感兴趣，你也可以试试运行 [`python manage.py check`](https://docs.djangoproject.com/zh-hans/3.2/ref/django-admin/#django-admin-check) ;这个命令帮助你检查项目中的问题，并且在检查过程中不会对数据库进行任何操作。

#### migrate

```shell
$ python manage.py migrate
```

**输出：**

```shell
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, polls, sessions
Running migrations:
  Rendering model states... DONE
  Applying polls.0001_initial... OK
```

### URLconf导入方式

**目录结构：**

```sh
polls/
    __init__.py
    admin.py
    apps.py
    migrations/
        __init__.py
    models.py
    tests.py
    urls.py
    views.py
```

**文件：`polls/urls.py`**

```python
path('', views.index, name='index')
```

#### include模式

```python
path('polls/', include('polls.urls'))
```

函数 [`include()`](https://docs.djangoproject.com/zh-hans/3.2/ref/urls/#django.urls.include) 允许引用其它 URLconfs。每当 Django 遇到 [`include()`](https://docs.djangoproject.com/zh-hans/3.2/ref/urls/#django.urls.include) 时，它会截断与此项匹配的 URL 的部分，并将剩余的字符串发送到 URLconf 以供进一步处理。

#### import模式

类似于 `admin` 的导入方式，通过导入包的导入方式，将 `views` 视图的返回值传入到 `path` 中。

**文件：`poll/__init__.py`**

```python
from . import views
```

**文件：`mysite/urls.py`**

```python
path('polls/', polls.views.index,name='index')
```

### PATH解析方式

#### 1.直接解析

```python
path('admin/', admin.site.urls)
```

#### 2.转换器解析

**`<转换器类型：自定义名>`**

！数据将按关键字传参给视图函数

```python
path('<int polls>', view.index)
```

| 转换器类型 | 作用                                  | 解释             |
| ---------- | ------------------------------------- | ---------------- |
| str        | 匹配除 `/` 以外的字符串               | 'a/b/c'==>'c'    |
| int        | 匹配 `0` 和正整数                     | 'a/1/2'==>2      |
| slug       | 匹配 `ASCII` 、`-` 和数字组成的短标签 | 'a/b-c'==>'b-c'  |
| path       | 匹配 `/` 以内的字段                   | 'a/b/c'==>'/b/c' |

#### 3.`re_path()` 解析

！正则表达式采用命名分组形式：**`(?P<key>pattern)`**

```python
re_path(reg, view.index)
```
































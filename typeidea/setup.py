# 配置项目的setup.py
from setuptools import setup,find_packages

setup(
    name='typeidea',
    version='0.1',
    description='Blog System base on Django',
    author='zomodo',
    author_email='986001564@qq.com',
    url='#',
    license='MIT',
    packages=find_packages('typeidea'),
    package_dir={'':'typeidea'},

    # 方法一：打包数据文件，需按照目录层级匹配,package_data指除了.py文件以外还需要打包哪些
    # package_data={'':[
    #     'themes/*/*/*/*',
    # ]},

    # 方法二：打包数据文件，配合MANIFEST.in文件，使用较多,两个方法可以共存
    include_package_data=True,

    install_requires=[
        'django==1.11.28',
        'dj-pagination==2.4.0',
        'supervisor==4.1.0',
        'xadmin==0.6.1',
        'mysqlclient==1.4.6',
        'django-ckeditor==5.4.0',
        'django-rest-framework==0.1.0',
        'django-redis==4.9.0',
        'django-autocomplete-light==3.2.10',
        'mistune==0.8.4',
        'Pillow==5.1.0',
        'coreapi==2.3.3',
        'django-debug-toolbar==1.9.1',

    ],
    extras_require={
        'ipython':['ipython==6.2.1'],
    },
    scripts=[
        './manage.py',
    ],
    entry_points={
        'console_scripts':[
            'typeidea_manage=manage:main',
        ]
    },
    classifiers=[
        # 软件成熟度如何，一般有下面几项
        # 3 - Alpha
        # 4 - Beta
        # 5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # 指明项目的受众
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',

        # 选择项目许可证（License）
        'License :: OSI Approved :: MIT License',

        # 指定项目需要使用的python版本
        'Programming Language :: Python :: 3.6',

    ],

)

"""
配置好之后就打包
python setup.py sdist:打包之后以.tar.gz结尾
python setup.py bdist_wheel:打包是wheel格式的，以whl结尾，优先使用wheel包
"""
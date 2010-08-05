from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='intranett.theme',
      version=version,
      description="Basic theme providing base fonts, typography, \
                   rhythm for intranett.no projects. Particular \
                   projects' specific visual themes are going to \
                   be built on top of this base theme.",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['intranett'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'z3c.jbot'
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )

from distutils.core import setup

setup(
    name='aluno_exatas',
    version='0.6',
    packages=['aluno_exatas'],
    install_requires = ['numpy', 'sympy'] ,
    license='MIT License',
    long_description=open('README.md').read(),
   	url='http://pypi.python.org/pypi/AlunoExatas',
    author='EricoNR',
    author_email='e170610@g.unicamp.br'
)
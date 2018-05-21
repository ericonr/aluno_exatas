from setuptools import setup

setup(
    name='aluno_exatas',
    version='0.8.3',
    packages=['aluno_exatas'],
    install_requires = ['numpy', 'sympy'],
    license='MIT License',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
   	url='https://github.com/ericonr/aluno_exatas',
    author='EricoNR',
    author_email='e170610@g.unicamp.br',
)
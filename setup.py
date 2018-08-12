from setuptools import setup, find_packages

setup(
    name='aluno_exatas',
    version='0.8.5',
    packages=find_packages(),
    install_requires=['numpy', 'sympy'],
    license='MIT License',
    description='Um pacote para auxiliar alunos de exatas.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
   	url='https://github.com/ericonr/aluno_exatas',
    author='EricoNR',
    author_email='e170610@g.unicamp.br',
)

from setuptools import setup, find_packages

setup(
    name='on_builtin',
    version="0.1.2",
    description='Package to use builtin function',
    url='git+https://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@github.com/hopelife/on_builtin.git',
    author='Moon Jung Sam',
    author_email='monblue@snu.ac.kr',
    license='MIT',
    packages=['on_builtin'],
    include_package_data = True,
    keywords='on_py',
    python_requires='>=3.8',  # 
    install_requires=[ # 패키지 사용을 위해 필요한 추가 설치 패키지
        'pyyaml',
        'pandas',
        'openpyxl',
    ],
)

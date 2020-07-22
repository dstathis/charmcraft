# Copyright 2020 Canonical Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# For further info, check https://github.com/canonical/charmcraft

from argparse import Namespace
import subprocess

from charmcraft.commands.init import InitCommand
from charmcraft.commands._utils import S_IXALL
from tests.test_infra import pep8_test, get_python_filepaths


def test_init_pep8(tmp_path, *, name=None, author="J Doe"):
    if name is None:
        name = tmp_path.name
    cmd = InitCommand('group')
    cmd.run(Namespace(directory=tmp_path, name=name, author=author))
    paths = get_python_filepaths(roots=[tmp_path / "src", tmp_path / "tests"], python_paths=[])
    pep8_test(paths)


def test_init_non_ascii_author(tmp_path):
    test_init_pep8(tmp_path, author="فلانة الفلانية")


def test_init_non_ascii_name(tmp_path):
    test_init_pep8(tmp_path, name="ჭიჭიკო")


def test_all_the_files(tmp_path):
    cmd = InitCommand('group')
    cmd.run(Namespace(directory=tmp_path, name=tmp_path.name, author="ಅಪರಿಚಿತ ವ್ಯಕ್ತಿ"))
    assert sorted(str(p.relative_to(tmp_path)) for p in tmp_path.glob("**/*")) == [
        "LICENSE",
        "README.md",
        "config.yaml",
        "metadata.yaml",
        "requirements-dev.txt",
        "requirements.txt",
        "run_tests",
        "src",
        "src/charm.py",
        "tests",
        "tests/__init__.py",
        "tests/test_charm.py",
    ]


def test_executables(tmp_path):
    cmd = InitCommand('group')
    cmd.run(Namespace(directory=tmp_path, name=tmp_path.name, author="홍길동"))
    assert (tmp_path / "run_tests").stat().st_mode & S_IXALL == S_IXALL
    assert (tmp_path / "src/charm.py").stat().st_mode & S_IXALL == S_IXALL


def test_tests(tmp_path):
    cmd = InitCommand('group')
    cmd.run(Namespace(directory=tmp_path, name=tmp_path.name, author="홍길동"))
    subprocess.run(["./run_tests"], cwd=tmp_path, check=True)

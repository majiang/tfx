# Lint as: python2, python3
# Copyright 2020 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Local filesystem-based filesystem plugin."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import glob
import os
import shutil

from typing import Any, Callable, Iterable, List, Text, Tuple

from tfx.dsl.io import filesystem
from tfx.dsl.io import filesystem_registry
from tfx.dsl.io.filesystem import PathType


class LocalFilesystem(filesystem.Filesystem):
  """Filesystem that uses local file operations."""

  SUPPORTED_SCHEMES = ['']

  @staticmethod
  def open(name: PathType, mode: Text = 'r') -> Any:
    return open(name, mode=mode)

  @staticmethod
  def copy(src: PathType, dst: PathType, overwrite: bool = False) -> None:
    if not overwrite and os.path.exists(dst):
      raise OSError(
          ('Destination file %r already exists and argument `overwrite` is '
           'false.') % dst)
    shutil.copyfile(src, dst)

  @staticmethod
  def exists(path: PathType) -> bool:
    return os.path.exists(path)

  @staticmethod
  def glob(pattern: PathType) -> List[PathType]:
    return glob.glob(pattern)

  @staticmethod
  def isdir(path: PathType) -> bool:
    return os.path.isdir(path)

  @staticmethod
  def listdir(path: PathType) -> List[PathType]:
    return os.listdir(path)

  @staticmethod
  def makedirs(path: PathType) -> None:
    os.makedirs(path, exist_ok=True)

  @staticmethod
  def mkdir(path: PathType) -> None:
    os.mkdir(path)

  @staticmethod
  def remove(path: PathType) -> None:
    os.remove(path)

  @staticmethod
  def rename(src: PathType, dst: PathType, overwrite: bool = False) -> None:
    if not overwrite and os.path.exists(dst):
      raise OSError(
          ('Destination path %r already exists and argument `overwrite` is '
           'false.') % dst)
    os.rename(src, dst)

  @staticmethod
  def rmtree(path: PathType) -> None:
    shutil.rmtree(path)

  @staticmethod
  def stat(path: PathType) -> Any:
    return os.stat(path)

  @staticmethod
  def walk(
      top: PathType,
      topdown: bool = True,
      onerror: Callable[..., None] = None
  ) -> Iterable[Tuple[PathType, List[PathType], List[PathType]]]:
    yield from os.walk(top, topdown=topdown, onerror=onerror)


filesystem_registry.DEFAULT_FILESYSTEM_REGISTRY.register(
    LocalFilesystem, priority=10)

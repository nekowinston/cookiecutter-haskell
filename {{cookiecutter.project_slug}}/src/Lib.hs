-- SPDX-FileCopyrightText: {{ cookiecutter.__spdx_text }}
-- SPDX-License-Identifier: {{ cookiecutter.license }}

module Lib where

fibs :: [Word64]
fibs = unfoldr
  (\(x, y) -> Just (x, (y, x + y)))
  (0, 1)

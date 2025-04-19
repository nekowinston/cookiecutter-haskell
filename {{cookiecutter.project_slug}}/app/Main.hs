-- SPDX-FileCopyrightText: {{ cookiecutter.__spdx_text }}
-- SPDX-License-Identifier: {{ cookiecutter.license }}

import Lib

main :: IO ()
main = putTextLn $ show $ take 20 fibs

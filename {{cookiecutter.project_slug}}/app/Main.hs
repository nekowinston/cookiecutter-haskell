-- SPDX-FileCopyrightText: {{ cookiecutter.__spdx_text }}
-- SPDX-License-Identifier: {{ cookiecutter.license }}

{%- if cookiecutter.is_library %}
import Lib

main :: IO ()
main = putTextLn $ show $ take 20 fibs
{%- else %}
main :: IO ()
main = putTextLn "Hello World!"
{% endif -%}


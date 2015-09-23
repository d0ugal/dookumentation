#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Dookumentation.

StandAlone Async single-file cross-platform no-dependencies
Python3-ready Documentation Generator from Source Code.
"""


import ast
import functools
import logging as log
import os
import re
import socket
import sys

from argparse import ArgumentParser
from copy import copy
from ctypes import byref, cdll, create_string_buffer
from datetime import datetime
from getpass import getuser
from hashlib import sha1
from json import dumps
from multiprocessing import Pool, cpu_count
from platform import platform, python_version
from random import randint
from string import punctuation
from tempfile import gettempdir
from time import sleep

import _ast

try:
    from urllib import request
    from subprocess import getoutput
    from shutil import disk_usage
except ImportError:
    request = getoutput = disk_usage = None

try:
    import resource  # windows dont have resource
except ImportError:
    resource = None

try:
    from pylama.main import check_path, parse_options
except ImportError:
    check_path = parse_options = None
    print("WARNING: PyLama Not Found !!!, Run: \nsudo pip3 install pylama")


__version__ = "1.0.0"
__license__ = "GPLv3+ LGPLv3+ AGPLv3+"
__author__ = "Juan Carlos"
__email__ = "juancarlospaco@gmail.com"
__url__ = "https://github.com/juancarlospaco/dookumentation"
__source__ = ("https://raw.githubusercontent.com/juancarlospaco/"
              "dookumentation/master/dookumentation.py")


start_time = datetime.now()


HTML = """<!DOCTYPE html><meta charset=utf-8/><meta name=keywords content=Docs>
<title> {%{{ data['basename'].title()[:99] }}%} - Dookumentation </title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="shortcut icon" href="https://www.python.org/static/favicon.ico"/>
<meta name=generator content=Dookumentation> <link rel=stylesheet href="
https://storage.googleapis.com/code.getmdl.io/1.0.4/material.green-blue.min.css
"><style>body,details{background:linear-gradient(lightcyan,transparent),
linear-gradient(90deg,skyblue,transparent),linear-gradient(-90deg,lightblue,
transparent);width:100%;height:100%;background-blend-mode:screen}
section{display:flex;flex-wrap:wrap;justify-content:space-around}
details{border:1px gray solid;border-radius:9px;background:#fff;padding:9px;
margin:9px;min-width:480px;max-width:600px;flex:1;flex-grow:1;opacity:0.5;
white-space:pre-wrap;word-wrap:break-word;word-break:break-word}
details[open]{height:inherit;opacity:1};
@media screen and (max-width:550px) { #footer, h1 {display:none}; }</style>
<div class="mdl-layout mdl-js-layout mdl-layout--fixed-header">
<header class="mdl-layout__header"><div class="mdl-layout__header-row">
<span class="mdl-layout-title"><h1>&equiv; Dookumentation !</h1></span>
<div class="mdl-layout-spacer"></div><nav class="mdl-navigation">
        <a class="mdl-navigation__link" href="">Link</a>
        <a class="mdl-navigation__link" href="">Link</a>
        <a class="mdl-navigation__link" href="">Link</a>
        <a class="mdl-navigation__link" href="">Link</a>
</nav></div></header><br>
<section><details open><summary><b>Imports</b></summary> {%
if len(data.get('imports')):
    for _ in data['imports'].items():
        {{ _[0], _[1] }}
else:
    {{ '<p>No Imports!, Parser can not find any Imports!.' }}
{{ '</details> <details open> <summary> <b>Functions</b> </summary>' }}
if len(data.get('functions')):
    for _ in data['functions'].items():
        {{ _[0], _[1] }}
else:
    {{ '<p>No Functions!, Parser can not find any Functions!.' }}
{{ '</details> <details open> <summary> <b>Attributes</b> </summary>' }}
if len(data.get('attributes')):
    for _ in data['attributes'].items():
        {{ _[0], _[1] }}
else:
    {{ '<p>No Attributes!, Parser can not find any Attributes!.' }}
{{ '</details> <details open> <summary> <b>&hercon; Bugs</b> </summary>' }}
if len(data.get('pylama')):
    {{ '<h4> &star; You wrote 1 Bug every {0} Lines of Code!.</h4><ol>'.format(
       data['lines_per_bug']) }}
    for _ in data['pylama']:
        {{ '<li><b>Line {0} Column {1} found by {2}:</b> &raquo; {3}.'.format(
           _['lnum'], _['col'], _['linter'].upper(), _['text']) }}
else:
    if check_path and parse_options:  # Theres PyLama but theres no Errors.
        {{ '<p style="color:green">No Bugs !, PyLama cant find any Errors.' }}
    else:  # Theres NO PyLama, but may or may not be no Errors ?.
        {{ '<p style="color:red">No PyLama!, Install PyLama using PIP !.' }}
{{ '</details>' }}
if data.get('todo'):
    {{ '<details open><summary><b>&check; Things To Do</b></summary><ol>' }}
    for _ in data['todo']:
        {{ '<li><b>{0} on Line {1}</b> &raquo;&nbsp;&nbsp;&nbsp;{2}.'.format(
          _['type'].upper(), _['lnum'], _['text'][:99]) }}
    {{ '</ol></details>' }}
%}<details open><summary><b>&ccupssm; Statistics</b></summary><center>
<table class="mdl-data-table mdl-data-table--selectable">
<th>Lines Total<th>Lines of Code<th>Size (KiloBytes)<th>Characters</th><tr><td>
{%{{'{}<td>{}<td>{}<td>{}<tr>'.format(data['lines_total'], data['lines_code'],
                                      data['kilobytes'],data['characters'])}}%}
<th>Words<th>Punctuations<th>Permissions<th>Bugs ?</th><tr><td>
{%{{'{}<td>{}<td>{}<td>{}<tr>'.format(data['words'], data['punctuations'],
    data['permissions'], bool(len(data['pylama'])))}}%}
<th>SymLink ?<th>Writable ?<th>Executable ?<th>Readable ?</th><tr><td>
{%{{'{}<td>{}<td>{}<td>{}<tr>'.format(data['symlink'],data['writable'],
    data['executable'],data['readable']) }}%}
<th>Has Print()?<th>Has __import__()?<th>Has BreakPoints?<th>SheBang ?</th><tr>
<td>{%{{'{}<td>{}<td>{}<td>{}<tr>'.format(data['has_print'],
data['import_procedural'],data['has_set_trace'],data['has_shebang']) }}%}
</table><br><table class="mdl-data-table mdl-data-table--selectable">
<th>SHA-1 CheckSum Hash of the file (UTF-8)<tr><td>{%{{ data['sha1'] }}%}<tr>
<th>Date of last Modifications (ISO Format)<tr><td>{%{{ data['modified'] }}%}
<tr><th>Date of last Accessed (ISO Format)<tr><td>{%{{ data['accessed'] }}%}
</table></center></details><section>
<br><footer id=footer class="mdl-mini-footer">
<button class="mdl-button mdl-button--raised mdl-button--accent">JSON</button>
&nbsp;<a href="javascript:window.print()"><button
class="mdl-button mdl-button--raised mdl-button--accent">Print</button></a>
&nbsp;<a href="javascript:window.history.back()"><button
class="mdl-button mdl-button--raised mdl-button--accent">Back</button></a>
&nbsp;<a href="javascript:window.location.reload()"><button
class="mdl-button mdl-button--raised mdl-button--accent">Reload</button></a>
&nbsp;<a href="javascript:window.history.forward()"><button
class="mdl-button mdl-button--raised mdl-button--accent">Forward</button></a>
&nbsp;<a href="javascript:location.replace('view-source:'+location.href)">
<button class="mdl-button mdl-button--raised mdl-button--accent">Source
</button></a>&nbsp;<br>&nbsp;<br><div class="mdl-mini-footer__left-section">
<b class="mdl-logo">Dookumentation</b><ul class="mdl-mini-footer__link-list">
<li>Made with &hearts; & Python StdLibs by <a href={%{{__url__}}%}>Juan</a>!.
<li>Tested on Chromium,Chrome,Android,Firefox & Qupzilla.
<li>Share Dookumentation with friends and coworkers:
{%{{ (" <a href='https://twitter.com/home?status=I%20Like%20{n}!:%20{u}'>" +
"Twitter</a> <a href='https://plus.google.com/share?url={u}'>GooglePlus</a>"+
" <a href='http://www.facebook.com/share.php?u={u}&t=I%20Like%20{n}'>Facebook"+
"</a>").format(u=__url__, n="Dookumentation") }}%}</div></footer>"""


SVG = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg height="299%" width="299%" xmlns="http://www.w3.org/2000/svg"
style="font-family:Ubuntu" title="Dookumentation"><text title="Dookumentation">
<tspan x="9" y="50" style="font-size:4em">Dookumentation !</tspan>  {%
{{'<tspan x="9" y="99" style="font-size:2em"> Statistics </tspan>'}}
{{'<tspan x="9" y="120">Lines Total: {0}</tspan>'.format(data['lines_total'])}}
{{'<tspan x="150" y="120">Lines Code: {0}</tspan>'.format(data['lines_code'])}}
{{'<tspan x="300" y="120">Size (Kb.): {0}</tspan>'.format(data['kilobytes']) }}
{{'<tspan x="9" y="150">Characters: {0}.</tspan>'.format(data['characters']) }}
{{'<tspan x="150" y="150"> Words: {0}         </tspan>'.format(data['words'])}}
{{'<tspan x="300" y="150">Punct.: {0}  </tspan>'.format(data['punctuations'])}}
{{'<tspan x="9" y="180">Permissions: {0}</tspan>'.format(data['permissions'])}}
{{'<tspan x="150" y="180">Bugs ?: {0}.</tspan>'.format(bool(data['pylama'])) }}
{{'<tspan x="300" y="180"> SymLink ?: {0} </tspan> '.format(data['symlink']) }}
{{'<tspan x="9" y="210"> Writable ?: {0}. </tspan>'.format(data['writable']) }}
{{'<tspan x="150" y="210">Executable?:{0}</tspan>'.format(data['executable'])}}
{{'<tspan x="300" y="210">Readable ?: {0}.</tspan>'.format(data['readable']) }}
{{'<tspan x="9" y="240">Has Print()?: {0}</tspan>'.format(data['has_print']) }}
{{'<tspan x="150" y="240">__import__()?: {0}.</tspan>'.format(
    data['import_procedural'])}}
{{'<tspan x="300" y="240"> Has BreakPoints ?: {0}.</tspan>'.format(
    data['has_set_trace']) }}
{{'<tspan x="9" y="270"> SheBang ? {0}.</tspan>'.format(data['has_shebang']) }}
{{ '<tspan x="500" y="99" style="font-size:2em" title="Bugs">Bugs</tspan>' }}
if len(data.get('pylama')):
    {{'<tspan x="500" y="120"> You wrote 1 Bug every '}}
    {{'{0} Lines of Code !.</tspan>'.format(data['lines_per_bug']) }}
    for i, _ in enumerate(data['pylama']):
        {{'    <tspan x="500" y="{0}"> {1}. '.format(150 + i * 20, i) }}
        {{'    Line {0} Column {1} found by {2}: {3}.</tspan>'.format(
               _['lnum'], _['col'], _['linter'].upper(), _['text'][:99]) }}
else:
    if check_path and parse_options:  # Theres PyLama but theres no Errors.
        {{ '<tspan x="500" y="170" style="color:green"> No Bugs !. </tspan>' }}
    else:  # Theres NO PyLama, but may or may not be no Errors ?.
        {{ '<tspan x="500" y="170" style="color:red"> No PyLama !. </tspan>' }}
if len(data.get('todo')):
    {{ '<tspan x="1200" y="99" style="font-size:2em"> Things To Do</tspan>' }}
    for i, _ in enumerate(data['todo']):
        {{'    <tspan x="1200" y="{0}"> {1}. '.format(150 + i * 20, i) }}
        {{'    {0} on Line {1}: {2}. </tspan>'.format(
               _['type'].upper(), _['lnum'], _['text'][:99]) }}
{{'<tspan x="9" y="500" title="Import" style="font-size:2em">Imports</tspan>'}}
if len(data.get('imports')):
    for i, _ in enumerate(data['imports'].items()):
        {{'<tspan x="9" y="{0}">{1}. {2}</tspan>'.format(550 + i * 30, i,
          str(_)[:70])}}
else:
    {{ '<tspan x="9" y="550">No Imports!, Parser cant find Imports.</tspan>' }}
{{ '<tspan x="500" y="500" style="font-size:2em">Attributes</tspan>' }}
if len(data.get('attributes')):
    for i, _ in enumerate(data['attributes'].items()):
        {{'<tspan x="500" y="{0}">{1}. {2}</tspan>'.format(550 + i * 30, i,
          str(_)[:70])}}
else:
    {{ '<tspan x="9" y="550">No Attributes!, cant find Attributes.</tspan>' }}
{{ '<tspan x="1200" y="500" style="font-size:2em">Functions</tspan>' }}
if len(data.get('attributes')):
    for i, _ in enumerate(data['functions'].items()):
        {{'<tspan x="1200" y="{0}">{1}. {2}</tspan>'.format(550 + i * 30, i,
          str(_)[:70])}}
else:
    {{ '<tspan x="1200" y="550">No Functions!, cant find Functions.</tspan>' }}
%} <tspan x="700" y="25">Made with Python StdLibs by Juan</tspan><tspan x="700"
y="50"> Tested on Chromium, Chrome, Android, Firefox and Qupzilla. </tspan>
<tspan x="1200" y="25" title="Dookumentation"> {%{{ __url__ }} %} </tspan>
<tspan x="1200" y="50" title="Dookumentation">{%{{data['generator']}}%}</tspan>
</text>ERROR: Your Browser does not support SVG</svg><!-- Dookumentation -->"""


MD = """# Dookumentation\n\n\n### [Imports](#imports "Imports")\n\n\n {%
if len(data.get('imports')):
    for _ in data['imports'].items():
        {{ _[0], _[1] }}
else:
    {{ '- No Imports!, Parser can not find any Imports!.' + os.linesep }}
{{os.linesep * 2 + '### [Functions](#functions "Functions")' + os.linesep * 2}}
if len(data.get('functions')):
    for _ in data['functions'].items():
        {{ _[0], _[1] }}
else:
    {{ '- No Functions!, Parser can not find any Functions!.' + os.linesep}}
{{os.linesep*2 + '### [Attributes](#attributes "Attributes")' + os.linesep*2}}
if len(data.get('attributes')):
    for _ in data['attributes'].items():
        {{ _[0], _[1] }}
else:
    {{ '- No Attributes!, Parser can not find any Attributes!.' + os.linesep }}
{{ os.linesep * 2 + '### [&hercon; Bugs](#bugs "Bugs")' + os.linesep * 2 }}
if len(data.get('pylama')):
    {{ '- &star; You wrote 1 Bug every {0} Lines of Code!.{1}'.format(
       data['lines_per_bug'], os.linesep * 2) }}
    for _ in data['pylama']:
        {{ '- Line {0} Column {1} found by {2}: &raquo; {3}.{4}'.format(
           _['lnum'], _['col'], _['linter'].upper(), _['text'], os.linesep) }}
else:
    if check_path and parse_options:  # Theres PyLama but theres no Errors.
        {{ '<p style="color:green">No Bugs !, PyLama cant find any Errors.' }}
    else:  # Theres NO PyLama, but may or may not be no Errors ?.
        {{ '<p style="color:red">No PyLama!, Install PyLama using PIP !.' }}
if data.get('todo'):
    {{ os.linesep*2+'### [&check; Things To Do](#todo "To Do")'+os.linesep*2 }}
    for _ in data['todo']:
        {{ '- {0} on Line {1} &raquo;&nbsp;&nbsp;&nbsp;{2}.{3}'.format(
          _['type'].upper(), _['lnum'], str(_['text'])[:99],os.linesep) }}
%} \n\n\n### [&ccupssm; Statistics](#statistics "Statistics")\n\n
|  Lines Total  | Lines of Code  |  Size (KiloBytes)  |  Characters  |
| ------------- | -------------- | ------------------ | ------------ |
{%{{'|  {}  |  {}  |  {}  |  {}  |'.format(data['lines_total'],
    data['lines_code'],data['kilobytes'],data['characters'])}}%} \n\n
|  Words  |  Punctuations  |  Permissions  |  Bugs ?  |
| ------- | -------------- | ------------- | -------- |
{%{{'|  {}  |  {}  |  {}  |  {}  |'.format(data['words'], data['punctuations'],
    data['permissions'], bool(len(data['pylama'])))}}%} \n\n
|  SymLink ?  |  Writable ?  |  Executable ?  |  Readable ?  |
| ----------- | ------------ | -------------- | ------------ |
{%{{'|  {}  |  {}  |  {}  |  {}  |'.format(data['symlink'],data['writable'],
                           data['executable'],data['readable']) }}%} \n\n
|  Has Print()?  |  Has import()?  |  Has BreakPoints ?  |  SheBang ?  |
| -------------- | --------------- | ------------------- | ----------- |
{%{{'|  {}  |  {}  |  {}  |  {}  |'.format(data['has_print'],
    data['import_procedural'],data['has_set_trace'],data['has_shebang']) }}%}
\n\n|  SHA-1 CheckSum Hash of the file (UTF-8)  |
| --------------------------------------------- |
|  {%{{ data['sha1'] }}%}  |\n\n
| Date of last Modification (ISO Format) | Date of last Accessed (ISO Format) |
| -------------------------------------- | ---------------------------------- |
|  {%{{ data['modified'] + " | " + data['accessed'] }}%}  |\n\n
<hr><details title=About><summary><i>Dookumentation !</i></summary><br><sub>
Made with Python StdLibs by Juan!. Tested on Chromium,Chrome,Android,Qupzilla.
Share Dookumentation with friends and coworkers:{%
{{('[Twitter](https://twitter.com/home?status=I%20Like%20{n}!:%20{u} "{n}"), '
   '[GooglePlus](https://plus.google.com/share?url={u} "{n}"), '
   '[Facebook](http://www.facebook.com/share.php?u={u}&t=I%20Like%20{n} "{n}")'
   ).format(u=__url__, n="Dookumentation") }} %}  <!-- Dookumentation -->   """


###############################################################################


class Templar(str):

    """Templar is a tiny Template Engine that Render and Runs native Python."""

    def __init__(self, template):
        """Init the Template class."""
        self.tokens = self.compile(template.strip())

    @classmethod
    def from_file(cls, fl):
        """Load template from file.A str/file-like object supporting read()."""
        return cls(str(open(fl).read() if isinstance(fl, str) else fl.read()))

    def compile(self, t):
        """Parse and Compile all Tokens found on the template string t."""
        tokens = []
        for i, p in enumerate(re.compile("\{\%(.*?)\%\}", re.DOTALL).split(t)):
            if not p or not p.strip():
                continue
            elif i % 2 == 0:
                tokens.append((False, p.replace("{\\%", "{%")))
            else:
                lines = tuple(p.replace("%\\}", "%}").replace(
                    "{{", "spit(").replace("}}", "); ") .splitlines())
                mar = min(len(_) - len(_.lstrip()) for _ in lines if _.strip())
                al = "\n".join(line_of_code[mar:] for line_of_code in lines)
                tokens.append((True, compile(al, "<t {}>".format(al), "exec")))
        return tokens

    def render(__self, __namespace={}, mini=False, **kw):
        """Render template from __namespace dict + **kw added to namespace."""
        html = []
        __namespace.update(kw, **globals())
        __namespace["spit"] = lambda *arg: [html.append(str(_)) for _ in arg]
        for is_code, value in __self.tokens:
            eval(value, __namespace) if is_code else html.append(value)
        return re.sub('>\s+<', '> <', "".join(html)) if mini else "".join(html)

    __call__ = render  # shorthand


###############################################################################


class PyParse(object):

    """Python source code file path to JSON string meta-data Parser."""

    def parse_file(self, filepath):
        """Parse file,create info Imports,Class,Function,Attr,Decorator,etc."""
        print('Parsing file: {0}'.format(filepath))
        source = ""
        with open(filepath, 'r', encoding="utf-8") as python_file_to_read:
            source = python_file_to_read.read()
        if source:
            symbols = self.get_symbols(source, filepath)
            return symbols

    def get_symbols(self, source, filename=''):
        """Parse module code to get Classes, Functions and Assigns."""
        symbols, globalAttributes, globalFunctions, classes = {}, {}, {}, {}
        try:
            module = ast.parse(source)
        except:
            print("The file contains syntax errors: {0}".format(filename))
            return {}
        for symbol in module.body:
            if symbol.__class__ is ast.Assign:
                result = self.parse_assign(symbol)
                globalAttributes.update(result[0])
                globalAttributes.update(result[1])
            elif symbol.__class__ is ast.FunctionDef:
                result = self.parse_function(symbol)
                globalFunctions[result['name']] = result
            elif symbol.__class__ is ast.ClassDef:
                result = self.parse_class(symbol)
                classes[result['name']] = result
        if globalAttributes:
            symbols['attributes'] = globalAttributes
        if globalFunctions:
            symbols['functions'] = globalFunctions
        if classes:
            symbols['classes'] = classes
        symbols['imports'] = self.parse_import(module)
        symbols['docstring'] = ast.get_docstring(module, clean=True)
        return symbols

    def expand_attribute(self, attribute):
        """Expand attribute to get more info about itself."""
        parent_name = []
        while attribute.__class__ is ast.Attribute:
            parent_name.append(attribute.attr)
            attribute = attribute.value
        name = '.'.join(reversed(parent_name))
        attribute_id = ''
        if attribute.__class__ is ast.Name:
            attribute_id = attribute.id
        elif attribute.__class__ is ast.Call:
            if attribute.func.__class__ is ast.Attribute:
                attribute_id = "{0}.{1}()".format(
                    self.expand_attribute(attribute.func.value),
                    attribute.func.attr)
            else:
                attribute_id = "{0}()".format(attribute.func.id)
        name = attribute_id if name == "" else "{0}.{1}".format(attribute_id, name)
        return name

    def parse_assign(self, symbol):
        """Parse assign and get info from itself."""
        assigns, attributes = {}, {}
        for var in symbol.targets:
            if var.__class__ == ast.Attribute:
                attributes[var.attr] = var.lineno
            elif var.__class__ == ast.Name:
                assigns[var.id] = var.lineno
        return (assigns, attributes)

    def parse_class(self, symbol):
        """Parse class and get info from itself."""
        docstring, attr, func, decorators = "", {}, {}, []
        name = symbol.name + '('
        name += ', '.join([
            self.expand_attribute(base) for base in symbol.bases])
        name += ')'
        for sym in symbol.body:
            if sym.__class__ is ast.Assign:
                result = self.parse_assign(sym)
                attr.update(result[0])
                attr.update(result[1])
            elif sym.__class__ is ast.FunctionDef:
                result = self.parse_function(sym)
                attr.update(result['attrs'])
                func[result['name']] = result
        docstring = ast.get_docstring(symbol, clean=True)
        lineno = symbol.lineno
        for decorator in symbol.decorator_list:
            decorators.append(self.expand_attribute(decorator))
        return {
            'name': name, 'attributes': attr, 'functions': func,
            'lineno': lineno, 'docstring': docstring, 'decorators': decorators}

    def parse_function(self, symbol):
        """Parse function and get info from itself."""
        docstring, attrs, decorators, defaults, arguments = "", {}, [], [], []
        tipes = {_ast.Tuple: "tuple", _ast.List: "list", _ast.Str: "str",
                 _ast.Dict: "dict", _ast.Num: "int", _ast.Call: "function()"}
        func_name = symbol.name + '('
        for value in symbol.args.defaults:
            defaults.append(value)
        for arg in reversed(symbol.args.args):
            if arg.__class__ is not _ast.Name or arg.id == 'self':
                continue
            argument = arg.id
            if defaults:
                value = defaults.pop()
                arg_default = tipes.get(value.__class__, None)
                if arg_default is None:
                    if value.__class__ is _ast.Attribute:
                        arg_default = self.expand_attribute(value)
                    elif value.__class__ is _ast.Name:
                        arg_default = value.id
                    else:
                        arg_default = 'object'
                argument += '=' + arg_default
            arguments.append(argument)
        func_name += ', '.join(reversed(arguments))
        if symbol.args.vararg is not None:
            if not func_name.endswith('('):
                func_name += ', '
            func_name += '*' + symbol.args.vararg
        if symbol.args.kwarg is not None:
            if not func_name.endswith('('):
                func_name += ', '
            func_name += '**' + symbol.args.kwarg
        func_name += ')'
        for sym in symbol.body:
            if sym.__class__ is ast.Assign:
                result = self.parse_assign(sym)
                attrs.update(result[1])
        docstring = ast.get_docstring(symbol, clean=True)
        lineno = symbol.lineno
        for decorator in symbol.decorator_list:
            decorators.append(self.expand_attribute(decorator))
        return {'name': func_name, 'lineno': lineno, 'attrs': attrs,
                'docstring': docstring, 'decorators': decorators}

    def parse_import(self, module):
        """Parse import, get info from itself."""
        imports, from_imports = {}, {}
        for simbolos in module.body:
            if type(simbolos) is ast.Import:
                for item in simbolos.names:
                    imports[item.name] = {
                        "asname": item.asname if item.asname else "unknown",
                        "lineno": simbolos.lineno}
            if type(simbolos) is ast.ImportFrom:
                for item in simbolos.names:
                    from_imports[item.name] = {
                        "module": simbolos.module, "lineno": simbolos.lineno,
                        "asname": item.asname if item.asname else "unknown"}
        return {"imports": imports, "from_imports": from_imports}


##############################################################################


def typecheck(f):
    """Decorator for Python3 annotations to type-check inputs and outputs."""
    def __check_annotations(tipe):
        _type, is_ok = None, isinstance(tipe, (type, tuple, type(None)))
        if is_ok:  # Annotations can be Type or Tuple or None
            _type = tipe if isinstance(tipe, tuple) else tuple((tipe, ))
            if None in _type:  # if None on tuple replace with type(None)
                _type = tuple([_ if _ is not None else type(_) for _ in _type])
        return _type, is_ok

    @functools.wraps(f)  # wrap a function or method to Type Check it.
    def decorated(*args, **kwargs):
        msg = "Type check error: {0} must be {1} but is {2} on function {3}()."
        notations, f_name = tuple(f.__annotations__.keys()), f.__code__.co_name
        for i, name in enumerate(f.__code__.co_varnames):
            if name not in notations:
                continue  # this arg name has no annotation then skip it.
            _type, is_ok = __check_annotations(f.__annotations__.get(name))
            if is_ok:  # Force to tuple
                if i < len(args) and not isinstance(args[i], _type):
                    log.critical(msg.format(repr(args[i])[:50], _type,
                                            type(args[i]), f_name))
                elif name in kwargs and not isinstance(kwargs[name], _type):
                    log.critical(msg.format(repr(kwargs[name])[:50], _type,
                                            type(kwargs[name]), f_name))
        out = f(*args, **kwargs)
        _type, is_ok = __check_annotations(f.__annotations__.get("return"))
        if is_ok and not isinstance(out, _type) and "return" in notations:
            log.critical(msg.format(repr(out)[:50], _type, type(out), f_name))
        return out    # The output result of function or method.
    return decorated  # The decorated function or method.


@typecheck
def walkdir_to_filelist(where: str, target: tuple, omit: str) -> tuple:
    """Perform full walk of where, gather full path of all files."""
    log.debug("""Recursively Scanning {0}, searching for {1}, and ignoring {2}.
    """.format(where, target, omit))
    return tuple([os.path.join(root, f)
                  for root, d, files in os.walk(where, followlinks=True)
                  for f in files if not f.startswith('.')  # ignore hidden
                  and not f.endswith(omit)  # not process processed file
                  and f.endswith(target)])  # only process target files


@typecheck
def check_working_folder(folder_to_check: str=os.path.expanduser("~")) -> bool:
    """Check working folder,passed argument,for everything that can go wrong.

    >>> check_working_folder()
    True
    """
    folder_to_check = os.path.join(os.path.abspath(folder_to_check), "doc")
    log.debug("Checking the Working Folder: '{0}'".format(folder_to_check))
    if not isinstance(folder_to_check, str):  # What if folder is not a string.
        log.critical("Folder {0} is not String type!.".format(folder_to_check))
        return False
    elif os.path.isfile(folder_to_check):
        log.info("Folder {0} is File or Relative Path".format(folder_to_check))
        return True
    elif not os.path.isdir(folder_to_check):  # What if folder is not a folder.
        log.debug("Folder {0} does not exist !.".format(folder_to_check))
        os.makedirs(folder_to_check, exist_ok=True)
        log.warning("Creating Required Folder: {0}/".format(folder_to_check))
    elif not os.access(folder_to_check, os.R_OK):  # destination no Readable.
        log.critical("Folder {0} not Readable !.".format(folder_to_check))
        return False
    elif not os.access(folder_to_check, os.W_OK):  # destination no Writable.
        log.critical("Folder {0} Not Writable !.".format(folder_to_check))
        return False
    elif disk_usage and os.path.exists(folder_to_check):  # No free space.
        hdd = int(disk_usage(folder_to_check).free / 1024 / 1024 / 1024)
        if hdd:  # > 1 Gb
            log.info("Total Free Space: ~{0} GigaBytes.".format(hdd))
        else:  # < 1 Gb
            log.critical("Total Free Space is < 1 GigaByte; Epic Fail !.")
            return False
    basic_folders = ("json", "html", "md", "svg", "plugins")  # sub-folders.
    for subfolder in [os.path.join(folder_to_check, _) for _ in basic_folders]:
        if not os.path.isdir(subfolder):
            log.warning("Creating Required Sub-Folder: {0}/".format(subfolder))
            os.makedirs(subfolder, exist_ok=True)
        if not os.path.isdir(subfolder):
            return False
    return True


def process_multiple_files(file_path):
    """Process multiple Python files with multiprocessing."""
    log.debug("Process {0} is Processing {1}.".format(os.getpid(), file_path))
    if args.watch:
        previous = int(os.stat(file_path).st_mtime)
        log.info("Process {0} is Watching {1}.".format(os.getpid(), file_path))
        while True:
            actual = int(os.stat(file_path).st_mtime)
            if previous == actual:
                sleep(60)
            else:
                previous = actual
                log.debug("Modification detected on '{0}'.".format(file_path))
                process_single_python_file(file_path)
    else:
        process_single_python_file(file_path)


@typecheck
def prefixer_extensioner(file_path: str) -> str:
    """Take a file path and safely prepend a prefix and change extension.

    This is needed because filepath.replace('.foo', '.bar') sometimes may
    replace '/folder.foo/file.foo' into '/folder.bar/file.bar' wrong!.
    """
    log.debug("Prepending '{0}' Prefix to {1}.".format(args.prefix, file_path))
    extension = os.path.splitext(file_path)[1].lower()
    filenames = os.path.splitext(os.path.basename(file_path))[0]
    filenames = args.prefix + filenames if args.prefix else filenames
    dir_names = os.path.dirname(file_path)
    file_path = os.path.join(dir_names, filenames + extension)
    return file_path


def python_file_to_json_meta(python_file_path):
    """Take python source code string and extract meta-data as json file."""
    json_meta = {}
    log.debug("INPUT: Reading Python file {0}.".format(python_file_path))
    with open(python_file_path, encoding="utf-8-sig") as python_file:
        original_python = python_file.read()
    # Miscellaneous
    json_meta["generator"] = __doc__.splitlines()[0] + " " + __version__
    # Paths
    json_meta["relpath"] = os.path.relpath(python_file_path)
    json_meta["basename"] = os.path.basename(python_file_path)
    json_meta["dirname"] = os.path.dirname(python_file_path)
    json_meta["fullpath"] = python_file_path
    # Statistics
    json_meta["lines_total"] = len(original_python.splitlines())
    json_meta["characters"] = len(original_python.replace("\n", ""))
    json_meta["kilobytes"] = int(os.path.getsize(python_file_path) / 1024)
    json_meta["lines_code"] = len(  # DocString count as code,because DocTests.
        [_ for _ in original_python.splitlines()
         if len(_.strip()) and not _.strip().startswith("#")])
    json_meta["words"] = len([_ for _ in re.sub(
        "[^a-zA-Z0-9 ]", "", original_python).split(" ") if _ != ""])
    json_meta["punctuations"] = len(
        [_ for _ in original_python if _ in punctuation])
    # File Properties
    json_meta["permissions"] = int(oct(os.stat(python_file_path).st_mode)[-3:])
    json_meta["writable"] = os.access(python_file_path, os.W_OK)
    json_meta["executable"] = os.access(python_file_path, os.X_OK)
    json_meta["readable"] = os.access(python_file_path, os.R_OK)
    json_meta["symlink"] = os.path.islink(python_file_path)
    json_meta["sha1"] = sha1(original_python.encode("utf-8")).hexdigest()
    json_meta["import_procedural"] = "__import__(" in original_python
    json_meta["has_set_trace"] = ".set_trace()" in original_python
    json_meta["has_print"] = "print(" in original_python
    json_meta["has_shebang"] = re.findall('^#!/.*python', original_python)
    json_meta["accessed"] = datetime.utcfromtimestamp(os.path.getatime(
        python_file_path)).isoformat(" ").split(".")[0]
    json_meta["modified"] = datetime.utcfromtimestamp(os.path.getmtime(
        python_file_path)).isoformat(" ").split(".")[0]
    # Bugs
    json_meta["pylama"] = [
        pylama_error.__dict__["_info"]  # dict with PyLama Errors from linters
        for pylama_error in check_path(parse_options((python_file_path, )))
        ] if check_path and parse_options else []  # if no PyLama empty list
    if len(json_meta["pylama"]) > 1 and json_meta["lines_total"]:
        json_meta["lines_per_bug"] = int(
            json_meta["lines_total"] / len(json_meta["pylama"]))
    regex_for_todo, all_todo = r"(  # TODO|  # FIXME|  # OPTIMIZE|  # BUG)", []
    for index, line in enumerate(original_python.splitlines()):
        if re.findall(regex_for_todo, line):
            all_todo.append({  # Using same keywords as PyLama array.
                "lnum": index + 1, "text": line.strip(),
                "type": re.findall(regex_for_todo, line)[0].replace(
                    "#", "").strip().lower()})
    if len(all_todo):
        json_meta["todo"] = all_todo  # this is all todo, fixme,etc on the code
    # Procedural from Parser
    for key, value in PyParse().parse_file(python_file_path).items():
        json_meta[key] = value  # "some_code_entity": "value_of_that_entity",
    return json_meta  # return the Big Ol' JSON


@typecheck
def json_pretty(json_dict: dict) -> str:
    """Pretty-Printing JSON data from dictionary to string."""
    _json = dumps(json_dict, sort_keys=1, indent=4, separators=(",\n", ": "))
    posible_ends = tuple('true false , " ] 0 1 2 3 4 5 6 7 8 9 \n'.split(" "))
    max_indent, justified_json = 1, ""
    for json_line in _json.splitlines():
        if len(json_line.split(":")) >= 2 and json_line.endswith(posible_ends):
            lenght = len(json_line.split(":")[0].rstrip()) + 1
            max_indent = lenght if lenght > max_indent else max_indent
            max_indent = max_indent if max_indent <= 80 else 80  # Limit indent
    for line_of_json in _json.splitlines():
        condition_1 = max_indent > 1 and len(line_of_json.split(":")) >= 2
        condition_2 = line_of_json.endswith(posible_ends) and len(line_of_json)
        if condition_1 and condition_2:
            propert_len = len(line_of_json.split(":")[0].rstrip()) + 1
            xtra_spaces = " " * (max_indent + 1 - propert_len)
            xtra_spaces = ":" + xtra_spaces
            justified_line_of_json = ""
            justified_line_of_json = line_of_json.split(":")[0].rstrip()
            justified_line_of_json += xtra_spaces
            justified_line_of_json += "".join(
                line_of_json.split(":")[1:len(line_of_json.split(":"))])
            justified_json += justified_line_of_json + "\n"
        else:
            justified_json += line_of_json + "\n"
    return str("\n\n" + justified_json if max_indent > 1 else _json)


def json_meta_to_html(json_meta):
    """Take json_meta string and convert it to HTML5+CSS3 file."""
    html = Templar(HTML)  # instantiate and give it template string,then render
    return html(data=json_meta, mini=True)  # mini is HTML Minification.


def json_meta_to_svg(json_meta):
    """Take json_meta string and convert it to SVG (for HTML5) file."""
    svg = Templar(SVG)  # instantiate and give it template string,then render
    return svg(data=json_meta, mini=True)  # mini is SVG Minification.


def json_meta_to_md(json_meta):
    """Take json_meta string and convert it to MD MarkDown file."""
    md = Templar(MD)  # instantiate and give it template string,then render
    return md(data=json_meta, mini=False)  # Do NOT mini, it breaks MarkDown!!.


def json_meta_to_plugins(plugin_folder, python_file_path, json_meta):
    """Load and Run Plugins from Plugins folder."""
    if not all((plugin_folder, python_file_path, json_meta)):
        return
    plgns = [os.path.join(plugin_folder, _)  for _ in os.listdir(plugin_folder)
             if "template" == os.path.splitext(_)[0] and not _.startswith(".")]
    for template_to_render in tuple(sorted(plgns)):
        subdir = os.path.splitext(template_to_render)[-1].replace(".", "")
        plugin_dr = os.path.join(os.path.dirname(args.fullpath), "doc", subdir)
        if not os.path.isdir(plugin_dr):  # Create Sub-Folder for nre Plugin
            log.warning("Creating Required Sub-Folder: {0}/".format(plugin_dr))
            os.makedirs(plugin_dr, exist_ok=True)
        log.debug("INPUT: Reading Template {0}.".format(template_to_render))
        with open(template_to_render, "r", encoding="utf-8") as template_file:
            template_plugin = template_file.read().strip()
        custom = Templar(template_plugin)  # instantiate and give it template
        custom_rendered = custom(data=json_meta, mini=False)
        new_file = os.path.join(plugin_dr, os.path.basename(python_file_path) +
                                os.path.splitext(template_to_render)[-1])
        log.debug("OUTPUT: Writing Plugin Documentation {0}.".format(new_file))
        with open(new_file, "w", encoding="utf-8") as new_file_from_plugin:
            new_file_from_plugin.write(custom_rendered)
    return plgns


@typecheck
def process_single_python_file(python_file_path: str):
    """Process a single Python file."""
    log.info("Processing Python file: {0}".format(python_file_path))
    global args
    is_a_file = os.path.isfile(python_file_path)
    is_readable = os.access(python_file_path, os.R_OK)
    if is_a_file and is_readable:
        json_meta = python_file_to_json_meta(python_file_path)
    new_json_file = os.path.join(
        os.path.dirname(args.fullpath), "doc", "json",
        os.path.basename(python_file_path) + ".json")
    log.debug("OUTPUT: Writing MetaData JSON file {0}.".format(new_json_file))
    with open(new_json_file, "w", encoding="utf-8") as json_file:
            json_file.write(json_pretty(json_meta))
    html = json_meta_to_html(json_meta)
    new_html_file = os.path.join(
        os.path.dirname(args.fullpath), "doc", "html",
        os.path.basename(python_file_path) + ".html")
    log.debug("OUTPUT: Writing HTML5 Documentation {0}.".format(new_html_file))
    with open(new_html_file, "w", encoding="utf-8") as html_file:
            html_file.write(html)
    md = json_meta_to_md(json_meta)
    new_md_file = os.path.join(
        os.path.dirname(args.fullpath), "doc", "md",
        os.path.basename(python_file_path) + ".md")
    log.debug("OUTPUT: Writing MD Documentation {0}.".format(new_md_file))
    with open(new_md_file, "w", encoding="utf-8") as md_file:
            md_file.write(md)
    svg = json_meta_to_svg(json_meta)
    new_svg_file = os.path.join(
        os.path.dirname(args.fullpath), "doc", "svg",
        os.path.basename(python_file_path) + ".svg")
    log.debug("OUTPUT: Writing SVG Documentation {0}.".format(new_svg_file))
    with open(new_svg_file, "w", encoding="utf-8") as svg_file:
            svg_file.write(svg)
    plugin_dir = os.path.join(os.path.dirname(args.fullpath), "doc", "plugins")
    log.debug("Checking for Plugins and Running from {0}.".format(plugin_dir))
    json_meta_to_plugins(plugin_dir, python_file_path, json_meta)


###############################################################################


def check_for_updates():
    """Method to check for updates from Git repo versus this version."""
    this_version = str(open(__file__).read())
    last_version = str(request.urlopen(__source__).read().decode("utf8"))
    if this_version != last_version:
        log.warning("Theres new Version available!,Update from " + __source__)
    else:
        log.info("No new updates!,You have the lastest version of this app.")


@typecheck
def make_root_check_and_encoding_debug() -> bool:
    """Debug and Log Encodings and Check for root/administrator,return Boolean.

    >>> make_root_check_and_encoding_debug()
    True
    """
    log.info(__doc__)
    log.debug("Python {0} on {1}.".format(python_version(), platform()))
    log.debug("STDIN Encoding: {0}.".format(sys.stdin.encoding))
    log.debug("STDERR Encoding: {0}.".format(sys.stderr.encoding))
    log.debug("STDOUT Encoding:{}".format(getattr(sys.stdout, "encoding", "")))
    log.debug("Default Encoding: {0}.".format(sys.getdefaultencoding()))
    log.debug("FileSystem Encoding: {0}.".format(sys.getfilesystemencoding()))
    log.debug("PYTHONIOENCODING Encoding: {0}.".format(
        os.environ.get("PYTHONIOENCODING", None)))
    os.environ["PYTHONIOENCODING"] = "utf-8"
    sys.dont_write_bytecode = True
    if not sys.platform.startswith("win"):  # root check
        if not os.geteuid():
            log.critical("Runing as root is not Recommended,NOT Run as root!.")
            return False
    elif sys.platform.startswith("win"):  # administrator check
        if getuser().lower().startswith("admin"):
            log.critical("Runing as Administrator is not Recommended!.")
            return False
    return True


@typecheck
def set_process_name_and_cpu_priority(name: str) -> bool:
    """Set process name and cpu priority.

    >>> set_process_name_and_cpu_priority("test_test")
    True
    """
    try:
        os.nice(19)  # smooth cpu priority
        libc = cdll.LoadLibrary("libc.so.6")  # set process name
        buff = create_string_buffer(len(name.lower().strip()) + 1)
        buff.value = bytes(name.lower().strip().encode("utf-8"))
        libc.prctl(15, byref(buff), 0, 0, 0)
    except Exception:
        return False  # this may fail on windows and its normal, so be silent.
    else:
        log.debug("Process Name set to: {0}.".format(name))
        return True


@typecheck
def set_single_instance(name: str, single_instance: bool=True, port: int=8888):
    """Set process name and cpu priority, return socket.socket object or None.

    >>> isinstance(set_single_instance("test"), socket.socket)
    True
    """
    __lock = None
    if single_instance:
        try:  # Single instance app ~crossplatform, uses udp socket.
            log.info("Creating Abstract UDP Socket Lock for Single Instance.")
            __lock = socket.socket(
                socket.AF_UNIX if sys.platform.startswith("linux")
                else socket.AF_INET, socket.SOCK_STREAM)
            __lock.bind(
                "\0_{name}__lock".format(name=str(name).lower().strip())
                if sys.platform.startswith("linux") else ("127.0.0.1", port))
        except socket.error as e:
            log.warning(e)
        else:
            log.info("Socket Lock for Single Instance: {0}.".format(__lock))
    else:  # if multiple instance want to touch same file bad things can happen
        log.warning("Multiple instance on same file can cause Race Condition.")
    return __lock


@typecheck
def make_logger(name: str=str(os.getpid())):
    """Build and return a Logging Logger."""
    if not sys.platform.startswith("win") and sys.stderr.isatty():
        def add_color_emit_ansi(fn):
            """Add methods we need to the class."""
            def new(*args):
                """Method overload."""
                if len(args) == 2:
                    new_args = (args[0], copy(args[1]))
                else:
                    new_args = (args[0], copy(args[1]), args[2:])
                if hasattr(args[0], 'baseFilename'):
                    return fn(*args)
                levelno = new_args[1].levelno
                if levelno >= 50:
                    color = '\x1b[31;5;7m\n '  # blinking red with black
                elif levelno >= 40:
                    color = '\x1b[31m'  # red
                elif levelno >= 30:
                    color = '\x1b[33m'  # yellow
                elif levelno >= 20:
                    color = '\x1b[32m'  # green
                elif levelno >= 10:
                    color = '\x1b[35m'  # pink
                else:
                    color = '\x1b[0m'  # normal
                try:
                    new_args[1].msg = color + str(new_args[1].msg) + ' \x1b[0m'
                except Exception as reason:
                    print(reason)  # Do not use log here.
                return fn(*new_args)
            return new
        # all non-Windows platforms support ANSI Colors so we use them
        log.StreamHandler.emit = add_color_emit_ansi(log.StreamHandler.emit)
    else:
        log.debug("Colored Logs not supported on {0}.".format(sys.platform))
    log_file = os.path.join(gettempdir(), str(name).lower().strip() + ".log")
    log.basicConfig(level=-1, filemode="w", filename=log_file,
                    format="%(levelname)s:%(asctime)s %(message)s %(lineno)s")
    log.getLogger().addHandler(log.StreamHandler(sys.stderr))
    adrs = "/dev/log" if sys.platform.startswith("lin") else "/var/run/syslog"
    try:
        handler = log.handlers.SysLogHandler(address=adrs)
    except:
        log.debug("Unix SysLog Server not found,ignored Logging to SysLog.")
    else:
        log.addHandler(handler)
    log.debug("Logger created with Log file at: {0}.".format(log_file))
    return log


@typecheck
def make_post_execution_message(app: str=__doc__.splitlines()[0].strip()):
    """Simple Post-Execution Message with information about RAM and Time.

    >>> make_post_execution_message() >= 0
    True
    """
    ram_use, ram_all = 0, 0
    if sys.platform.startswith("linux"):
        ram_use = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss *
                    resource.getpagesize() / 1024 / 1024 if resource else 0)
        ram_all = int(os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
                      / 1024 / 1024 if hasattr(os, "sysconf") else 0)
    msg = "Total Maximum RAM Memory used: ~{0} of {1} MegaBytes.".format(
        ram_use, ram_all)
    log.info(msg)
    if start_time and datetime:
        log.info("Total Working Time: {0}".format(datetime.now() - start_time))
    if randint(0, 100) < 25:  # ~25% chance to see the message,dont get on logs
        print("Thanks for using this App,share your experience!{0}".format("""
        Twitter: https://twitter.com/home?status=I%20Like%20{n}!:%20{u}
        Facebook: https://www.facebook.com/share.php?u={u}&t=I%20Like%20{n}
        G+: https://plus.google.com/share?url={u}""".format(u=__url__, n=app)))
    return msg


def make_arguments_parser():
    """Build and return a command line agument parser."""
    # Parse command line arguments.
    parser = ArgumentParser(description=__doc__, epilog="""Dookumentation:
    Takes file or folder full path string and process all Python code found.
    If argument is not file/folder will fail.
    Watch works for whole folders, with minimum of ~60 Secs between runs.""")
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('fullpath', metavar='fullpath', type=str,
                        help='Full path to local file or folder.')
    parser.add_argument('--prefix', type=str,
                        help="Prefix string to prepend on output filenames.")
    parser.add_argument('--timestamp', action='store_true',
                        help="Add a Time Stamp on all Doc output files.")
    parser.add_argument('--quiet', action='store_true',
                        help="Quiet, Silent, force disable all Logging.")
    parser.add_argument('--checkupdates', action='store_true',
                        help="Check for Updates from Internet while running.")
    parser.add_argument('--after', type=str,
                        help="Command to execute after run (Experimental).")
    parser.add_argument('--before', type=str,
                        help="Command to execute before run (Experimental).")
    parser.add_argument('--watch', action='store_true',
                        help="Re-Process if file changes (Experimental).")
    global args
    args = parser.parse_args()


def main():
    """Main Loop."""
    make_arguments_parser()
    make_logger("dookumentation")
    make_root_check_and_encoding_debug()
    set_process_name_and_cpu_priority("dookumentation")
    set_single_instance("dookumentation")
    if args.checkupdates:
        check_for_updates()
    if args.quiet:
        log.disable(log.CRITICAL)
    log.info(__doc__ + __version__)
    check_working_folder(os.path.dirname(args.fullpath))
    if args.before and getoutput:
        log.info(getoutput(str(args.before)))
    # Work based on if argument is file or folder, folder is slower.
    if os.path.isfile(args.fullpath
                      ) and args.fullpath.endswith((".py", ".pyw")):
        log.info("Target is a PY / PYW Source Code File.")
        list_of_files = str(args.fullpath)
        process_single_python_file(args.fullpath)
    elif os.path.isdir(args.fullpath):
        log.info("Target is a Folder with PY / PYW Source Code  Files.")
        log.warning("Processing a whole Folder may take some time...")
        list_of_files = walkdir_to_filelist(args.fullpath, (".py", ".pyw"), [])
        pool = Pool(cpu_count())  # Multiprocessing Async
        pool.map_async(process_multiple_files, list_of_files)
        pool.close()
        pool.join()
    else:
        log.critical("File or folder not found,or cant be read,or I/O Error.")
        sys.exit(1)
    if args.after and getoutput:
        log.info(getoutput(str(args.after)))
    log.info('-' * 80)
    log.info('Files Processed: {0}.'.format(list_of_files))
    log.info('Number of Files Processed: ~{0}.'.format(
        len(list_of_files) if isinstance(list_of_files, tuple) else 1))
    make_post_execution_message()


if __name__ in '__main__':
    main()

#! /usr/bin/env python
# coding: utf-8
#
# Copyright (c) 2020 JR Oakes
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os

from seodeploy.lib.modules import ModuleBase
from seodeploy.lib.config import Config

CONFIG = Config(module="headless")

os.environ["PYPPETEER_CHROMIUM_REVISION"] = str(
    CONFIG.headless.PYPPETEER_CHROMIUM_REVISION
)

from .functions import run_render  # noqa


class SEOTestingModule(ModuleBase):
    """SEO Testing Module: Headless Module"""

    def __init__(self, config=None):

        super(SEOTestingModule, self).__init__()

        self.modulename = "headless"
        self.config = config or Config(module=self.modulename)
        self.exclusions = config.headless.ignore

        # item: item name.
        # loc: dot dictionary location of exclusions dict, and page_data dict
        self.mappings = [
            {"item": "canonical", "loc": "content.canonical"},
            {"item": "robots", "loc": "content.robots"},
            {"item": "title", "loc": "content.title"},
            {"item": "meta_description", "loc": "content.meta_description"},
            {"item": "h1", "loc": "content.h1"},
            {"item": "h2", "loc": "content.h2"},
            {"item": "links", "loc": "content.links"},
            {"item": "images", "loc": "content.images"},
            {"item": "schema", "loc": "content.schema"},
            {"item": "performance", "loc": "performance"},
            {"item": "coverage-summary", "loc": "coverage.summary"},
            {"item": "coverage-css", "loc": "coverage.css"},
            {"item": "coverage-js", "loc": "coverage.js"},
        ]

    def run(self, sample_paths):

        self.sample_paths = sample_paths

        page_data = run_render(sample_paths, self.config)

        diffs = self.run_diffs(page_data)

        self.messages = self.prepare_messages(diffs)

        self.passing = len(self.messages) == 0

        return self.errors
#!/usr/bin/env python3

## Author(s): Kenzo-Hugo Hillion
## Contact(s): kehillio@pasteur.fr
## Python version: 3.6.0
## Creation : 01-02-2017

'''
Unit tests for pycwl library
'''

###########  Import  ###########

# General libraries
import os
import filecmp
import unittest

# External libraries
import pycwl

# Class and Objects

###########  Constant(s)  ###########

###########  Function(s)  ###########

###########  Class(es)  ###########

class TestCommandLineTool(unittest.TestCase):

    def setUp(self):
        self.cwl = pycwl.CommandLineTool(tool_id='an_id', label='a description '+\
                                         'with spaces.', base_command='a_command')

    def test_init(self):
        self.assertEqual(self.cwl.tool_id, 'an_id')
        self.assertEqual(self.cwl.label, 'a description with spaces.')
        self.assertEqual(self.cwl.base_command, 'a_command')
        self.assertListEqual(self.cwl.inputs, [])
        self.assertListEqual(self.cwl.outputs, [])
        self.assertIsNone(self.cwl.doc)

    '''
    def test_export(self):
        tmp_file = 'test_export.tmp'
        expected_file = os.path.dirname(__file__) + '/test_export.cwl'
        self.cwl.export(tmp_file)
        try:
            self.assertTrue(filecmp.cmp(expected_file, tmp_file))
        finally:
            os.remove(tmp_file)

    def test_full_export(self):
        tmp_file = 'test_full_export.tmp'
        expected_file = os.path.dirname(__file__) + '/test_full_export.cwl'
        self.cwl.doc = "documentation"
        an_input = pycwl.CommandInputParameter('an_in_id', param_type='File')
        self.cwl.inputs.append(an_input)
        an_output = pycwl.CommandOutputParameter('an_out_id', param_type='File')
        self.cwl.outputs.append(an_output)
        self.cwl.export(tmp_file)
        try:
            self.assertTrue(filecmp.cmp(expected_file, tmp_file))
        finally:
            os.remove(tmp_file)
    '''

class TestParameter(unittest.TestCase):

    def setUp(self):
        self.param = pycwl.Parameter('an_id', param_type='File', label='a_label',\
                                     doc='a_doc', param_format='a_format',\
                                     streamable=True, secondary_files='sec_files')

    def test_init(self):
        self.assertEqual(self.param.id, 'an_id')
        self.assertEqual(self.param.type, 'File')
        self.assertEqual(self.param.doc, 'a_doc')
        self.assertEqual(self.param.format, 'a_format')
        self.assertEqual(self.param.label, 'a_label')
        self.assertEqual(self.param.secondary_files, 'sec_files')
        self.assertTrue(self.param.streamable)

    def test_get_dict(self):
        dict_test = self.param.get_dict()
        self.assertEqual(dict_test['type'], 'File')
        self.assertEqual(dict_test['doc'], 'a_doc')
        self.assertEqual(dict_test['format'], 'a_format')
        self.assertEqual(dict_test['label'], 'a_label')
        self.assertEqual(dict_test['secondaryFiles'], 'sec_files')
        self.assertTrue(dict_test['streamable'])


class TestCommandInputParameter(unittest.TestCase):

    def setUp(self):
        self.frst_inp = pycwl.CommandInputParameter('frst_id', param_type='File',\
                                                    label='a_label', \
                                                    default='def_value')
        binding = pycwl.CommandLineBinding(position=2, prefix='--prefix')
        self.scnd_inp = pycwl.CommandInputParameter('scnd_id', param_type='File',\
                                                    input_binding=binding)

    def test_init(self):
        # Test first input
        self.assertEqual(self.frst_inp.id, 'frst_id')
        self.assertEqual(self.frst_inp.type, 'File')
        self.assertEqual(self.frst_inp.label, 'a_label')
        self.assertEqual(self.frst_inp.default, 'def_value')
        # Test second input
        self.assertEqual(self.scnd_inp.id, 'scnd_id')
        self.assertEqual(self.scnd_inp.type, 'File')
        self.assertEqual(self.scnd_inp.input_binding.position, 2)
        self.assertEqual(self.scnd_inp.input_binding.prefix, '--prefix')

    def test_get_dict(self):
        # Test first input
        dict_frst = self.frst_inp.get_dict()
        self.assertEqual(dict_frst['type'], 'File')
        self.assertEqual(dict_frst['default'], 'def_value')
        self.assertEqual(dict_frst['label'], 'a_label')
        # Test second input
        dict_scnd = self.scnd_inp.get_dict()
        self.assertEqual(dict_scnd['type'], 'File')
        self.assertEqual(dict_scnd['inputBinding']['prefix'], '--prefix')
        self.assertEqual(dict_scnd['inputBinding']['position'], 2)


class TestCommandOutputParameter(unittest.TestCase):

    def setUp(self):
        self.outp = pycwl.CommandOutputParameter('an_out_id', param_type='File')

    def test_init(self):
        self.assertEqual(self.outp.id, 'an_out_id')
        self.assertEqual(self.outp.type, 'File')

    def test_get_dict(self):
        dict_test = self.outp.get_dict()
        self.assertEqual(dict_test['type'], 'File')


class TestCommandLineBinding(unittest.TestCase):

    def setUp(self):
        self.line_binding = pycwl.CommandLineBinding(load_contents=True, position=1, \
                                                     prefix='--prefix', separate=True, \
                                                     item_separator='-', shell_quote=True,\
                                                     value_from='text.txt')

    def test_init(self):
        self.assertTrue(self.line_binding.load_contents)
        self.assertEqual(self.line_binding.position, 1)
        self.assertEqual(self.line_binding.prefix, '--prefix')
        self.assertTrue(self.line_binding.separate)
        self.assertEqual(self.line_binding.item_separator, '-')
        self.assertTrue(self.line_binding.shell_quote)
        self.assertEqual(self.line_binding.value_from, 'text.txt')

    def test_get_dict(self):
        dict_test = self.line_binding.get_dict()
        self.assertEqual(dict_test['position'], 1)
        self.assertEqual(dict_test['prefix'], '--prefix')
        self.assertTrue(dict_test['separate'])
        self.assertEqual(dict_test['itemSeparator'], '-')
        self.assertTrue(dict_test['shellQuote'])
        self.assertEqual(dict_test['valueFrom'], 'text.txt')


class TestCommandOutputBinding(unittest.TestCase):

    def setUp(self):
        self.out_binding = pycwl.CommandOutputBinding(glob='file.txt', load_contents=True,\
                                                      output_eval='eval')

    def test_init(self):
        self.assertEqual(self.out_binding.glob, 'file.txt')
        self.assertTrue(self.out_binding.load_contents)
        self.assertEqual(self.out_binding.output_eval, 'eval')

    def test_get_dict(self):
        dict_test = self.out_binding.get_dict()
        self.assertEqual(dict_test['glob'], 'file.txt')
        self.assertTrue(dict_test['loadContents'])
        self.assertEqual(dict_test['outputEval'], 'eval')


class TestRequirement(unittest.TestCase):

    def setUp(self):
        self.requirement = pycwl.Requirement('a_class')

    def test_init(self):
        self.assertEqual(self.requirement.req_class, 'a_class')


class TestInlineJavascriptReq(unittest.TestCase):

    def setUp(self):
        self.js_req = pycwl.InlineJavascriptReq(expression_lib='expression')

    def test_init(self):
        self.assertEqual(self.js_req.req_class, 'InlineJavascriptRequirement')
        self.assertEqual(self.js_req.expression_lib, 'expression')

class TestDockerRequirement(unittest.TestCase):

    def setUp(self):
        self.dock_req = pycwl.DockerRequirement(docker_pull='pull', docker_load='load',\
                                                docker_file='file', docker_import='import',\
                                                docker_image_id='id', docker_output_dir='dir')

    def test_init(self):
        self.assertEqual(self.dock_req.docker_pull, 'pull')
        self.assertEqual(self.dock_req.docker_load, 'load')
        self.assertEqual(self.dock_req.docker_file, 'file')
        self.assertEqual(self.dock_req.docker_import, 'import')
        self.assertEqual(self.dock_req.docker_image_id, 'id')
        self.assertEqual(self.dock_req.docker_output_dir, 'dir')


###########  Main  ###########

if __name__ == "__main__":
    unittest.main()

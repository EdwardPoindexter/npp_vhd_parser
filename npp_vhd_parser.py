#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os


class Generic:
    def __init__(self, raw_str):
        self.raw_str = raw_str
        self.name = str()
        self.type = str()
        self.value = str()
        self.comment = str()
        self.comment_only = False

        if raw_str:
            self.parse(raw_str)

    def parse(self, raw_str):
        reg_exp = r"""(?P<name>\w+)    \s*     # the generic name
                  :                    \s*     # a separator
                 (?P<type>.*)          \s*     # the type of generic
                 (                           # optional value of generic
                 \:\=                  \s*     # operator :=
                 (?P<value>[\d\w"]+))? \s*      # the value ( digit or word or ") multiple times
                 \;?
        """
        my_reg_exp = re.compile(reg_exp, re.VERBOSE)

        # check if the line contains comments
        comment_pos = raw_str.find("--")
        if comment_pos == 0:
            # there is line containing only comments
            self.comment = self.raw_str
            self.comment_only = True
            return
        elif comment_pos != -1:
            # there is a comment
            self.comment = raw_str[comment_pos:].strip()
            self.raw_str = raw_str[:comment_pos]

        if len(self.raw_str):
            result = my_reg_exp.match(self.raw_str)
            if result:
                self.name = result.group("name").strip()
                self.type = result.group("type").strip()
                self.value = result.group("value")
                if self.value:
                    self.value = self.value.srip()
                if self.type.endswith(';'):
                    self.type = self.type[:-1].strip()

            else:
                Exception("error can't parse generic: {}\n".format(self.raw_str))

    def __str__(self):
        return self.paste_as_entity(separator=True)

    def get_name(self, prefix=''):
        return self.name

    def paste_as_entity(self, separator, name_len=30):
        if separator:
            separator_str = ';'
        else:
            separator_str = ' '

        if len(self.raw_str) == 0:
            return ""
        elif self.comment_only:
            return "{}".format(self.comment)
        else:
            if self.value:
                # append the separator after the value
                value_and_sep = self.value + separator_str
                res = "{name:{name_len}s} : {type:3s} := {value:30s}{comment}".format(
                    name=self.name, type=self.type, value=value_and_sep, comment=self.comment, name_len=name_len)
            else:
                res = "{name:{name_len}s} : {type:3s}{sep}{comment}".format(
                    name=self.name, type=self.type, sep=separator_str, comment=self.comment,
                    name_len=name_len)
            return res.strip()

    def paste_as_instance(self, separator, name_len=30, prefix=''):
        if separator:
            separator_str = ','
        else:
            separator_str = ' '

        if len(self.raw_str) == 0:
            return ""
        elif self.comment_only:
            return "{}".format(self.comment)
        else:
            # append the separator after the name
            name_and_sep = self.name + separator_str
            res ="{name:{name_len}s} => {name_and_sep:{name_len_sep}s} {comment}".format(
                name=self.name, name_and_sep=name_and_sep, comment=self.comment, name_len=name_len, name_len_sep=name_len + 1)
            return res.strip()

    def paste_as_component(self, separator, name_len=30):
        if separator:
            separator_str = ';'
        else:
            separator_str = ' '

        if len(self.raw_str) == 0:
            return ""
        elif self.comment_only:
            return "{}".format(self.comment)
        else:
            # append the separator after the value
            if self.value:
                value_and_sep = self.value + separator_str
                res = "{name:{name_len}s} : {type:3s} := {value:40s}{comment}".format(
                    name=self.name, type=self.type, value=value_and_sep, comment=self.comment, name_len=name_len)
            else:
                res = "{name:{name_len}s} : {type:3s}{sep} {comment}".format(
                    name=self.name, type=self.type, sep=separator_str, comment=self.comment,
                    name_len=name_len)
            return res.strip()

    def paste_as_signal(self, name_len=30, prefix='_i'):
        if len(self.raw_str) == 0:
            return ""
        elif self.comment_only:
            return "{}".format(self.comment)
        else:
            if self.value:
                # append the separator after the value
                value_and_sep = self.value + ';'
                res = "constant {name:{name_len}s} : {type:s} := {value:40s}{comment}".format(
                    name=self.name, type=self.type, value=value_and_sep, comment=self.comment, name_len=name_len)
            else:
                res = "constant {name:{name_len}s} : {type:s};{comment}".format(
                    name=self.name, type=self.type, comment=self.comment, name_len=name_len)
            return res.strip()


class Port:
    def __init__(self, raw_str):
        self.raw_str = raw_str.strip()
        self.name = str()
        self.mode = str()
        self.type = str()
        self.comment = str()
        self.comment_only = False
        self.indent = 4

        if len(raw_str):
            self.parse(raw_str)

    def get_indent(self, level):
        return self.indent * level * " "

    def parse(self, raw_str):
        # TODO: add support of initial value (it's optional)
        reg_exp = r"""(?P<name>\w+)                           \s+     # the port name
                  \:                                          \s*     # a separator
                  (?P<mode>\w+)                               \s+     # the mode
                  (?P<type>.*)                                \s*     # the type
                  \;?
        """

        # regexp KO (?P<mode>in|out|inout|buffer|linkage)       \s+     # the mode

        my_reg_exp = re.compile(reg_exp, re.VERBOSE)

        # check if the line contains comments
        comment_pos = raw_str.find("--")
        if comment_pos == 0:
            # there is line containing only comments
            self.comment = self.raw_str
            self.comment_only = True
            return
        elif comment_pos != -1:
            # there is a comment
            self.comment = raw_str[comment_pos:].strip()
            self.raw_str = raw_str[:comment_pos]

        if len(self.raw_str):
            result = my_reg_exp.match(self.raw_str)
            if result:
                self.name = result.group("name").strip()
                self.mode = result.group("mode").strip()
                self.type = result.group("type").strip()
                if self.type.endswith(';'):
                    self.type = self.type[:-1]
            else:
                Exception("error can't parse port: {}\n".format(self.raw_str))

    def __str__(self):
        if len(self.raw_str) == 0:
            return ""
        elif self.comment_only:
            return "{}".format(self.comment.strip())
        else:
            return "{:20s} : {:3s} {:40s} {}".format(self.name, self.mode, self.type, self.comment.strip())

    def get_name(self, prefix=''):
        return "{}{}".format(self.name, prefix)

    def paste_as_entity(self, separator, name_len=30):
        if separator:
            separator_str = ';'
        else:
            separator_str = ' '
        if len(self.raw_str) == 0:
            return ""
        elif self.comment_only:
            return "{}".format(self.comment)
        else:
            # append the separator after the value
            type_and_sep = self.type + separator_str
            res = "{name:{name_len}s} : {mode:3s} {type:40s}{comment}".format(
                name=self.name, mode=self.mode, type=type_and_sep, comment=self.comment, name_len=name_len)
            return res.strip()

    def paste_as_instance(self, separator, name_len=30, prefix=''):
        if separator:
            separator_str = ','
        else:
            separator_str = ' '
        if len(self.raw_str) == 0:
            return ""
        elif self.comment_only:
            return "{}".format(self.comment)
        else:
            # append the separator after the name
            name_and_sep = "{}{}{}".format(self.name, prefix, separator_str)
            res = "{name:{len}s} => {name_and_sep:{lenp1}s}{comment}".format(
                name=self.name, name_and_sep=name_and_sep, comment=self.comment, len=name_len, lenp1=name_len + 1)
            return res.strip()

    def paste_as_component(self, separator, name_len=30):
        if separator:
            separator_str = ';'
        else:
            separator_str = ' '
        if len(self.raw_str) == 0:
            return ""
        elif self.comment_only:
            return "{}".format(self.comment)
        else:
            # append the separator after the value
            type_and_sep = self.type + separator_str
            res = "{name:{name_len}s} : {mode:3s} {type:60s}{comment}".format(
                name=self.name, mode=self.mode, type=type_and_sep, comment=self.comment, name_len=name_len)
            return res.strip()

    def paste_as_signal(self, name_len=30, prefix=''):
        if len(self.raw_str) == 0:
            return ""
        elif self.comment_only:
            return "{}".format(self.comment)
        else:
            # append the separator after the value
            type_and_sep = self.type + ';'
            name = "{}{}".format(self.name, prefix)
            res = "signal {name:{name_len}s} : {type:60s}{comment}".format(
                name=name, type=type_and_sep, comment=self.comment, name_len=name_len)
            return res.strip()

    def paste_as_initialization(self, name_len=30):
        if len(self.raw_str) == 0:
            return ""
        elif self.comment_only:
            return ""
        else:
            if self.mode == "in":
                # don't init input ports
                return ""
            # init output ports only
            if self.type == 'std_logic':
                val = "'0'"
            elif 'std_logic_vector' in self.type:
                val = "(others => '0')"
            else:
                val = '0'

            res = "{name:{name_len}s} <= {val};{eol}".format(
                name=self.name, name_len=name_len, val=val, eol=os.linesep)
            return res

    def paste_as_tb_drivers(self, name_len=30):
        if len(self.raw_str) == 0:
            return ""
        elif self.comment_only:
            return ""
        else:
            if self.mode == "out":
                # don't drive outputs ports on the TestBench
                return ""
            # init output ports only
            if self.type == 'std_logic':
                val = "'0'"
            elif 'std_logic_vector' in self.type:
                val = "(others => '0')"
            else:
                val = '0'

            res = "{name:{name_len}s} <= {val};".format(name=self.name, name_len=name_len, val=val)
            return res

    def paste_as_tb_clock(self, name_len=30):
        res = list()
        res.append("{indent}p_{name:s}: process".format(indent=self.get_indent(0), name=self.name))
        res.append("{indent}begin".format(indent=self.get_indent(0)))
        res.append("{indent}{name} <= '1';".format(indent=self.get_indent(1),name=self.name))
        res.append("{indent}wait for 5ns;".format(indent=self.get_indent(1)))
        res.append("{indent}{name} <= '0';".format(indent=self.get_indent(1), name=self.name))
        res.append("{indent}wait for 5ns;".format(indent=self.get_indent(1)))
        res.append("{indent}end process p_{name:s};".format(indent=self.get_indent(0), name=self.name))

        return os.linesep.join(res)

    def paste_as_tb_reset(self, name_len=30):
        res = "{name:s} <= '0', '1' after 50 ns;".format(name=self.name)
        return res

    def paste_as_fake_par(self, name_len=30, prefix=''):
        if len(self.raw_str) == 0:
            return ""
        elif self.comment_only:
            return "{}".format(self.comment)
        else:
            if self.mode == "out":
                res = "{name:{name_len}s} <= {name}{prefix};".format(
                    name=self.name, name_len=(name_len + len(prefix)), prefix=prefix)
            else:
                name_and_prefix = self.name + prefix
                res = "{name_and_prefix:{name_len}s} <= {name};".format(
                    name_and_prefix=name_and_prefix, name=self.name, name_len=(name_len+len(prefix)), prefix=prefix)

            return res

    def is_clk(self):
        if ("clk" in self.name):
            return True
        
    def is_reset(self):
        if ("rst" in self.name or "reset" in self.name):
            return True


class Elements:
    '''
    elements can describe a list of ports or a list of generics
    '''
    def __init__(self):
        self.elements = list()
        self.indent = 4

    def get_indent(self, level):
        return self.indent * level * " "

    def get_nbr_elt(self):
        res = 0
        for elt in self.elements:
            if not elt.comment_only:
                res += 1
        return res

    def find_name_length(self, prefix=''):
        max_length = 0
        for elt in self.elements:
            name = elt.get_name()
            name_length = len(name)
            max_length = max(max_length, name_length)
        return max_length

    def paste_as_signal(self, prefix=''):
        name_len = self.find_name_length()
        res = list()
        if len(self.elements):
            for index, element in enumerate(self.elements):
                paste_res = element.paste_as_signal(name_len, prefix)
                res.append("{}{}".format(self.get_indent(0), paste_res))
        return os.linesep.join(res)


class Generics(Elements):

    def append(self, elt):
        self.elements.append(elt)

    def paste_as_component(self):
        res = list()
        name_len = self.find_name_length()
        res.append("{indent}generic(".format(indent=self.get_indent(1)))
        for index, elt in enumerate(self.elements):
            separator = not index == len(self.elements) - 1  # always append a separator but not on the last element
            paste_res = elt.paste_as_component(separator, name_len)
            res.append("{}{}".format(self.get_indent(2), paste_res))
        res.append("{});".format(self.get_indent(1)))
        return os.linesep.join(res)

    def paste_as_entity(self):
        res = list()
        name_len = self.find_name_length()
        res.append("{indent}generic(".format(indent=self.get_indent(1)))
        for index, elt in enumerate(self.elements):
            separator = not index == len(self.elements) - 1  # always append a separator but not on the last element
            paste_res = elt.paste_as_entity(separator, name_len)
            res.append("{}{}".format(self.get_indent(2), paste_res))
        res.append("{});".format(self.get_indent(1)))
        return os.linesep.join(res)

    def paste_as_instance(self, prefix=''):
        res = list()
        name_len = self.find_name_length()
        if len(self.elements):
            res.append("{indent}generic map(".format(indent=self.get_indent(1)))
            for index, elt in enumerate(self.elements):
                separator = not index == len(self.elements) - 1  # always append a separator but not on the last element
                paste_res = elt.paste_as_instance(separator, name_len)
                res.append("{}{}".format(self.get_indent(2), paste_res))
            res.append("{})".format(self.get_indent(1)))
        return os.linesep.join(res)

    def paste_as_instance_fake_par(self):
        return self.paste_as_instance()


class Ports(Elements):

    def append(self, elt):
        self.elements.append(elt)

    def get_elements_but_clk_rst(self):
        for elt in self.elements:
            if not elt.is_clk() and not elt.is_reset():
                yield elt

    def get_elements_clk(self):
        for elt in self.elements:
            if elt.is_clk():
                yield elt

    def get_clk_name(self):
        res = str()
        # return the name of the last clock of the module
        for elt in self.get_elements_clk():
            res = elt.get_name()
        return res

    def get_elements_reset(self):
        for elt in self.elements:
            if elt.is_reset():
                yield elt

    def paste_as_component(self):
        res = list()
        name_len = self.find_name_length()
        res.append("{indent}port(".format(indent=self.get_indent(1)))
        for index, elt in enumerate(self.elements):
            separator = not index == len(self.elements) - 1  # always append a separator but not on the last element
            paste_res = elt.paste_as_component(separator, name_len)
            res.append("{}{}".format(self.get_indent(2), paste_res))
        res.append("{});".format(self.get_indent(1)))
        return os.linesep.join(res)

    def paste_as_entity(self):
        res = list()
        name_len = self.find_name_length()
        res.append("{indent}port(".format(indent=self.get_indent(1)))
        for index, elt in enumerate(self.elements):
            separator = not index == len(self.elements) - 1  # always append a separator but not on the last element
            paste_res = elt.paste_as_entity(separator, name_len)
            res.append("{}{}".format(self.get_indent(2), paste_res))
        res.append("{});".format(self.get_indent(1)))
        return os.linesep.join(res)

    def paste_as_instance(self, prefix=''):
        res = list()
        name_len = self.find_name_length()
        if len(self.elements):
            res.append("{indent}port map(".format(indent=self.get_indent(1)))
            for index, elt in enumerate(self.elements):
                separator = not index == len(self.elements) - 1  # always append a separator but not on the last element
                paste_res = elt.paste_as_instance(separator, name_len)
                res.append("{}{}".format(self.get_indent(2), paste_res))
            res.append("{});".format(self.get_indent(1)))
        return os.linesep.join(res)

    def paste_as_instance_fake_par(self):
        res = list()
        name_len = self.find_name_length()
        if len(self.elements):
            res.append("{indent}port map(".format(indent=self.get_indent(1)))
            for index, elt in enumerate(self.elements):
                separator = not index == len(self.elements) - 1  # always append a separator but not on the last element
                if elt.is_clk() or elt.is_reset():
                    # don't use the prefix for signal clock or reset
                    paste_res = elt.paste_as_instance(separator, name_len, '')
                else:
                    paste_res = elt.paste_as_instance(separator, name_len, '_i')
                res.append("{}{}".format(self.get_indent(2), paste_res))
            res.append("{});".format(self.get_indent(1)))
        return os.linesep.join(res)

    def paste_as_initialization(self):
        res = list()
        name_len = self.find_name_length()
        for port in self.elements:
            res.append(port.paste_as_initialization())
        return os.linesep.join(res)

    def paste_as_signal_fake_par(self):
        name_len = self.find_name_length() + len("_i")
        res = list()
        if len(self.elements):
            for index, port in enumerate(self.elements):
                if not port.is_clk() and not port.is_reset():
                    paste_res = port.paste_as_signal(name_len, '_i')
                    res.append("{}{}".format(self.get_indent(0), paste_res))
        return os.linesep.join(res)

    def paste_as_initialization_fake_par(self):
        res = list()
        name_len = self.find_name_length() + len("_i")
        for port in self.elements:
            if not port.is_clk() and not port.is_reset():
                res.append("{}{}".format(self.get_indent(2), port.paste_as_fake_par(name_len, '_i')))
        return os.linesep.join(res)

    def paste_as_tb_clock_drivers(self, indent):
        self.indent = indent
        name_len = self.find_name_length()
        res = list()
        for port in self.get_elements_clk():
            elt = port.paste_as_tb_clock(name_len)
            if len(elt.strip()):
                res.append(elt)
        return os.linesep.join(res)

    def paste_as_tb_reset_driver(self, indent):
        self.indent = indent
        name_len = self.find_name_length()
        res = list()
        for port in self.get_elements_reset():
            elt = port.paste_as_tb_reset(name_len)
            if len(elt.strip()):
                res.append(elt)
        return os.linesep.join(res)

    def paste_as_tb_signal_driver(self, indent):
        self.indent = indent
        name_len = self.find_name_length()
        res = list()
        for port in self.get_elements_but_clk_rst():
            elt = port.paste_as_tb_drivers(name_len)
            if len(elt.strip()):
                res.append(elt)
        return os.linesep.join(res)
    
    def paste_as_tb_driver(self, indent):
        res = list()
        res.append(self.paste_as_tb_clock_drivers(indent))
        res.append(os.linesep)
        res.append(self.paste_as_tb_reset_driver(indent))
        res.append(os.linesep)
        res.append(self.paste_as_tb_signal_driver(indent))
        return os.linesep.join(res)



class VhdParser:
    def __init__(self, input_text=None):

        self.input_text = str()
        self.entity_name = str()
        
        self.generics_str = str()
        self.generics_parsed = Generics()

        self.ports_str = str()
        self.ports_parsed = Ports()

        self.indent = str()

        if input_text:
            self.parse(input_text)

    def parse(self, input_text):
        '''

        :param input_text:
        :return:

        parse an entity and build Generic and Port object list.
        The Generics declaration part is optional
        The Ports declaration part is mandatory

        '''
        self.input_text = input_text.strip()

        self.entity_name = str()
        self.generics_str = str()
        self.ports_str = str()
        self.ports_parsed = Ports()

        # find entity name
        reg_exp_glob = r""".*entity       \s+     # start of the entity
                   (?P<entity_name>\w+) \s+     # name of the entity
                   is                   \s*     #
                   (?P<body>.*)                 # body of the entity
                   end                  \s+     # end of the entity
                   (?P=entity_name)     \s*     # repeat the name of the entity
                   ;                            # end of the entity
                   """
        my_reg_exp = re.compile(reg_exp_glob, re.DOTALL | re.VERBOSE)
        result = my_reg_exp.match(self.input_text)

        if not result:
            Exception("entity not recognized")

        self.entity_name = result.group('entity_name')
        entity_body = result.group('body')

        reg_exp = r"""
        (                                  # start an optional group to match a generic declaration
        generic                     \s*    # start of generic (it's optional)
        \(                          \s+    #
        (?P<generic_body>.*)        \s+    #
        \);                         \s+    # end of generic
        )?                                 # end of optional Generic group
        port\s*\(                   \s+    # start of port
        (?P<port_body>.*)           \s+    #
        \);                                # end of port
        """
        my_reg_exp = re.compile(reg_exp, re.DOTALL | re.VERBOSE)
        parsing_result = my_reg_exp.match(entity_body)
        if parsing_result:
            self.generics_str = parsing_result.group("generic_body")
            self.ports_str = parsing_result.group("port_body")

            if self.generics_str:
                for elt in self.generics_str.splitlines():
                    str_to_parse = elt.strip()
                    if len(str_to_parse):
                        generic_parsed = Generic(str_to_parse)
                        self.generics_parsed.append(generic_parsed)

            if self.ports_str:
                for elt in self.ports_str.splitlines():
                    str_to_parse = elt.strip()
                    if len(str_to_parse):
                        port_parsed = Port(str_to_parse)
                        self.ports_parsed.append(port_parsed)
        else:
            Exception("can't parse the body of the entity")

    def __repr__(self):
        res = str()
        res += "entity:       {}\n".format(self.entity_name)
        res += "nb generics : {}\n".format(self.generics_parsed.get_nbr_elt())
        res += "nb ports :    {}\n".format(self.ports_parsed.get_nbr_elt())
        return res

    def get_indent(self, level):
        return self.indent * level * " "

    def paste_as_entity(self, indent=4):
        self.indent = indent
        res = list()
        res.append("{indent}entity {name} is".format(indent=self.get_indent(0), name=self.entity_name))
        res.append(self.generics_parsed.paste_as_entity())
        res.append(self.ports_parsed.paste_as_entity())
        res.append("{}end {};".format(self.get_indent(0), self.entity_name))
        return os.linesep.join(res)

    def paste_as_component(self, indent=4):
        self.indent = indent
        res = list()
        res.append("{indent}component {name} is".format(indent=self.get_indent(0), name=self.entity_name))
        res.append(self.generics_parsed.paste_as_component())
        res.append(self.ports_parsed.paste_as_component())
        res.append("{}end component {};".format(self.get_indent(0), self.entity_name))
        return os.linesep.join(res)

    def paste_as_instance(self, indent=4, prefix=''):
        self.indent = indent
        res = list()
        res.append("{indent}{name}_inst : {name}".format(indent=self.get_indent(0), name=self.entity_name))
        res.append(self.generics_parsed.paste_as_instance())
        res.append(self.ports_parsed.paste_as_instance())
        return os.linesep.join(res)

    def paste_as_signal(self, indent=4, prefix=''):
        self.indent = indent
        res = list()
        res.append(self.generics_parsed.paste_as_signal())
        res.append(self.ports_parsed.paste_as_signal())
        return os.linesep.join(res)

    def paste_as_initializations(self, indent=4):
        self.indent = indent
        res = self.ports_parsed.paste_as_initialization()
        return res

    def paste_as_testbench(self, indent=4):
        self.indent = indent
        res = list()
        # entity
        res.append("entity {name}_tb is".format(name=self.entity_name))
        res.append("end entity {name}_tb;".format(name=self.entity_name))
        res.append(os.linesep)

        # architecture
        res.append("architecture tb of {name}_tb is".format(name=self.entity_name))

        res.append(self.paste_as_component(indent=indent))
        res.append(os.linesep)

        res.append(self.paste_as_signal(indent=indent))
        res.append(os.linesep)

        res.append("begin")
        res.append(os.linesep)

        res.append(self.paste_as_instance(indent=indent))
        res.append(os.linesep)

        res.append(self.ports_parsed.paste_as_tb_driver(indent=indent))
        res.append(os.linesep)

        res.append("end tb;")
        res.append(os.linesep)

        return os.linesep.join(res)

    def paste_as_fake_par_instance(self, indent=4, prefix=''):
        self.indent = indent
        res = list()
        res.append("{indent}{name}_inst : {name}".format(indent=self.get_indent(0), name=self.entity_name))
        res.append(self.generics_parsed.paste_as_instance())
        res.append(self.ports_parsed.paste_as_instance_fake_par())
        return os.linesep.join(res)

    def paste_as_fake_par(self, indent=4):
        res = list()
        self.entity_name += "_par"
        res.append(self.paste_as_entity(indent=indent))
        # architecture
        res.append("architecture rtl of {name} is".format(name=self.entity_name))
        self.entity_name = self.entity_name[:-4]

        res.append(self.paste_as_component(indent=indent))
        res.append(os.linesep)

        res.append(self.ports_parsed.paste_as_signal_fake_par())
        res.append(os.linesep)

        res.append("begin")
        res.append(os.linesep)

        res.append(self.paste_as_fake_par_instance(indent=indent, prefix='_i'))
        res.append(os.linesep)

        clock_name = self.ports_parsed.get_clk_name()
        res.append("{indent}process({clk})".format(indent=self.get_indent(0), clk=clock_name))
        res.append("{indent}begin".format(indent=self.get_indent(0)))
        res.append("{indent}if (rising_edge({clk})) then".format(indent=self.get_indent(1), clk=clock_name))
        res.append(self.ports_parsed.paste_as_initialization_fake_par())

        res.append("{indent}end if;".format(indent=self.get_indent(1)))
        res.append("{indent}end process;".format(indent=self.get_indent(0)))

        res.append(os.linesep)

        res.append("end rtl;")

        return os.linesep.join(res)


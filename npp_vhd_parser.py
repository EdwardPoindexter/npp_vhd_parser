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


class Ports:
    def __init__(self, raw_str):
        self.raw_str = raw_str.strip()
        self.name = str()
        self.mode = str()
        self.type = str()
        self.comment = str()
        self.comment_only = False

        if len(raw_str):
            self.parse(raw_str)

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
                name=self.name, mode=self.mode, type=type_and_sep, sep=separator_str, comment=self.comment, name_len=name_len)
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

            res = "{name:{name_len}s} <= {val};{eol}".format(
                name=self.name, name_len=name_len, val=val, eol=os.linesep)
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


class VhdParser:
    def __init__(self, input_text=None):

        self.input_text = str()
        self.generics_str = str()
        self.generics = list()
        self.ports_str = str()
        self.ports = list()
        self.indent = str()
        self.entity_name = str()
        self.generics_str = str()
        self.generics = list()
        self.ports_str = str()
        self.ports = list()

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
        self.generics = list()
        self.ports_str = str()
        self.ports = list()

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
                        self.generics.append(Generic(str_to_parse))

            if self.ports_str:
                for elt in self.ports_str.splitlines():
                    str_to_parse = elt.strip()
                    if len(str_to_parse):
                        self.ports.append(Ports(str_to_parse))
        else:
            Exception("can't parse the body of the entity")

    def __repr__(self):
        res = str()
        res += "entity:       {}\n".format(self.entity_name)
        res += "nb generics : {}\n".format(len(self.generics))
        res += "nb ports :    {}\n".format(len(self.ports))
        return res

    def get_indent(self, level):
        return self.indent * level * " "

    def find_name_length(self, my_object, prefix=''):
        max_length = 0
        for elt in my_object:
            name_length = len(elt.get_name(prefix))
            if name_length > max_length:
                max_length = name_length
        return max_length

    def paste_obj_list_as_entity(self, my_object):
        res = str()
        name_len = self.find_name_length(my_object)
        if len(my_object):
            if isinstance(my_object[0], Ports):
                keyword = "port"
            elif isinstance(my_object[0], Generic):
                keyword = "generic"
            else:
                keyword = "???"
            res += "{indent}{keyword}({eol}".format(indent=self.get_indent(1), keyword=keyword, eol=os.linesep)
            for index, port_or_generic in enumerate(my_object):
                separator = not index == len(my_object) - 1
                paste_res = port_or_generic.paste_as_entity(separator, name_len)
                res += "{}{}{}".format(self.get_indent(2), paste_res, os.linesep)
            res += "{});{}".format(self.get_indent(1), os.linesep)
        return res

    def paste_obj_list_as_instance(self, my_object, prefix):
        res = str()
        name_len = self.find_name_length(my_object)

        if len(my_object):
            if isinstance(my_object[0], Ports):
                keyword = "port map"
            elif isinstance(my_object[0], Generic):
                keyword = "generic map"
            else:
                keyword = "???"
            res += "{indent}{keyword}({eol}".format(indent=self.get_indent(0), keyword=keyword, eol=os.linesep)
            for index, port_or_generic in enumerate(my_object):
                separator = not index == len(my_object) - 1  # always append a separator but not on the last element
                paste_res = port_or_generic.paste_as_instance(separator, name_len, prefix)
                res += "{}{}{}".format(self.get_indent(1), paste_res, os.linesep)
            if isinstance(my_object[0], Ports):
                res += "{});{}".format(self.get_indent(0), os.linesep)
            elif isinstance(my_object[0], Generic):
                res += "{}){}".format(self.get_indent(0), os.linesep)

        return res

    def paste_obj_list_as_signal(self, my_object, prefix=''):
        res = str()
        name_len = self.find_name_length(my_object)
        if len(my_object):
            for index, port_or_generic in enumerate(my_object):
                paste_res = port_or_generic.paste_as_signal(name_len, prefix)
                res += "{}{}{}".format(self.get_indent(0), paste_res, os.linesep)

        return res

    def paste_obj_list_as_component(self, my_object):
        res = str()
        name_len = self.find_name_length(my_object)
        if len(my_object):
            if isinstance(my_object[0], Ports):
                keyword = "port"
            elif isinstance(my_object[0], Generic):
                keyword = "generic"
            else:
                keyword = "???"
            res += "{indent}{keyword}({eol}".format(indent=self.get_indent(1), keyword=keyword, eol=os.linesep)
            for index, port_or_generic in enumerate(my_object):
                separator = not index == len(my_object) - 1  # always append a separator but not on the last element
                paste_res = port_or_generic.paste_as_component(separator, name_len)
                res += "{}{}{}".format(self.get_indent(2), paste_res, os.linesep)
            res += "{});{}".format(self.get_indent(1), os.linesep)
        return res

    def paste_as_entity(self, indent=4):
        self.indent = indent
        res = str()
        res += "{indent}entity {name} is{eol}".format(indent=self.get_indent(0), name=self.entity_name, eol=os.linesep)
        res += self.paste_obj_list_as_entity(self.generics)
        res += self.paste_obj_list_as_entity(self.ports)
        res += "{}end {};{}".format(self.get_indent(0), self.entity_name, os.linesep)
        return res

    def paste_as_component(self, indent=4):
        self.indent = indent
        res = str()
        res += "{indent}component {name} is{eol}".format(indent=self.get_indent(0), name=self.entity_name,
                                                         eol=os.linesep)
        res += self.paste_obj_list_as_component(self.generics)
        res += self.paste_obj_list_as_component(self.ports)
        res += "{}end component {};{}".format(self.get_indent(0), self.entity_name, os.linesep)
        return res

    def paste_as_instance(self, indent=4, prefix=''):
        self.indent = indent
        res = str()
        res += "{indent}{name}_inst : {name}{eol}".format(indent=self.get_indent(0), name=self.entity_name, eol=os.linesep)
        res += self.paste_obj_list_as_instance(self.generics, prefix)
        res += self.paste_obj_list_as_instance(self.ports, prefix)
        return res

    def paste_as_signal(self, indent=4, prefix=''):
        self.indent = indent
        res = str()
        res += self.paste_obj_list_as_signal(self.generics, prefix)
        res += self.paste_obj_list_as_signal(self.ports, prefix)
        return res

    def paste_as_initializations(self, indent=4):
        self.indent = indent
        name_len = self.find_name_length(self.ports)
        res = str()
        for port in self.ports:
            res += port.paste_as_initialization(name_len)
        return res

    def paste_as_tb_drivers(self, indent=4):
        self.indent = indent
        name_len = self.find_name_length(self.ports)
        res = str()
        for port in self.ports:
            res += port.paste_as_tb_drivers(name_len)
        return res

    def paste_as_testbench(self, indent=4):
        self.indent = indent
        res = str()
        # entity
        res += "entity {name}_tb is{eol}".format(name=self.entity_name, eol=os.linesep)
        res += "end entity {name}_tb;{eol}".format(name=self.entity_name, eol=os.linesep)
        res += os.linesep

        # architecture
        res += "architecture tb of {name}_tb is{eol}".format(name=self.entity_name, eol=os.linesep)

        res += self.paste_as_component(indent=indent)
        res += os.linesep

        res += self.paste_as_signal(indent=indent)
        res += os.linesep

        res += "begin"
        res += os.linesep

        res += self.paste_as_instance(indent=indent)
        res += os.linesep

        res += self.paste_as_tb_drivers(indent=indent)
        res += os.linesep

        res += "end tb;{eol}".format(eol=os.linesep)

        return res

    def paste_as_fake_par(self, indent=4):
        res = str()
        self.entity_name += "_par"
        res += self.paste_as_entity(indent=indent)
        # architecture
        res += "architecture rtl of {name} is{eol}".format(name=self.entity_name, eol=os.linesep)
        self.entity_name = self.entity_name[:-4]

        res += self.paste_as_component(indent=indent)
        res += os.linesep

        res += self.paste_obj_list_as_signal(self.ports, prefix='_i')
        res += os.linesep

        res += "begin"
        res += os.linesep

        res += self.paste_as_instance(indent=indent, prefix='_i')
        res += os.linesep

        res += "{indent}process(clk){eol}".format(indent=self.get_indent(0), eol=os.linesep)
        res += "{indent}begin{eol}".format(indent=self.get_indent(0), eol=os.linesep)
        res += "{indent}if (rising_edge(clk)) then{eol}".format(indent=self.get_indent(1), eol=os.linesep)

        port_max_len = self.find_name_length(self.ports, prefix='_i')
        for port in self.ports:
            port_pasted = port.paste_as_fake_par(port_max_len, '_i')
            res += "{indent}{port_pasted}{eol}".format(indent=self.get_indent(2), port_pasted=port_pasted, eol=os.linesep)

        res += "{indent}end if;{eol}".format(indent=self.get_indent(1), eol=os.linesep)
        res += "{indent}end process;{eol}".format(indent=self.get_indent(0), eol=os.linesep)

        res += os.linesep

        res += "end rtl;{eol}".format(eol=os.linesep)

        return res


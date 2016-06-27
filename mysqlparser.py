# -*- coding: utf-8 -*-
import codecs

from pyparsing import Literal, White, Word, alphanums, CharsNotIn
from pyparsing import Forward, Group, Optional, OneOrMore, ZeroOrMore
from pyparsing import pythonStyleComment


class MySQLParser(object):

    # TODO: Fix the definition to work with !includedir
    key = Word(alphanums + "_-!")
    space = White().suppress()
    value = CharsNotIn("\n")
    comment = ("#")
    config_entry = (key + Optional(space)
                    + Optional(
                        Literal("=").suppress() + Optional(space)
                        + Optional(value) + Optional(space)
                        + Optional("#")
                    )
                    )
    single_value = key
    client_block = Forward()
    client_block << Group((Literal("[").suppress()
                          + key
                          + Literal("]").suppress())
                          + Group(ZeroOrMore(Group(config_entry)))
                          )
    
    client_file = OneOrMore(client_block).ignore(pythonStyleComment)
    
    file_header = """# File parsed and saved by privacyidea.\n\n"""
    
    def __init__(self, infile="/etc/mysql/my.cnf",
                 content=None):
        self.file = None
        if content:
            self.content = content
        else:
            self.file = infile
            self._read()

    def _read(self):
        """
        Reread the contents from the disk
        """
        f = codecs.open(self.file, "r", "utf-8")
        self.content = f.read()
        f.close()
        
    def get(self):
        """
        return the grouped config
        """
        if self.file:
            self._read()
        config = self.client_file.parseString(self.content)
        return config
    
    def format(self, dict_config):
        '''
        :return: The formatted data as it would be written to a file
        '''
        output = ""
        output += self.file_header
        for section, attributes in dict_config.items():
            output += "[{0}]\n".format(section)
            for k, v in attributes.iteritems():
                if v:
                    output += "{k} = {v}\n".format(k=k, v=v)
                else:
                    output += "{k}\n".format(k=k)
            output += "\n"

        return output

    def get_dict(self, section=None, key=None):
        '''
        return the client config as a dictionary.
        '''
        ret = {}
        config = self.get()
        for client in config:
            client_config = {}
            for attribute in client[1]:
                if len(attribute) > 1:
                    client_config[attribute[0]] = attribute[1]
                else:
                    client_config[attribute[0]] = None
            ret[client[0]] = client_config
        if section:
            ret = ret.get(section)
            if key:
                ret = ret.get(key)
        return ret

    def save(self, dict_config=None, outfile=None):
        if dict_config:
            output = self.format(dict_config)
            f = codecs.open(outfile, 'w', 'utf-8')
            for line in output.splitlines():
                f.write(line + "\n")
            f.close()

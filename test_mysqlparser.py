# -*- coding: utf-8 -*-
#
#    mysqlparser tests
# 
#    Copyright (C)  2016 Cornelius Kölbel, cornelius@privacyidea.org
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
log = logging.getLogger(__name__)
import unittest
import os
from mysqlparser import MySQLParser

MY_CNF = """#
# The MySQL database server configuration file.
#
# You can copy this to one of:
# - "/etc/mysql/my.cnf" to set global options,
# - "~/.my.cnf" to set user-specific options.
#
# One can use all long options that the program supports.
# Run program with --help to get a list of available options and with
# --print-defaults to see which it would actually understand and use.
#
# For explanations see
# http://dev.mysql.com/doc/mysql/en/server-system-variables.html

# This will be passed to all mysql clients
# It has been reported that passwords should be enclosed with ticks/quotes
# escpecially if they contain "#" chars...
# Remember to edit /etc/mysql/debian.cnf when changing the socket location.
[client]
port		= 3306
socket		= /var/run/mysqld/mysqld.sock
default-character-set=utf8

# Here is entries for some specific programs
# The following values assume you have at least 32M ram

# This was formally known as [safe_mysqld]. Both versions are currently parsed.
[mysqld_safe]
socket		= /var/run/mysqld/mysqld.sock
nice		= 0

[mysqld]
#
# * Basic Settings
#
wait_timeout = 700
user		= mysql
pid-file	= /var/run/mysqld/mysqld.pid
socket		= /var/run/mysqld/mysqld.sock
port		= 3306
basedir		= /usr
datadir		= /var/lib/mysql
tmpdir		= /tmp
lc-messages-dir	= /usr/share/mysql
skip-external-locking
init-connect='SET NAMES utf8'
character-set-server = utf8
#
# Instead of skip-networking the default is now to listen only on
# localhost which is more compatible and is not less secure.
bind-address		= 127.0.0.1
#
# * Fine Tuning
#
key_buffer		= 16M
max_allowed_packet	= 16M
thread_stack		= 192K
thread_cache_size       = 8
# This replaces the startup script and checks MyISAM tables if needed
# the first time they are touched
myisam-recover         = BACKUP
#max_connections        = 100
#table_cache            = 64
#thread_concurrency     = 10
#
# * Query Cache Configuration
#CKO: 1/16
query_cache_limit	= 0M
query_cache_size        = 0M
#
# * Logging and Replication
#
# Both location gets rotated by the cronjob.
# Be aware that this log type is a performance killer.
# As of 5.1 you can enable the log at runtime!
#general_log_file        = /var/log/mysql/mysql.log
#general_log             = 1
#
# Error log - should be very few entries.
#
log_error = /var/log/mysql/error.log
#
# Here you can see queries with especially long duration
#log_slow_queries	= /var/log/mysql/mysql-slow.log
#long_query_time = 2
#log-queries-not-using-indexes
#
# The following can be used as easy to replay backup logs or for replication.
# note: if you are setting up a replication slave, see README.Debian about
#       other settings you may need to change.
#server-id		= 1
#log_bin			= /var/log/mysql/mysql-bin.log
expire_logs_days	= 10
max_binlog_size         = 100M
#binlog_do_db		= include_database_name
#binlog_ignore_db	= include_database_name
#
# * InnoDB
#
# InnoDB is enabled by default with a 10MB datafile in /var/lib/mysql/.
# Read the manual for more InnoDB related options. There are many!
#
# * Security Features
#
# Read the manual, too, if you want chroot!
# chroot = /var/lib/mysql/
#
# For generating SSL certificates I recommend the OpenSSL GUI "tinyca".
#
# ssl-ca=/etc/mysql/cacert.pem
# ssl-cert=/etc/mysql/server-cert.pem
# ssl-key=/etc/mysql/server-key.pem



[mysqldump]
quick
quote-names
max_allowed_packet	= 16M

[mysql]
#no-auto-rehash	# faster start of mysql but no tab completition
default-character-set=utf8

[isamchk]
key_buffer		= 16M

#
# * IMPORTANT: Additional settings that can override those from this file!
#   The files must end with '.cnf', otherwise they'll be ignored.
#
!includedir /etc/mysql/conf.d/
"""




class TestMySQLParser(unittest.TestCase):

    def setUp(self):
        pass
    
    def test_01_simple_cnf(self):
        CP = MySQLParser("testdata/simple.cnf")
        config = CP.get_dict()
        self.assertTrue("section" in config)
        self.assertTrue("section2" in config)
        self.assertEqual(config.get("section").get("key"), "value")
        self.assertEqual(config.get("section2").get("key1"), "v1")
        self.assertEqual(config.get("section2").get("key2"), "v2")

    def test_02_simple2_cnf(self):
        CP = MySQLParser("testdata/simple2.cnf")
        config = CP.get_dict()

        self.assertTrue("section" in config)
        self.assertTrue("section2" in config)
        self.assertEqual(config.get("section").get("key"), "value")
        self.assertEqual(config.get("section2").get("key1"), "v1")
        self.assertEqual(config.get("section2").get("key2"), "v2")
        # A single line value will have None
        self.assertEqual(config.get("section2").get("single-value"), None)

    def test_03_my_cnf(self):
        CP = MySQLParser("testdata/my.cnf")
        config = CP.get_dict()

        output = CP.format(config)
        # Check if all sections are present
        self.assertTrue("mysqld_safe" in config)
        self.assertTrue("mysqld" in config)
        self.assertTrue("mysqldump" in config)
        self.assertTrue("mysql" in config)
        self.assertTrue("isamchk" in config)
        # check strange values
        self.assertEqual(config.get("mysqld").get("init-connect"),
                         "'SET NAMES utf8'")

        # check for includedir
        #self.assertTrue("!includedir" in output)



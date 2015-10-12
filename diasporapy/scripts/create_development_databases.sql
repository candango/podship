-- Copyright 2015 Flavio Garcia
--
-- Licensed under the Apache License, Version 2.0 (the "License");
-- you may not use this file except in compliance with the License.
-- You may obtain a copy of the License at
--
--    http://www.apache.org/licenses/LICENSE-2.0
--
-- Unless required by applicable law or agreed to in writing, software
-- distributed under the License is distributed on an "AS IS" BASIS,
-- WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
-- See the License for the specific language governing permissions and
-- limitations under the License.
--
-- vim: set expandtab tabstop=4 shiftwidth=4 softtabstop=4:
-- This is the script to start to develop.
-- Here a new user diasporapy will be create with the password diasporapypass
-- an a new database called diasporapy will be created with the diasporapy
-- user as owner.
--
-- Don't use this configuration in production for security reasons.

CREATE USER diasporapy WITH CREATEDB PASSWORD 'diasporapypass';

CREATE DATABASE diasporapy OWNER diasporapy;

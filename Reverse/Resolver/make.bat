@echo off
c:\masm32\bin\ml /c /Zd /coff Resolver.asm
c:\\masm32\bin\Link /SUBSYSTEM:CONSOLE Resolver.obj


import marshal,uncompyle6

f = open('wopr.exe_extracted/pyiboot02_cleanup','rb')

a = open('out.py','w')

ob = marshal.load(f)

uncompyle6.main.decompile(None,ob,a)

f.close()
a.close()

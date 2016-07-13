import subprocess, datetime
date = datetime.date.today()
date_today = date.strftime("%d.%m.%Y")
cmd = 'pg_dump -U postgres uzk > E:/uzk('+date_today+').backup'
PIPE = subprocess.PIPE
p = subprocess.Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE,
        stderr=subprocess.STDOUT)
while True:
    s = p.stdout.readline()
    if not s: break
    print (s)
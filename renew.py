#!/usr/local/bin/python2.7

"""
Wraps the "acme cron" command and updates WebFaction if ACME yields a new cert.
Install as a cron job in place of "acme cron".
"""
import sys
import subprocess
import xmlrpclib
from os.path import join
from os import getenv
from certs import certs

user = getenv('wf_username')
pw = getenv('wf_password')
acme_dir_path = '/home/' + user + '/.acme.sh'
SKIP_TEXT = 'Skip, Next renewal time'

def renew(cert):
    domain = cert['domain']
    wf_cert_name = cert['wf_cert_name']
    print 'starting renewal for ' + domain
    proc = subprocess.Popen([acme_dir_path + '/acme.sh', '--renew', '-d', domain], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    if err:
        print err
        sys.exit(err)
    if 'Cert success.' in out:
        # Load cert text
        with open(join(acme_dir_path, domain, domain + ".cer")) as f:
            cert_text = f.read()
        with open(join(acme_dir_path, domain, domain + ".key")) as f:
            key_text = f.read()
        with open(join(acme_dir_path, domain, "ca.cer")) as f:
            ca_text = f.read()
        # Send certs to API
        server = xmlrpclib.ServerProxy('https://api.webfaction.com/', allow_none=True)
        session, account = server.login(user, pw, None, 2)
        server.update_certificate(session, wf_cert_name, cert_text, key_text, ca_text)
        print "Successfully updated cert."
    elif SKIP_TEXT in out:
        for line in out.split('\n'):
            if SKIP_TEXT in line:
                print line
    else:
        print "Cert not updated: Nothing to do."


for cert in certs:
    renew(cert)


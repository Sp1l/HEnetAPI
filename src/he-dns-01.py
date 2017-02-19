#!/usr/local/bin/python2.7

from requests import Request, Session
from lxml import html, etree
import xml.etree.ElementTree as ET

# All classes will work with the session
sess = Session()

class HEsession(object):

    def __init__(self, sess, user_id, user_pw):
        self.user_id = user_id
        self.user_pw = user_pw
        # Authenticate to HE.net DNS service
        post_data = { 'email' : self.user_id, 
                      'pass'  : self.user_pw, 
                      'submit': 'Login!' }
        resp = sess.post('https://dns.he.net/', 
                         data = post_data)
        # Store landing page for later reference
        self.landing = html.fromstring(resp.content)
        # Check for login error
        selector = "//div[@class='caption']/../div[@id='dns_err']/text()"
        nodes = self.landing.xpath(selector)
        if nodes == 'Incorrect':
            print "Login incorrect"
            quit()
        # Get list of domains + id's (not reverse domains)
        selector = "//img[@alt='delete']" \
                        "[not(substring(@name, string-length(@name) - 4) = '.arpa')]" \
                   "/@*[name()='value' or name()='name']"
        nodes = self.landing.xpath(selector)
        # Transform to a dictionary of domain: id
        self.domains = dict(zip(nodes[0::2], nodes[1::2]))

    def getDomains(self):
        return self.domains
        
    def getZoneId(self,domain):
        return self.domains[domain]
    
    def getRR(self,domain, type):
        if self.domains is None:
            self.login()

    def delACMERR(self,domain):
        post_data = { 'hosted_dns_zoneid':   zoneid,
                      'menu':                "edit_zone",
                      'hosted_dns_editzone': ""}
        resp = self.sess.post('https://dns.he.net/', 
                              data = post_data)
        tree = html.fromstring(resp.content)
        selector = "//tr[td='_acme-challenge." \
                   + domain \
                   + "']/td/img[@data='TXT']/../../td[@class='dns_delete']/@onclick"
        nodes = tree.xpath(selector)

class ResourceRecord(object):
        def __init__(self, id, name, type, data)
            self.id   = id
            self.name = name
            self.type = type
            self.data = data

class HEdomain(object):
    Domain = etree.Element('Domain')

    def __init__(self, sess, HEnet, domain):
        # Get the ZoneID
        self.zoneid = HEnet.getZoneId(domain)
        post_data = { 'hosted_dns_zoneid':   self.zoneid,
                      'menu':                "edit_zone",
                      'hosted_dns_editzone': ""}
        resp = sess.post('https://dns.he.net/',
                         data = post_data )
        tree = html.fromstring(resp.content)
        # Extract Id, name, type and data
        selector =  "//tr[@class='dns_tr']/td[2]/text()" \
                    "|//tr[@class='dns_tr']/td[3]/text()" \
                    "|//tr[@class='dns_tr']/td[4]/img/@data" \
                    "|//tr[@class='dns_tr']/td[7]/@data"
        nodes = tree.xpath(selector)
        # Transform into a simple XML structure
        Ids   = nodes[0::4]
        names = nodes[1::4]
        types = nodes[2::4]
        datas = nodes[3::4]
        for i in range(len(Ids)):
            ResR = etree.Subelement(self.Domain, 'Record', id=Ids[i])
            Name = etree.SubElement(RR, 'Name')
            Name.text = names[i]
            Type = etree.SubElement(RR, 'Type')
            Type.text = types[i]
            Data = etree.Subelement(RR, 'Data')
            Data.text = datas[i]
        
    def listRRs():
        for i in range(len(self.Ids)):
            print "Id: %s, Name: %s, Type: %s, Data %s" % \
                (self.Ids[i], self.names[i], self.types[i], self.datas[i])

    def getRecord(id)
        selector = "//Record[Type='TXT'][Name='_acme.brnrd.eu']"
        
    def delRecord(recordid)
        post_data = { 'hosted_dns_zoneid':     self.zoneid,
                      'hosted_dns_recordid':   recordid,
                      'menu':                  "edit_zone",
                      'hosted_dns_delconfirm': "delete", 
                      'hosted_dns_delrecord':  "1",
                      'hosted_dns_editzone':   "1"}

    def addRecord()
        post_data = {
            'menu': "edit_zone"
            'Type': "TXT"
            'hosted_dns_zoneid':501311
            'hosted_dns_editzone':1
            'Priority':
            'Name': "_acme-challenge"
            'Content': "testing123"
            'TTL': "900"
            'hosted_dns_editrecord': "Submit"        }
    
user_id = ""
user_pw = ""
domain =  ""

HEnet = HEsession(sess, user_id, user_pw)

domains = HEnet.getDomains()

print domains

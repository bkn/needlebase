#!/usr/bin/env python
# coding: utf-8

import os
import os.path
import getpass
import urllib
import urllib2
import simplejson

def get_password(create_password_file=False):
    passwordfile = ".password.txt"
    USERNAME, PASSWORD = "", ""
    
    if not os.path.isfile(passwordfile):
        print "A username and password is required."
        print "You can enter info in the prompts below,"
        print " or create a hidden file called:'"+passwordfile+"'"
        print "Put your username and password in separate lines."
        USERNAME = raw_input("Please enter your username: ")
        try:
            PASSWORD = getpass.getpass("Please enter your password: ")
        except getpass.GetPassWarning:
            PASSWORD = raw_input("Please enter your password: ")
    
        print "Thanks!"
        
        if create_password_file:
            print "Creating file with name and password: .password.txt"
            print "This file will be used instead of a prompt next time."
            writepassword(passwordfile, USERNAME, PASSWORD)
    
    else:
        pf = open(passwordfile, "r")
        USERNAME = pf.readline()
        PASSWORD = pf.readline()
        pf.close()
    return USERNAME.strip(), PASSWORD.strip()
    

def writepassword(passwordfile, username, password):
    fh = open(passwordfile, "w")
    fh.write(username + "\n" + password)
    fh.close()

def needle_post(params,service_name='query', ):
    # NEED TO CREATE CLASS FOR LOGIN USERNAME AND PASSWORD
    needle_root = 'https://my.needlebase.com'
    if (service_name == 'edit'): 
        service_url = ''+needle_root+'/actions/api/EditingApi.do?'
    else:
        service_url = ''+needle_root+'/actions/api/V2Visualizer.do?'
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    
    password_mgr.add_password(None, needle_root, username, password)
    handler = urllib2.HTTPBasicAuthHandler(password_mgr)
    opener = urllib2.build_opener(handler)
#    opener.open(a_url) # fetch one url
    urllib2.install_opener(opener) # calls to urllib2.urlopen will use opener
    #header = {"Accept": "text/plain"}
    header = {"Accept": "application/json"}
    print header
    print ''+service_url+params
    req = urllib2.Request(service_url, headers = header, data = params)  
#    req = urllib2.Request(url)        
    fp = urllib2.urlopen(req)  
    response = fp.read()
    fp.close()
    opener.close()
    handler.close()
    try:
        response = simplejson.loads(response)
    except:
        print response
        print 'THE RESPONSE IS NOT VALID JSON'
        response = None
    return response

def needle_query(query,domain):
#    loc = 'https://pub.needlebase.com' 
#    needle_root = 'https://my.needlebase.com' 
#    url = ''
#    url += needle_root
#    url += '/actions/api/V2Visualizer.do?'
    params = 'render=Jsona'
    params += '&domain='+domain    
#    url += '&query='+urllib.quote_plus(query)
    params += '&thread='+urllib.quote_plus(query)
    response = needle_post(params,'query')
    return response

def needle_edit(params):
    response = needle_post(params,'edit')
    return response
    pass

def get_types(domain):
    query = '?._Type^|(.?)'
    response = needle_query(query, domain)
    return response
    
def make_edit_params(param_obj):
    param_str = ''
    for k in param_obj:
        param_str += '&'+k+'='+urllib.quote_plus(param_obj[k])
    return param_str

class Record():
    
    @staticmethod
    def disconnect(value_id, property, node, domain):
        param_obj = {
            "action":  "changeProperty",
            "domain":   domain,
            "node":     node,
            "property": property,
            "remove":      value_id
            }
        response = needle_post(make_edit_params(param_obj),'edit')
            
    @staticmethod
    def connect(value_id, property, node, domain):
        params = ''
        params += 'action=changeProperty'
        params += '&domain='+urllib.quote_plus(domain)
        params += '&node='+urllib.quote_plus(node)
        params += '&property='+urllib.quote_plus(property)
        params += '&add='+urllib.quote_plus(value_id)
        print params
        response = needle_post(params,'edit')
        return response
            
    @staticmethod
    def create(value, type, domain):
    #    Use 'action=create' to create a node for an Article.
    #    Send the 'value' as the display name. 
    #    Use 'edit' to change the display name.
    #    
    #    To specify  'jack' as the author of an article, 
    #    First create a Person node for 'jack'. 
    #    Then use 'changeProperty' to associate the 'jack' node with the Article.Author property. 
    #    The 'changeProperty' call would specify,
    #    
    #    action=changeProperty
    #    node=<the article id>
    #    add=<jack id>
    #    property=<Author>
    #    
        params = ''
        params += 'action=create'
        params += '&domain='+urllib.quote_plus(domain)
        params += '&type='+urllib.quote_plus(type)
        params += '&value='+urllib.quote_plus(value)
        print params
        response = needle_post(params,'edit')
        return response

    def upload(records):
        # expect an array of records
#        each record should specify a type and keys that correspond to property names
#        iterate array of records
#        check if record exists and get node id (use a 'key' property)
#        if it doesn't exist, create record and generate a record key (person_<name>)
#        iterate record object and add properties


        for r in records:
            for k in r:
                pass
            
        pass
    
    
# YOU ARE HERE TRYING TO MAP BIBJSON DATA RECORD
def map_record():#record, schema_map):
    record_type = "person"
    schema_map = {
        "person": {
             "students":     {"property":"students", "type":"person","_Display":"name"},
             "advisors":     {"property":"advisor", "type":"person","_Display":"name"},
             "thesisTitle": {"property":"phdthesis", "type":"phdthesis"},
             "institution": {"property":"affiliation", "type":"affiliation"},
             "name":         {"property":"_Display"},
             "id":            {"property":"key"},
             "type": "person"
         }
        }
    from_record =  {
         "links": [
             {
                 "text": "MathSciNet",
                 "href": "http://www.ams.org/mathscinet/search/author.html?mrauthid=107205&amp;Submit=Search" 
             } 
         ],
         "degree": "Ph.D. ",
         "students": [
             {
                 "ref": "@101426",
                 "name": "Jeffrey Albert" 
             },
             {
                 "ref": "@112049",
                 "name": "Carlos Coelho" 
             },
             {
                 "ref": "@77598",
                 "name": "Garciela Mentz" 
             } 
         ],
         "mrauthid": "107205",
         "advisors": [
             {
                 "ref": "@125584",
                 "name": "Maurice S. Barlett" 
             } 
         ],
         "thesisFlag": "img/flags/UnitedKingdom.gif",
         "id": "42688",
         "thesisCountry": "UnitedKingdom",
         "thesisYear": "1961",
         "thesisTitle": "Some Aspects of Multivariate Analysis",
         "msc": "62",
         "institution": "University of Manchester",
         "name": "Anant M. Kshirsagar"
     }
    t = schema_map[record_type]
    to_record = {}
    for k in from_record:
        to_prop = t[k]['property']
        if (isinstance(from_record[k],list)):
            # expect a list of objects
            for rv in from_record[k]:
                from_prop = t[k]['_Display']
                to_record[to_prop] = from_record[k][from_prop]
        elif (isinstance(from_record[k],list),dict):
            from_prop = t[k]['_Display']
            to_record[to_prop] = from_record[k][from_prop]
        else:
            to_record[to_prop] = from_record[k]

if 1:
    response = {}
    username = 'username'
    password = 'password'
    if username == "username" and password == "password":
        username, password = get_password()   
    
# edit API example url    
# okay to always uses POST
# see https://my.needlebase.com/docs/NeedleReferenceEditingAPI.html
# actions = 
#    create          (type, value), value=display name
#    edit            (node, value), value=display name
#    changeProperty  (node, add, remove, property), 
#    merge,          (node, mergeInto)
#    delete          (node)
#.../api/EditingApi.do?domain=Cows&action=edit&node=1234&value=Mildred    
    
    '''
    Special characters must be escaped in a query
    
    . : ^ / | [ ] ( ) , ! ~ = > < # @ ? _
    
    Brackets are used for escape. For instance to query an email address,
    
    [jack@someplace.com]
    
    '''
    domain = 'Combinatorial-Stochastic-Process'
    query = 'People'
#    query = '?'
    query = 'Article^|_NodeID,_Display, _Type,(.?._NodeID)' # all links for all nodes of a specified type
    # The following query returns separate articles for each attribute value
    # So an article with three authors would generate three separate records
    query = 'Article^|_NodeID,_Display, _Type,(.Person._NodeID),(.Institution._NodeID)'
    domain = 'model-test'
    query = "person._Type^|(.?)"
    query = 'organization'
#    response = get_types(domain)

#    response = Record.create('Universal Global Industries', 'organization', domain )
#    {'modifiedIds': [33]} # Universal Global Industries

    node = '1' # Jack Smack
    property = 'book_authored'
    value = '7'
#    response = Record.connect(value, property, node, domain)

#    response = Record.disconnect(value, property, node, domain)
    
    print response
    query = '@1|_NodeID,_Display, _Type,(.?)' # all links for all nodes of a specified type
    query = '@1|advisor,students,book_authored,book_edited' # all links for all nodes of a specified type
    query = '@1'
#    query = '@1|?.?'
#    query = '@1.?|(._Type)'
#    query = '@1|(.?)'
#    query = '@1._Count|(..nodes:#<=100|person)'
#    query = '@1._Count|(..nodes:#<=100|advisor,book_authored,book_edited,phdthesis,students|?,_Merge Tree),(..nodes.nodes._Count)'
#    query = "person._Type^|(.?)"
    response = needle_query(query, domain)
    print simplejson.dumps(response, indent=2)
    


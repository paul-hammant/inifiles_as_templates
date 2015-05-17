from bottle import route, run, template, static_file
import ConfigParser 
import simplejson as json
import codecs


@route('/css/common.css')
def static_css():    
    return static_file("common.css", root="./css")

@route('/js/skel.min.js')
def static_js():
    return static_file("skel.min.js", root="./js")

@route('/')
def index():
    return template("index.html")

@route('/<table>')
def index(table):    
    menu = ConfigParser.RawConfigParser() 
    # menu.read("menu.ini") 
    menu.readfp(codecs.open("menu.ini", "r", "utf8"))

    print menu

    menu2 = {}
    menu2["sections"] = []

    for section in menu.__dict__['_sections'].items(): 
        # print "Section = " + section[0]
        if section[0] == "header":
            menu2["title"] = menu.get("header", "title")
        else:
            section2 = {}
            section2["name"] = section[0]
            section2["choices"] = []
            for kv in section[1].items():
                if kv[0] == "text":  
                    section2["text"] = kv[1]
                elif kv[0] != "__name__": 
                    choice = {}
                    choice["id"] = kv[0]
                    desc_and_price = kv[1].split("|")
                    choice["desc"] = desc_and_price[0].strip() 
                    choice["price"] = desc_and_price[1].strip()
                    section2["choices"].append(choice)
            menu2["sections"].append(section2)
    return template("menu.html", menu = menu2, table = table)

run(host='localhost', port=8080)


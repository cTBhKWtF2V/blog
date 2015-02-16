import glob, datetime, os

import jinja2

files = glob.glob('./posts/*')
WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday','Friday', 'Saturday','Sunday']
MONTHS = ["January","February","March",	"April","May",	"June",	"July",	"August",	"September",	"October",	"November",	"December"]

class Post:
	id = ""
	date = datetime.date.today()
	weekday = ""
	month = ""
	title = "no title"
	tags = ""
	content = ""

posts = []
tags = {}

JINJA_ENVIORNMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

for file_name in files:
	with open(file_name,'r') as f:
		post = Post()
		post.id = file_name.split('/')[-1]
		date_str = f.readline().split(',')
		post.date = datetime.date(int(date_str[0]),int(date_str[1]), int(date_str[2]))
		post.weekday = WEEKDAYS[post.date.weekday()]
		post.month = MONTHS[post.date.month-1]
		post.title = f.readline()
		post.tags = f.readline().lower().strip().split(',')
		post.tags = ['-'.join(i.strip().split(' ')) for i in post.tags]
		post.content = f.read()
		posts.append(post)
		for tag in post.tags:
			if not tags.has_key(tag):
				tags[tag] = []
			tags[tag].append(post)

posts.sort(key=lambda x: x.date, reverse=True)
for t in tags.keys():
	tags[t].sort(key=lambda x: x.date, reverse=True)

template = JINJA_ENVIORNMENT.get_template('template.html')

template_values ={
	'posts':posts,
}

outfile = open('index.html','w')
outfile.write(template.render(template_values))
outfile.close()

for t in tags.keys():
	outfile = open(t+".html",'w')
	template_values['tag'] = t
	template_values['posts'] = tags[t]
	outfile.write(template.render(template_values))
	outfile.close()




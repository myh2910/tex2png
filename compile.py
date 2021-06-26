import os
from glob import glob
from colorama import Fore
from timeit import default_timer as timer

def convert(level, pacman):
	parents = []
	total = 0
	with open(level, 'r') as o:
		original = o.readlines()
		for i, line in enumerate(original):
			for pkg in pacman:
				if pkg['id'] in parents or pkg['cmd'] in line:
					parent = pkg['parent']
					if parent:
						parents.append(parent)
					pkg['stat'] = True
			if '%%' in line and i > 0 or i > len(original) - 2:
				with open(tex_file, 'r+') as t:
					contents = t.readlines()
					if i > len(original) - 2:
						contents.append(line)
					if i > 0:
						contents.append('\\end{document}')
					for pkg in pacman:
						if pkg['stat']:
							contents.insert(insert_point, pkg['code'])
							pkg['stat'] = False
					t.seek(0)
					t.writelines(contents)
				print(f'{Fore.LIGHTMAGENTA_EX}Compiling file {Fore.LIGHTCYAN_EX}{tex_file}{Fore.LIGHTMAGENTA_EX}...{Fore.RESET}')
				os.system(f'latexmk -silent {tex_file}')
				parents = []
				total += 1
			if '%%' in line:
				types = line.strip().split('.')
				file_type = types[0][2:]
				tex_dir = f'tex/{os.path.basename(level)[:-4]}/{file_type[1:]}/'
				if not os.path.exists(tex_dir):
					os.makedirs(tex_dir)
				tex_file = f'{tex_dir}{file_type}.tex'
				with open(tex_file, 'w') as t:
					t.write('\\documentclass[margin=1pt,preview]{standalone}\n')
					insert_point = 2
					if 'sp' in types[1:]:
						t.write('\\usepackage[spanish]{babel}\n')
						insert_point += 1
					t.write('\\usepackage{amsmath,amssymb,cmbright}\n')
					if file_type[0] == 'r':
						t.write(r'''\usepackage{xcolor}
\begin{document}
\color{red}
''')
						insert_point += 1
					else:
						t.write('\\begin{document}\n')
			elif i < len(original) - 1:
				with open(tex_file, 'a') as t:
					t.write(line)
	return total

def compile(*levels):
	start = timer()
	if len(levels) == 0:
		levels = glob('levels/*.tex')
	else:
		levels = [f'levels/{x}.tex' for x in levels]
	pacman = [
		{
			'id': 'array',
			'cmd': '\\begin{tabular}',
			'parent': None,
			'code': '\\usepackage{array}\n'
		},
		{
			'id': 'mhchem',
			'cmd': '\\ce{',
			'parent': None,
			'code': '\\usepackage{mhchem}\n'
		},
		{
			'id': 'multirow',
			'cmd': '\\multirow{',
			'parent': None,
			'code': '\\usepackage{multirow}\n'
		},
		{
			'id': 'xcolor',
			'cmd': '\\color{',
			'parent': None,
			'code': '\\usepackage{xcolor}\n'
		},
		{
			'id': 'tikz',
			'cmd': '\\begin{tikzpicture}',
			'parent': None,
			'code': '\\usepackage{tikz}\n'
		},
		{
			'id': 'tikz.matrix',
			'cmd': '\\matrix',
			'parent': 'tikz',
			'code': '\\usetikzlibrary{matrix}\n'
		},
		{
			'id': 'tkz-euclide',
			'cmd': '\\tkz',
			'parent': None,
			'code': '\\usepackage{tkz-euclide}\n'
		},
		{
			'id': 'tasks',
			'cmd': '\\begin{tasks}',
			'parent': None,
			'code': '\\usepackage{tasks}\n'
		},
		{
			'id': 'enum',
			'cmd': '\\begin{enum}',
			'parent': 'tasks',
			'code': '\\NewTasksEnvironment[label=\\Alph*)]{enum}[*]\n'
		},
		{
			'id': 'enum*',
			'cmd': '\\begin{enum*}',
			'parent': 'tasks',
			'code': '\\NewTasksEnvironment[label=\\Alph*)]{enum*}[*](4)\n'
		},
		{
			'id': 'task',
			'cmd': '\\begin{task}',
			'parent': 'enum*',
			'code': '\\newenvironment{task}{\\begin{minipage}{.6\\linewidth}\\begin{enum*}}{\\end{enum*}\\end{minipage}}\n'
		},
		{
			'id': 'mini',
			'cmd': '\\begin{mini}',
			'parent': None,
			'code': '\\newenvironment{mini}[1][.6]{\\begin{minipage}{#1\\linewidth}}{\\end{minipage}}\n'
		},
		{
			'id': 'dang',
			'cmd': '\\dang',
			'parent': None,
			'code': '\\newcommand{\\dang}{\\measuredangle}\n'
		},
		{
			'id': 'dg',
			'cmd': '\\dg',
			'parent': None,
			'code': '\\newcommand{\\dg}{^\\circ}\n'
		},
		{
			'id': 'ii',
			'cmd': '\\ii',
			'parent': None,
			'code': '\\newcommand{\\ii}{\\item}\n'
		},
		{
			'id': 'ol',
			'cmd': '\\ol',
			'parent': None,
			'code': '\\newcommand{\\ol}{\\overline}\n'
		},
		{
			'id': 'GA',
			'cmd': '\\GA',
			'parent': None,
			'code': '\\DeclareMathOperator{\\GA}{GA}\n'
		},
		{
			'id': 'GR',
			'cmd': '\\GR',
			'parent': None,
			'code': '\\DeclareMathOperator{\\GR}{GR}\n'
		}
	]
	pacman.reverse()
	for pkg in pacman:
		pkg['stat'] = False
	total = 0
	for level in levels:
		if os.path.exists(level):
			print(f'{Fore.LIGHTGREEN_EX}File {Fore.LIGHTCYAN_EX}{level} {Fore.LIGHTGREEN_EX}found. Processing images...')
			total += convert(level, pacman)
		else:
			print(f'{Fore.LIGHTRED_EX}Error! The file {Fore.LIGHTYELLOW_EX}{level} {Fore.LIGHTRED_EX}does not exist.')
	end = timer()
	print(f'{Fore.LIGHTYELLOW_EX}Compiled files: {Fore.LIGHTCYAN_EX}{total} {Fore.LIGHTYELLOW_EX}documents.')
	print(f'Elapsed time: {Fore.LIGHTCYAN_EX}{end - start} {Fore.LIGHTYELLOW_EX}seconds.')

if __name__ == '__main__':
	compile()

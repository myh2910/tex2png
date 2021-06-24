import os
from glob import glob
from colorama import Fore
from timeit import default_timer as timer

pkg_manager = [
	{
		'name': 'array',
		'stat': False,
		'id': '\\begin{tabular}',
		'parent': None,
		'code': '\\usepackage{array}\n'
	},
	{
		'name': 'multirow',
		'stat': False,
		'id': '\\multirow{',
		'parent': None,
		'code': '\\usepackage{multirow}\n'
	},
	{
		'name': 'xcolor',
		'stat': False,
		'id': '\\color{',
		'parent': None,
		'code': '\\usepackage{xcolor}\n'
	},
	{
		'name': 'tikz',
		'stat': False,
		'id': '\\begin{tikzpicture}',
		'parent': None,
		'code': r'''\usepackage{tikz}
\usetikzlibrary{calc,scopes,shapes.geometric}
'''
	},
	{
		'name': 'tikz.angles',
		'stat': False,
		'id': 'angle',
		'parent': 'tikz',
		'code': '\\usetikzlibrary{angles,quotes}\n'
	},
	{
		'name': 'tikz.intersections',
		'stat': False,
		'id': 'intersection',
		'parent': 'tikz',
		'code': '\\usetikzlibrary{intersections}\n'
	},
	{
		'name': 'mini',
		'stat': False,
		'id': '\\begin{mini}',
		'parent': None,
		'code': '\\newenvironment{mini}{\\begin{minipage}{.6\\linewidth}}{\\end{minipage}}\n'
	},
	{
		'name': 'tasks',
		'stat': False,
		'id': '\\begin{tasks}',
		'parent': None,
		'code': '\\usepackage{tasks}\n'
	},
	{
		'name': 'enum',
		'stat': False,
		'id': '\\begin{enum}',
		'parent': 'tasks',
		'code': '\\NewTasksEnvironment[label=\\Alph*)]{enum}[*]\n'
	},
	{
		'name': 'task',
		'stat': False,
		'id': '\\begin{task}',
		'parent': 'tasks',
		'code': r'''\NewTasksEnvironment[label=\Alph*)]{enum*}[*](4)
\newenvironment{task}{\begin{minipage}{.6\linewidth}\begin{enum*}}{\end{enum*}\end{minipage}}
'''
	},
	{
		'name': 'dg',
		'stat': False,
		'id': '\\dg',
		'parent': None,
		'code': '\\newcommand{\\dg}{^\\circ}\n'
	},
	{
		'name': 'GA',
		'stat': False,
		'id': '\\GA',
		'parent': None,
		'code': '\\DeclareMathOperator{\\GA}{GA}\n'
	},
	{
		'name': 'GR',
		'stat': False,
		'id': '\\GR',
		'parent': None,
		'code': '\\DeclareMathOperator{\\GR}{GR}\n'
	}
]
def convert(level):
	with open(level, 'r') as o:
		original = o.readlines()
		pacman = list(reversed(pkg_manager))
		parents = []
		for i, line in enumerate(original):
			for pkg in pacman:
				if pkg['name'] in parents:
					pkg['stat'] = True
				if pkg['id'] in line:
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
							contents.insert(2, pkg['code'])
							pkg['stat'] = False
					parents = []
					t.seek(0)
					t.writelines(contents)
				print(f'{Fore.LIGHTMAGENTA_EX}Compiling file {Fore.LIGHTYELLOW_EX}{tex_file}{Fore.LIGHTMAGENTA_EX}...{Fore.RESET}')
				os.system(f'latexmk -quiet {tex_file}')
			if '%%' in line:
				tex_dir = f'tex/{os.path.basename(level)[:-4]}/'
				if not os.path.exists(tex_dir):
					os.makedirs(tex_dir)
				types = line.strip().split('.')
				kind = types[0][2:]
				tex_file = f'{tex_dir}{kind}.tex'
				with open(tex_file, 'w') as t:
					t.write(r'''\documentclass[margin=1pt,preview]{standalone}
\usepackage{amsmath,amssymb,cmbright}
''')
					if 'sp' in types:
						t.write('\\usepackage[spanish]{babel}\n')
					if kind[0] == 'r':
						t.write(r'''\usepackage{xcolor}
\begin{document}
\color{red}
''')
					else:
						t.write('\\begin{document}\n')
			elif i < len(original) - 1:
				with open(tex_file, 'a') as t:
					t.write(line)

def compile(*levels):
	start = timer()
	if len(levels) == 0:
		levels = glob('levels/*.tex')
	else:
		levels = [f'levels/{x}.tex' for x in levels]
	for level in levels:
		if os.path.exists(level):
			print(f'{Fore.LIGHTGREEN_EX}File {Fore.LIGHTYELLOW_EX}{level} {Fore.LIGHTGREEN_EX}found. Processing images...')
			convert(level)
		else:
			print(f'{Fore.LIGHTRED_EX}Error! The file {Fore.LIGHTYELLOW_EX}{level} {Fore.LIGHTRED_EX}does not exist.')
	end = timer()
	print(f'{Fore.LIGHTYELLOW_EX}Elapsed time: {Fore.LIGHTCYAN_EX}{end - start} {Fore.LIGHTYELLOW_EX}seconds.')

if __name__ == '__main__':
	compile()

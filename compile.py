import os
from glob import glob
from colorama import Fore
from timeit import default_timer as timer

pkg_manager = [
	{
		'name': 'array',
		'stat': False,
		'cmd': '\\begin{tabular}',
		'parent': None,
		'code': '\\usepackage{array}\n'
	},
	{
		'name': 'multirow',
		'stat': False,
		'cmd': '\\multirow{',
		'parent': None,
		'code': '\\usepackage{multirow}\n'
	},
	{
		'name': 'xcolor',
		'stat': False,
		'cmd': '\\color{',
		'parent': None,
		'code': '\\usepackage{xcolor}\n'
	},
	{
		'name': 'tkz-euclide',
		'stat': False,
		'cmd': '\\tkz',
		'parent': None,
		'code': '\\usepackage{tkz-euclide}\n'
	},
	{
		'name': 'tikz',
		'stat': False,
		'cmd': '\\begin{tikzpicture}',
		'parent': None,
		'code': r'''\usepackage{tikz}
\usetikzlibrary{calc,scopes,shapes.geometric}
'''
	},
	{
		'name': 'tikz.angles',
		'stat': False,
		'cmd': 'angle',
		'parent': 'tikz',
		'code': '\\usetikzlibrary{angles,quotes}\n'
	},
	{
		'name': 'tikz.intersections',
		'stat': False,
		'cmd': 'intersection',
		'parent': 'tikz',
		'code': '\\usetikzlibrary{intersections}\n'
	},
	{
		'name': 'mini',
		'stat': False,
		'cmd': '\\begin{mini}',
		'parent': None,
		'code': '\\newenvironment{mini}{\\begin{minipage}{.6\\linewidth}}{\\end{minipage}}\n'
	},
	{
		'name': 'tasks',
		'stat': False,
		'cmd': '\\begin{tasks}',
		'parent': None,
		'code': '\\usepackage{tasks}\n'
	},
	{
		'name': 'enum',
		'stat': False,
		'cmd': '\\begin{enum}',
		'parent': 'tasks',
		'code': '\\NewTasksEnvironment[label=\\Alph*)]{enum}[*]\n'
	},
	{
		'name': 'task',
		'stat': False,
		'cmd': '\\begin{task}',
		'parent': 'tasks',
		'code': r'''\NewTasksEnvironment[label=\Alph*)]{enum*}[*](4)
\newenvironment{task}{\begin{minipage}{.6\linewidth}\begin{enum*}}{\end{enum*}\end{minipage}}
'''
	},
	{
		'name': 'dang',
		'stat': False,
		'cmd': '\\dang',
		'parent': None,
		'code': '\\newcommand{\\dang}{\\measuredangle}\n'
	},
	{
		'name': 'dg',
		'stat': False,
		'cmd': '\\dg',
		'parent': None,
		'code': '\\newcommand{\\dg}{^\\circ}\n'
	},
	{
		'name': 'GA',
		'stat': False,
		'cmd': '\\GA',
		'parent': None,
		'code': '\\DeclareMathOperator{\\GA}{GA}\n'
	},
	{
		'name': 'GR',
		'stat': False,
		'cmd': '\\GR',
		'parent': None,
		'code': '\\DeclareMathOperator{\\GR}{GR}\n'
	}
]
def convert(level):
	pacman = list(reversed(pkg_manager))
	parents = []
	total = 0
	with open(level, 'r') as o:
		original = o.readlines()
		for i, line in enumerate(original):
			for pkg in pacman:
				if pkg['name'] in parents:
					pkg['stat'] = True
				if pkg['cmd'] in line:
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
					t.seek(0)
					t.writelines(contents)
				print(f'{Fore.LIGHTMAGENTA_EX}Compiling file {Fore.LIGHTYELLOW_EX}{tex_file}{Fore.LIGHTMAGENTA_EX}...{Fore.RESET}')
				os.system(f'latexmk -quiet -cd- -outdir={dirs[0]} {tex_file}')
				parents = []
				total += 1
			if '%%' in line:
				dirs = [f'{x}/{os.path.basename(level)[:-4]}/' for x in ['tex', 'png']]
				for d in dirs:
					if not os.path.exists(d):
						os.makedirs(d)
				types = line.strip().split('.')
				kind = types[0][2:]
				tex_file = f'{dirs[0]}{kind}.tex'
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
	return total

def compile(*levels):
	start = timer()
	if len(levels) == 0:
		levels = glob('levels/*.tex')
	else:
		levels = [f'levels/{x}.tex' for x in levels]
	total = 0
	for level in levels:
		if os.path.exists(level):
			print(f'{Fore.LIGHTGREEN_EX}File {Fore.LIGHTYELLOW_EX}{level} {Fore.LIGHTGREEN_EX}found. Processing images...')
			total += convert(level)
		else:
			print(f'{Fore.LIGHTRED_EX}Error! The file {Fore.LIGHTYELLOW_EX}{level} {Fore.LIGHTRED_EX}does not exist.')
	end = timer()
	print(f'{Fore.LIGHTYELLOW_EX}Compiled files: {Fore.LIGHTCYAN_EX}{total} {Fore.LIGHTYELLOW_EX}documents.')
	print(f'Elapsed time: {Fore.LIGHTCYAN_EX}{end - start} {Fore.LIGHTYELLOW_EX}seconds.')

if __name__ == '__main__':
	compile()

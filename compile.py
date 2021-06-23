import os
from glob import glob
from colorama import Fore
from timeit import default_timer as timer

pkg_manager = [
	{
		'stat': False,
		'id': '\\begin{tabular}',
		'use': '\\usepackage{array}\n'
	},
	{
		'stat': False,
		'id': '\\multirow{',
		'use': '\\usepackage{multirow}\n'
	},
	{
		'stat': False,
		'id': '\\color{',
		'use': '\\usepackage{xcolor}\n'
	},
	{
		'stat': False,
		'id': '\\begin{tikzpicture}',
		'use': r"""\usepackage{tikz}
\usetikzlibrary{angles,calc,quotes,scopes,shapes.geometric}
"""
	},
	{
		'stat': False,
		'id': '\\begin{mini}',
		'use': r"""\newenvironment{mini}{\begin{minipage}{.6\linewidth}}{\end{minipage}}
"""
	},
	{
		'stat': False,
		'id': '\\begin{enum}',
		'use': r"""\usepackage{tasks}
\NewTasksEnvironment[label=\Alph*)]{enum}[*]
\NewTasksEnvironment[label=\Alph*)]{enum*}[*](4)
"""
	},
	{
		'stat': False,
		'id': '\\begin{task}',
		'use': r"""\newenvironment{task}{\begin{minipage}{.6\linewidth}\begin{enum*}}{\end{enum*}\end{minipage}}
"""
	},
	{
		'stat': False,
		'id': '\\dg',
		'use': r"""\newcommand{\dg}{^\circ}
"""
	},
	{
		'stat': False,
		'id': '\\GA',
		'use': r"""\DeclareMathOperator{\GA}{GA}
"""
	},
	{
		'stat': False,
		'id': '\\GR',
		'use': r"""\DeclareMathOperator{\GR}{GR}
"""
	}
]
def convert(level):
	with open(level, 'r') as o:
		original = o.readlines()
		pacman = list(reversed(pkg_manager))
		for i, line in enumerate(original):
			for pkg_idx, pkg in enumerate(pacman):
				if pkg['id'] in line:
					if pkg_idx == 3:
						pacman[4]['stat'] = True
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
							contents.insert(2, pkg['use'])
							pkg['stat'] = False
					t.seek(0)
					t.writelines(contents)
				print(f'{Fore.LIGHTMAGENTA_EX}Compiling file {tex_file}...{Fore.LIGHTCYAN_EX}')
				os.system(f'latexmk -quiet {tex_file}\
					&& pdftocairo -png -singlefile -transp -r 2000 {tex_file[:-4]}.pdf {png_file[:-4]}\
					&& convert -density 300 -trim {png_file} -quality 100 {png_file}')
				print(Fore.RESET)
			if '%%' in line:
				dirs = [f'levels/{x}/{os.path.basename(level)[:-4]}/' for x in ['tex', 'png']]
				for d in dirs:
					if not os.path.exists(d):
						os.makedirs(d)
				types = line.strip().split('.')
				kind = types[0][2:]
				tex_file, png_file = f'{dirs[0]}{kind}.tex', f'{dirs[1]}{kind}.png'
				with open(tex_file, 'w') as t:
					t.write(r"""\documentclass[margin=1pt,preview]{standalone}
\usepackage{amsmath,amssymb,cmbright}
""")
					if 'sp' in types:
						t.write('\\usepackage[spanish]{babel}\n')
					if kind[0] == 'r':
						t.write(r"""\usepackage{xcolor}
\begin{document}
\color{red}
""")
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
			print(f'{Fore.LIGHTGREEN_EX}File {level} found. Processing images...{Fore.RESET}')
			convert(level)
		else:
			print(f'{Fore.LIGHTRED_EX}Error! The file {level} does not exist.{Fore.RESET}')
	end = timer()
	print(end - start)

if __name__ == '__main__':
	compile()

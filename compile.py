import os
from glob import glob
from colorama import Fore
def convert(level):
	with open(level, 'r') as o:
		original = o.readlines()
		for i, line in enumerate(original):
			if '%%' in line and i > 0 or i > len(original) - 2:
				with open(tex_file, 'a') as t:
					if i > len(original) - 2:
						t.write(line)
					if i > 0:
						t.write('\\end{document}')
				with open(tex_file, 'r+') as t:
					gr, ga, dg = False, False, False
					enum, mini, tasks, tikz = False, False, False, False
					xcolor, multirow, array = False, False, False
					contents = t.readlines()
					for content in contents:
						if '\\GR' in content:
							gr = True
						if '\\GA' in content:
							ga = True
						if '\\dg' in content:
							dg = True
						if '\\begin{enum}' in content:
							enum = True
						if '\\begin{mini}' in content:
							mini = True
						if '\\begin{task}' in content:
							tasks = True
						if 'tikz' in content:
							tikz = True
						if '\\color' in content:
							xcolor = True
						if 'multirow' in content:
							multirow = True
						if '\\begin{tabular}' in content:
							array = True
					if gr:
						contents.insert(2, '\\DeclareMathOperator{\\GR}{GR}\n')
					if ga:
						contents.insert(2, '\\DeclareMathOperator{\\GA}{GA}\n')
					if dg:
						contents.insert(2, '\\newcommand{\\dg}{^\\circ}\n')
					if tasks:
						enum, mini = True, True
						contents.insert(2, '\\newenvironment{task}{\\begin{mini}\\begin{enum*}}{\\end{enum*}\\end{mini}}\n')
					if enum:
						contents.insert(2, """\\usepackage{tasks}
\\NewTasksEnvironment[label=\\Alph*)]{enum}[*]
\\NewTasksEnvironment[label=\\Alph*)]{enum*}[*](4)
""")
					if mini:
						contents.insert(2, '\\newenvironment{mini}{\\begin{minipage}{.6\\linewidth}}{\\end{minipage}}\n')
					if tikz:
						contents.insert(2, """\\usepackage{tikz}
\\usetikzlibrary{angles,calc,quotes,scopes,shapes.geometric}
""")
					if xcolor:
						contents.insert(2, '\\usepackage{xcolor}\n')
					if multirow:
						contents.insert(2, '\\usepackage{multirow}\n')
					if array:
						contents.insert(2, '\\usepackage{array}\n')
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
					t.write("""\\documentclass[margin=1pt,preview]{standalone}
\\usepackage{amsmath,amssymb,cmbright}
""")
					if 'sp' in types:
						t.write('\\usepackage[spanish]{babel}\n')
					t.write('\\begin{document}\n')
					if kind[0] == 'r':
						t.write('\color{red}\n')
			elif i < len(original) - 1:
				with open(tex_file, 'a') as t:
					t.write(line)
def compile(*levels):
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

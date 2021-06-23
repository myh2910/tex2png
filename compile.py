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
				kind = line.strip()[2:]
				tex_file, png_file = f'{dirs[0]}{kind}.tex', f'{dirs[1]}{kind}.png'
				with open(tex_file, 'w') as t:
					with open('preamble.tex', 'r') as f:
						t.write(f.read())
					t.write('\\begin{document}\n')
					try:
						with open(f'macros/{kind[0]}.tex', 'r') as f:
							t.write(f.read())
					except:
						pass
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

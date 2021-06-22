import os
from glob import glob
from colorama import Fore
levels = glob('levels/*.tex')
for level in levels:
	with open(level, 'r') as o:
		original = o.readlines()
		for i, line in enumerate(original):
			if '%%' in line and i > 0 or i > len(original) - 2:
				with open(tex_file, 'a') as t:
					if i > len(original) - 2:
						t.write(line)
					if i > 0:
						t.write('\\end{document}')
				print(Fore.CYAN + tex_file + Fore.RESET)
				os.system(f'latexmk -quiet {tex_file} &&\
					pdftocairo -png -singlefile -transp -r 2000 {tex_file[:-4]}.pdf {png_file[:-4]} &&\
					convert -density 300 -trim {png_file} -quality 100 {png_file}')
			if '%%' in line:
				dirs = [f'levels/{x}/{os.path.basename(level)[:-4]}/' for x in ['tex', 'png']]
				for d in dirs:
					if not os.path.exists(d):
						os.makedirs(d)
				kind = line.strip()[2:]
				tex_file, png_file = f'{dirs[0]}{kind}.tex', f'{dirs[1]}{kind}.png'
				with open(tex_file, 'w') as t:
					for file in ['preamble.tex', f'macros/{kind[0]}.tex', 'macros.tex']:
						with open(file, "r") as f:
							t.write(f.read())
					t.write('\\begin{document}\n')
			elif i < len(original) - 1:
				with open(tex_file, 'a') as t:
					t.write(line)

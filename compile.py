import os
from glob import glob
from timeit import default_timer as timer

from colorama import Fore

pacman = [
    {
        "id": "array",
        "cmd": "\\begin{tabular}",
        "parent": None,
        "code": "\\usepackage{array}\n",
    },
    {
        "id": "enumitem",
        "cmd": "\\begin{enumerate}",
        "parent": None,
        "code": "\\usepackage{enumitem}\n",
    },
    {
        "id": "mhchem",
        "cmd": "\\ce{",
        "parent": None,
        "code": "\\usepackage{mhchem}\n",
    },
    {
        "id": "multirow",
        "cmd": "\\multirow{",
        "parent": None,
        "code": "\\usepackage{multirow}\n",
    },
    {
        "id": "tikz",
        "cmd": "\\begin{tikzpicture}",
        "parent": None,
        "code": "\\usepackage{tikz}\n",
    },
    {
        "id": "tikz.matrix",
        "cmd": "\\matrix",
        "parent": "tikz",
        "code": "\\usetikzlibrary{matrix}\n",
    },
    {
        "id": "tkz-euclide",
        "cmd": "\\tkz",
        "parent": None,
        "code": "\\usepackage{tkz-euclide}\n",
    },
    {
        "id": "tasks",
        "cmd": "\\begin{tasks}",
        "parent": None,
        "code": "\\usepackage{tasks}\n",
    },
    {
        "id": "enum",
        "cmd": "\\begin{enum}",
        "parent": "tasks",
        "code": "\\NewTasksEnvironment[label=\\Alph*)]{enum}[*]\n",
    },
    {
        "id": "enum*",
        "cmd": "\\begin{enum*}",
        "parent": "tasks",
        "code": "\\NewTasksEnvironment[label=\\Alph*)]{enum*}[*](4)\n",
    },
    {
        "id": "task",
        "cmd": "\\begin{task}",
        "parent": "enum*",
        "code": "\\newenvironment{task}{\\begin{minipage}{.6\\linewidth}\\begin{enum*}}{\\end{enum*}\\end{minipage}}\n",
    },
    {
        "id": "mini",
        "cmd": "\\begin{mini}",
        "parent": None,
        "code": "\\newenvironment{mini}[1][.6]{\\begin{minipage}{#1\\linewidth}}{\\end{minipage}}\n",
    },
    {
        "id": "dang",
        "cmd": "\\dang",
        "parent": None,
        "code": "\\newcommand{\\dang}{\\measuredangle}\n",
    },
    {
        "id": "dg",
        "cmd": "\\dg",
        "parent": None,
        "code": "\\newcommand{\\dg}{^\\circ}\n",
    },
    {
        "id": "ii",
        "cmd": "\\ii",
        "parent": None,
        "code": "\\newcommand{\\ii}{\\item}\n",
    },
    {
        "id": "ol",
        "cmd": "\\ol",
        "parent": None,
        "code": "\\newcommand{\\ol}{\\overline}\n",
    },
    {
        "id": "GA",
        "cmd": "\\GA",
        "parent": None,
        "code": "\\DeclareMathOperator{\\GA}{GA}\n",
    },
    {
        "id": "GR",
        "cmd": "\\GR",
        "parent": None,
        "code": "\\DeclareMathOperator{\\GR}{GR}\n",
    },
]


def compile_tex_files(path, name):
    parents = []
    num_files = 0

    with open(path, "r") as o:
        original = o.readlines()
        tex_file = ""
        insert_point = 0

        for i, line in enumerate(original):
            for pkg in pacman:
                if pkg["id"] in parents or pkg["cmd"] in line:
                    parent = pkg["parent"]
                    if parent:
                        parents.append(parent)
                    pkg["stat"] = True

            if "%%" in line and i > 0 or i > len(original) - 2:
                with open(tex_file, "r+") as t:
                    contents = t.readlines()
                    if i > len(original) - 2:
                        contents.append(line)
                    if i > 0:
                        contents.append("\\end{document}")
                    for pkg in pacman:
                        if pkg["stat"]:
                            contents.insert(insert_point, pkg["code"])
                            pkg["stat"] = False
                    t.seek(0)
                    t.writelines(contents)
                print(
                    "%sCompiling file %s%s%s...%s"
                    % (
                        Fore.LIGHTMAGENTA_EX,
                        Fore.LIGHTCYAN_EX,
                        tex_file,
                        Fore.LIGHTMAGENTA_EX,
                        Fore.RESET,
                    )
                )
                os.system(f'latexmk -silent "{tex_file}"')
                parents = []
                num_files += 1

            if "%%" in line:
                types = line.strip().split(".")
                file_type = types[0][2:]
                tex_dir = f"tex/{name}/{file_type[1:]}/"
                tex_file = f"{tex_dir}{file_type}.tex"

                if not os.path.exists(tex_dir):
                    os.makedirs(tex_dir)

                with open(tex_file, "w") as t:
                    t.write("\\documentclass[margin=1pt,preview]{standalone}\n")
                    insert_point = 2
                    if "sp" in types[1:]:
                        t.write("\\usepackage[spanish]{babel}\n")
                        insert_point += 1
                    t.write("\\usepackage{amsmath,amssymb,cmbright}\n")
                    if file_type[0] == "r":
                        t.write(
                            "\\usepackage{xcolor}\n\\begin{document}\n\\color{red}\n"
                        )
                        insert_point += 1
                    else:
                        t.write("\\begin{document}\n")

            elif i < len(original) - 1:
                with open(tex_file, "a") as t:
                    t.write(line)
    return num_files


def copy_images(name):
    tex_dir = f"tex/{name}/"
    png_dir = f"png/{name}/"

    if not os.path.exists(png_dir):
        os.makedirs(png_dir)

    os.system(f"cp -u {tex_dir}**/*.png {png_dir}")


def main(*levels):
    start_time = timer()

    pacman.reverse()

    for pkg in pacman:
        pkg["stat"] = False

    if len(levels) == 0:
        paths = glob("levels/*.tex")
    else:
        paths = [f"levels/{name}.tex" for name in levels]

    num_files = 0
    for path in paths:
        if os.path.exists(path):
            print(
                "%sFile %s%s%s found. Compiling TeX files..."
                % (Fore.LIGHTGREEN_EX, Fore.LIGHTCYAN_EX, path, Fore.LIGHTGREEN_EX)
            )
            name = os.path.basename(path)[:-4]
            num_files += compile_tex_files(path, name)
            copy_images(name)
        else:
            print(
                "%sError! The file %s%s%s does not exist."
                % (Fore.LIGHTRED_EX, Fore.LIGHTYELLOW_EX, path, Fore.LIGHTRED_EX)
            )

    end_time = timer()

    print(
        "%sProcessed %s%s%s images."
        % (Fore.LIGHTYELLOW_EX, Fore.LIGHTCYAN_EX, num_files, Fore.LIGHTYELLOW_EX)
    )
    print(
        "Elapsed time: %s%0.2f%s seconds."
        % (Fore.LIGHTCYAN_EX, end_time - start_time, Fore.LIGHTYELLOW_EX)
    )


if __name__ == "__main__":
    main()

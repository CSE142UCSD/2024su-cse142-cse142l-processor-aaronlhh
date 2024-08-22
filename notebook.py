import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt
import math
from IPython.display import IFrame, Image, TextDisplayObject
import subprocess 
import os
from collections import namedtuple
from IPython.display import display, Markdown, Latex, Code, HTML
import re
import copy
import pandas
from autograde import *
import glob
from IPython.core.display import HTML
import delegate_function
import cfiddle
from cfiddle import *
from hungwei import HungWeiExecutionMethod
cfiddle.set_config("RunnerExecutionMethod_type", HungWeiExecutionMethod)

import os
from pathlib import Path
with open(str(Path.home())+"/.ssh/id_rsa.pub", 'r') as file:
    pub_key = file.read()
file.close()
if not (os.path.isfile(str(Path.home())+"/.ssh/authorized_keys")): 
    authorized_keys = open(str(Path.home())+"/.ssh/authorized_keys", 'w')
    authorized_keys.close()
authorized_keys = open(str(Path.home())+"/.ssh/authorized_keys", 'r')
if pub_key in authorized_keys.read():
    print('The key is already registered')
else:
    authorized_keys.close()
    authorized_keys = open(str(Path.home())+"/.ssh/authorized_keys", 'a')
    authorized_keys.write(pub_key)
    print('We\'re done!')
authorized_keys.close()

#styles = open("./styles/custom.css", "r").read()
styles = "div.prompt, code, output, prompt, kbd, pre, samp {font-family: 'SF Mono', 'Courier New', Courier, monospace, sans-serif !important;}"
display(HTML('<style>' + styles + '</style>'))
os.environ['PATH']=f"{os.environ['PATH']}:/usr/local/bin"

pa_columns=["function", "seed", "size", "power","p1", "p2", "p3", "p4", "p5", "IC", "CPI", "CT", "ET", "L1_MPI", "TLB_MPI", "L1_cache_misses", "TLB_misses"]
default_layers=["misses-compulsory-all", "misses-capacity-all", "hits-all"]

pandas.set_option('display.max_rows', 130)

user = None

RenderedCode =namedtuple("RenderedCode", "source asm cfg cfg_counts gprof call_graph stats mtrace")

def shell_cmd(cmd, shell=False, quiet_on_success=False):
    try:
        if not quiet_on_success:
            print(cmd)
        if shell:
            p = subprocess.run(cmd, shell=True, check=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        else:
            p = subprocess.run(cmd.split(), check=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)

        if not quiet_on_success:
            print(p.stdout.decode())
        return True
    except subprocess.CalledProcessError as e:
        print(e.output.decode())
        return False


    
def do_gprof(exe, gmon="gmon.out", out=None):
    if out is None:
        out = f"{exe}.gprof"
    shell_cmd(f"gprof {exe} > {out}", shell=True, quiet_on_success=True)
    with open(out) as f:
        return HTML(f"<pre>{f.read()}</pre>")

    
def do_call_graph(exe, gmon="gmon.out", root=None, out=None):
    if not root:
        root = "main"
        
    if out is None:
        out = f"{exe}.call_graph.png"
    shell_cmd(f"gprof {exe} | gprof2dot -n0 -e0 -z {root} | dot -Tpng -o {out}", shell=True, quiet_on_success=False)
    return Image(out)

def build_reps(src, asm, obj, function, mtrace=None, stats=None, gmon=None, run=None, *argc, **kwargs):
    if obj.endswith(".exe") and "gprof" in run:
        gprof = do_gprof(obj, gmon)
        call_graph = do_call_graph(obj, gmon, root=function)
    else:
        gprof = None
        call_graph = None
        
    if function:
        cfg_counts=do_cfg(obj,
                          output=f"{obj}-{function}-counts.png",
                          symbol=function,
                          jupyter=True,
                          spacing=kwargs.get('spacing',1),
                          inst_counts=True,
                          remove_assembly=False,
                          trim_addresses=False,
                          trim_comments=False),
        cfg=do_cfg(obj,
                   output=f"{obj}-{function}-cfg.png",
                   symbol=function,
                   jupyter=True,
                   spacing=kwargs.get('spacing',1),
                   number_nodes=kwargs.get('number_nodes', False),
                   remove_assembly=kwargs.get('remove_assembly', False),
                   trim_addresses=kwargs.get('trim_addresses', True),
                   trim_comments=kwargs.get('trim_comments', False))
    else:
        cfg_counts = None
        cfg = None

    print("Done build representations.")    
    return RenderedCode(source=do_render_code(file=src, lang="c++", show=function),
                        asm=do_render_code(file=asm, lang="gas", demangle=kwargs.get("demangle", True), show=function),
                        cfg_counts=cfg_counts,
                        cfg=cfg,
                        gprof = gprof,
                        call_graph = call_graph,
                        stats=stats,
                        mtrace=mtrace)


def render_czoo(file, function, *argc, **kwargs):
    return dict(opt=build_reps(f"{file}_O4", function, *argc, **kwargs),
                unopt=build_reps(file, function, *argc, **kwargs))


def fiddle(fname, function=None, compile=True, name=None, code=None, opt=None, run=None, cmdline=None, perf_cmdline=None, analyze=False, **kwargs):

    # Maybe fiddle should have a liquid interface.  You could create an object
    # that would be a container for some code. and then call methods on it to
    # display different aspects of it.
    #
    # ex = fiddle(code="""....""").cmdline("--size 1000").compile().show_cfg().mtrace()
    # and later...
    # ex.gprof().show_callgraph()
    # ex.perf_counters("--stat-set L1.cfg").plotScatter()
    # ex.plotBar()

    if isinstance(function, str):
        function=[function]
        
    if not cmdline:
        cmdline = ""
    if not perf_cmdline:
        perf_cmdline = ""
    if run is None:
        run = []
        
    if "gprof" in run:
        gprof=True
        compile_together=True
    else:
        gprof= False
        compile_together = False
        
    if opt is None:
        opt = ""

    fname = os.path.join("build",fname)

    tagged_only = kwargs.pop("tagged_only", False)
    if code is not None:
        code = f"{code}\n//{opt}"  # this ensures we modify fname if optimization flags change, so we will recompile.
        updated = False

        if os.path.exists(fname):
            with open(fname, "r") as  f:
                old = f.read()
            if old != code: 
                updated = True
        else:
            updated = True

        if updated:
            if os.path.exists(fname):
                i = 0
                root, ext = os.path.splitext(fname)
                while True:
                    os.makedirs(".fiddle_backups", exist_ok=True)
                    os.makedirs(".fiddle_backups/build", exist_ok=True)
                    p = f".fiddle_backups/{root}_{i:04}{ext}"
                    if not os.path.exists(p):
                        break
                    i += 1
                os.rename(fname, p)

            os.makedirs("build", exist_ok=True)
            with open(fname, "w") as  f:
                f.write(code)
    
    base, _ =  os.path.splitext(fname)

    so = f"{base}.so"
    doto = f"{base}.o"
    exe = "fiddle.exe"
    if compile_together:
        obj = exe
    else:
        obj = so


    if name is None:
        name = base

    stats = f"{name}.csv"

        
    print("Done code generation...")

    if function is None:
        function = [None]
#    print("Done running.")
    if analyze:
        print("Building representations")
        return build_reps(src=fname,
                          asm=f"{base}.s",
                          obj=obj,
                          gprof=gprof,
                          stats=stats,
                          function=function[0],
                          run=run,
                          mtrace=f"./{name}_0.hdf5",
                          **kwargs)
    else:
        return None
    
def funcs(file, funcs, *argc, **kwargs):
    for f in funcs:

        display(HTML(f"<div style='text-align:center; font-weight: bold'><span>{f}</span></div>"))
        reps = build_reps(file, f, *argc, **kwargs)
        display(reps.source)    
        display(reps.asm)
        display(reps.cfg)
        display(reps.cfg_counts)


def side_by_side(function, *argc, **kwargs):
    data = render_czoo("czoo", function, *argc, **kwargs)
    display(HTML("<div style='text-align:center; font-weight: bold'><span>Source</span></div>"))
    display(data['opt'].source)    
    display(HTML("<div style='text-align:center; font-weight: bold'><span>Unoptimized</span></div>"))
    compare([data['unopt'].asm, data['unopt'].cfg])
    display(HTML("<div style='text-align:center; font-weight: bold'><span>Optimized</span></div>"))
    compare([data['opt'].asm, data['opt'].cfg])

    
def stacked(function, *argc, **kwargs):
    data = render_czoo("czoo", function, *argc, **kwargs)
    display(HTML("<div style='text-align:center; font-weight: bold'><span>Source</span></div>"))
    display(data['opt'].source)    
    display(HTML("<div style='text-align:center; font-weight: bold'><span>Unoptimized</span></div>"))
    display(data['unopt'].asm)
    display(data['unopt'].cfg)
    display(HTML("<div style='text-align:center; font-weight: bold'><span>Optimized</span></div>"))
    display(data['opt'].asm)
    display(data['opt'].cfg)

    
def czoo_compare2(function, *argc, **kwargs):
    file = "czoo"
    render_code(f"{file}.cpp", lang="c++", show=function),
    display(HTML("<div style='text-align:center; font-weight: bold'><span>Unoptimized</span></div>"))
    czoo2(function, optimize=False, *argc, **kwargs)
    display(HTML("<div style='text-align:center; font-weight: bold'><span>Optimized</span></div>"))
    czoo2(function, optimize=True, *argc, **kwargs)


def show_png(file):
    return Image(file)

def display_mono(df):
    display(df.style.set_properties(**{'font-family': 'monospace'}))
    
    return


def login(username):
    global user
    user = username
    return  IFrame(f"{os.environ['DJR_SERVER']}/user/web-login?email={username}", width=500, height=400)



def token(token):
    cmd = f"cse142 login {user} --token {token}"
    try:
        print(subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode())
    except subprocess.CalledProcessError as e:
        print(f"""Authentication failed.  Try the following:
  1.  Click "Sign in" again to get a new token.
  2.  Make sure you are using your "@ucsd.edu" email address.
  3.  Make sure you are completely replacing the old token in the command above.

Here's the output of the authentication command:

{e.output.decode()}

If you get something like this:

File "/opt/conda/lib/python3.7/site-packages/pkg_resources/__init__.py", line 792, in resolve
    raise VersionConflict(dist, req).with_context(dependent_req)
pkg_resources.ContextualVersionConflict: (grpcio 1.32.0 (/home/oweng/.local/lib/python3.7/site-packages), Requirement.parse('grpcio<2.0dev,>=1.38.1'), 'google-cloud-pubsub')

that mentions a "ContextualVersionConflict" and includes a path in your home direcotry (e.g., "/home/oweng/.local..."), then you have some python libraries installed in your home directory (probably from an earlier course).  You can fix this with:

mv ~/.local ~/.local-old

If the output shows evidence of a different uncaught exception, contact the course staff.

""")

#         Traceback (most recent call last):
#   File "/opt/conda/lib/python3.7/site-packages/pkg_resources/__init__.py", line 584, in _build_master
#     ws.require(__requires__)
#   File "/opt/conda/lib/python3.7/site-packages/pkg_resources/__init__.py", line 901, in require
#     needed = self.resolve(parse_requirements(requirements))

# During handling of the above exception, another exception occurred:

# Traceback (most recent call last):
#   File "/opt/conda/bin/cse142", line 6, in <module>
#     from pkg_resources import load_entry_point
#   File "/opt/conda/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3254, in <module>
#     @_call_aside
#   File "/opt/conda/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3238, in _call_aside
#     f(*args, **kwargs)
#   File "/opt/conda/lib/python3.7/site-packages/pkg_resources/__init__.py", line 3267, in _initialize_master_working_set
#     working_set = WorkingSet._build_master()
#   File "/opt/conda/lib/python3.7/site-packages/pkg_resources/__init__.py", line 586, in _build_master
#     return cls._build_from_requirements(__requires__)
#   File "/opt/conda/lib/python3.7/site-packages/pkg_resources/__init__.py", line 599, in _build_from_requirements
#     dists = ws.resolve(reqs, Environment())
#   File "/opt/conda/lib/python3.7/site-packages/pkg_resources/__init__.py", line 787, in resolve
#     raise DistributionNotFound(req, requirers)
# pkg_resources.DistributionNotFound: The 'ipython-genutils' distribution was not found and is required by jupyter-contrib-nbextensions, traitlets

    
def plot1(file=None, df=None, field="per_element"):
    if df is None:
        df = render_csv(file)
    std=df[field].std()
    mean=df[field].mean()
    max_v =df[field].max()
    min_v =df[field].min()
    fix, axs = plt.subplots(1,2)
    axs[0].set_ylabel("per_element")
    axs[1].set_ylabel("Count")
    df[field].plot.line(ax=axs[0])
    df[field].plot.hist(ax=axs[1])
    axs[0].set_ybound(0,max_v*2)
    axs[0].set_xlabel("rep")
    axs[1].set_xlabel("per_element") 
    axs[1].set_xbound(1e-8,3e-8)
    plt.tight_layout()
    
    max_error = max(abs(max_v-mean),abs(min_v-mean))
    
    return pd.DataFrame.from_dict(dict(mean_per_rep=[df['ET'].mean()], mean=[mean], max=[max_v], min=[min_v], max_error_percent=[(max_error)/mean*100.0]))
    #f"Mean: {mean:1.2}; std: {std:1.2}; max: {max:1.2}; min: {min:1.2}; range: {max-min:1.2}; max-variation: {(max-min)/mean*100.0:1.2f}%"



def my_render(c):
    try:
        return c._repr_html_()
    except:
        try:
            return c._repr_svg_()
        except:
            return f'<img src="data:image/png;base64,{c._repr_png_()}">'



def compare(content, headings=None):
    if headings is None:
        headings = [""] * len(content)
        
    display(HTML("""
            <style>
        .side-by-side {
            display: flex;
            align-items: stretch;
        }
        .side-by-side-pane {
            margin-right:1em;
            border-right-style: solid;
            border-right-color: black;
            border-right-width: 1px;
            flex: 1;
        }
        .side-by-side-pane .heading{
            font-size: 1.5;
            font-weight: bold;
            text-align:center;
            border-bottom-style: dotted;
            border-bottom-width: 1px;
            border-bottom-color: gray;
            margin-left: 1em;
            margin-right: 1em;

        }
        </style>
        <div class="side-by-side"> """ +
                 
                 "".join([f"<div class='side-by-side-pane'><div class='heading'>{headings[i]}</div><div>{my_render(c)}</div></div>" for (i,c) in enumerate(content)]) +


                 """
        </div>
    """))

def render_code(*argc, **kwargs):
    display(do_render_code(*argc, **kwargs))
def do_render_code(file, lang="c++", show=None, line_numbers=True, trim_ends=False, demangle=None):

    if demangle is None:
        if lang == "gas":
            demangle = True
        else:
            demangle = False

    with open(file) as f:
        if demangle:
            lines = subprocess.check_output('c++filt', stdin=f).decode().split("\n")
        else:
            lines = open(file).read().split("\n")
        
    start_line = 0
    end_line = len(lines)

    if isinstance(show, str):
        if lang == "c++":
            show = (f"[\s\*]{re.escape(show)}\s*\(", "^\}")
        elif lang == "gas":
            show = (f"^{re.escape(show)}:\s*", ".cfi_endproc")
        else:
            raise Exception("Don't know how to find functions in {lang}")

    if show is not None and len(show) == 2:
        if isinstance(show[0], str): # regexes
            started = False
            for n, l in enumerate(lines):
                if not started:
                    if re.search(show[0], l):
                        start_line = n
                        started = True
                        
                else:
                    if re.search(show[1], l):
                        end_line = n + 1
                        break
        else:
            start_line, end_line = show
    elif show is not None:
        raise ValueError(f"{show} is not a good range for displaying code")
    
    if trim_ends:
        start_line += 1
        end_line -= 1
            
    comments = {"c++": "//",
                "gas": ";",
                "python" : "#"}
    
    src = f"{comments.get(lang, '//')} {file}:{start_line+1}-{end_line} ({end_line-start_line} lines)\n"
    src += "\n".join(lines[start_line:end_line])

    return Code(src, language=lang)

import pandas as pd

    
def render_csv(file, columns = None, sort_by=None, average_by=None, skip=0):
    if isinstance(file,list):
        pass
    else:
        file = [file]

    t = []
    for f in file:
        t += glob.glob(f)

    file = t
    
    df = None
    for f in file:
        d = pd.read_csv(f, sep=",")
        if df is None:
            df = d
        else:
            df = df.append(d)
            
    df = df[skip:]
    if sort_by:
        df = df.sort_values(by=sort_by)
    if average_by:
        df = df.groupby(average_by).mean()
        df[average_by] = df.index
    if columns:
        df = df[columns]
    df.reset_index(inplace=True)
    return df

def _(csv, key, row, column, average_by=None):
    df = render_csv(csv, average_by=average_by)
    return df.filter(like="row", axis=key)[column]
    
    
from contextlib import contextmanager

@contextmanager
def layout(subplots, columns=4):
    f = plt.figure()
    rows = int(math.ceil(subplots/columns))
    f.set_size_inches(4*columns, 4*rows)
    def next_fig():
        c = 0
        while True:
            c += 1
            assert c <= subplots, "Too many subplots.  Increase the number you passed to layout()"
#            f.set_size_inches(4*columns, 4*rows)
            yield f.add_subplot(rows, columns, c)

    try:
        yield f, next_fig()
    finally:
        f.figsize=[4*columns, 4*rows]
        plt.tight_layout()
        

import matplotlib.pyplot as plt
def plot2(file=None, df=None, field="per_element"):
    if df is None:
        df = render_csv(file)

    df['incremental_average'] = incremental_average(df['per_element'])
    df['incremental_error'] = (df['per_element'].mean() - df['incremental_average'])/df['per_element'].mean()*100
    df['rep_error'] = (df['per_element'] - df['incremental_average'])/df['per_element'].mean()*100
    print(f"===================================\nMean = {df['per_element'].mean()}\nTotal execution time = {df['ET'].sum()}")

    std = df[field].std()
    mean = df[field].mean()
    max_v = df[field].max()
    min_v = df[field].min()
    
    with layout(subplots=1) as (fig, sub):
        axs = next(sub)
        
        axs.set_ylabel("per_element runtime")
        axs.set_ybound(0, df['per_element'].max()*2)
        axs.set_xlabel("rep")
        axs.set_title("Per-element time for each rep")
        df["per_element"].plot.line(ax=axs)
        axs.plot([0,200], [df["per_element"].mean(),df["per_element"].mean()], label="mean")
        axs.legend()
        return 
        
        axs = next(sub)
        axs.set_ylabel("absolute error (%)")
        axs.set_ybound(0,df['rep_error'].max()*2)
        axs.set_xlabel("rep")
        axs.set_title("Error compared to mean across all reps")
        df["rep_error"].abs().plot.line(ax=axs)

        axs.set_ylabel("absolute error (%)")
        axs.set_ybound(0,df['rep_error'].max()*2)
        axs.set_xlabel("rep")
        axs.set_title("Error compared to mean across all reps")
        df["rep_error"].abs().plot.line(ax=axs)

        axs = next(sub)
      
        axs.set_ylabel("incremental_average")
        axs.set_ybound(0,df['incremental_average'].max()*2)
        axs.set_xlabel("N")
        axs.set_title("Average over the first N reps")
        df["incremental_average"].plot.line(ax=axs)

        axs = next(sub)
        axs.set_ylabel("absolute error (%)")
        axs.set_ybound(0,df['incremental_error'].max()*2)
        axs.set_xlabel("rep")
        df["incremental_error"].abs().plot.line(ax=axs)

        axs = next(sub)
        axs.set_ylabel("Count")
        axs.set_xlabel("per_element") 
        axs.set_xbound(1e-8,3e-8)
        df["per_element"].plot.hist(ax=axs)


def plotPE(file=None, what=None, df=None,  lines=False, columns=4, logx=None, logy=None, average=False, average_by=None, dot_size=5, combined=False, log_autoscale_x=True, log_autoscale_y=True):

    if df is None:
        df = render_csv(file,average_by=average_by)

    colors = ["blue",
              "red",
              "green",
              "purple",
              "orange",
              "yellow"
        ]
    axs = None
    with layout(subplots=len(what), columns=columns) as (fig, sub):
        for i, (x, y) in enumerate(what):
            d = df.copy()
            if not combined or not axs:
                axs = next(sub)
            axs.set_ylabel(y)
            axs.set_xlabel(x)
            axs.set_title(y)

            if logx:
                axs.set_xscale("log", base=logx)
                if not log_autoscale_x:
                    axs.set_xbound(d[x].min(), d[x].max()*1.3)
            else:
                axs.set_autoscalex_on(False)
                axs.set_xbound(0, d[x].max()*1.3)

            if logy:
                axs.set_yscale("log", base=logy)
                if not log_autoscale_y:
                    axs.set_ybound(d[y].min(), d[y].max()*1.3)
            else:
                axs.set_autoscaley_on(False)
                axs.set_ybound(0, d[y].max()*1.3)

                
            if average:
                d = d.groupby(x).mean()
                d[x] = d.index
                #axs.plot.errorbar(x, y, yerr=1, fmt="o")
                d.plot.scatter(y=y, x=x, ax=axs, s=dot_size, c=colors[i % len(colors)] )

                if lines:
                    d.plot.scatter(y=y, x=x, ax=axs, c=colors[i % len(colors)] )

            else:
                d.plot.scatter(y=y, x=x, ax=axs, s=dot_size, c=colors[i%len(colors)])
                if lines:
                    d.plot(y=y, x=x, ax=axs, c=colors[i%len(colors)])

                
def plotPEBar(file=None, what=None, df=None,columns=4, log=False, average=False, average_by=None, skip=0, height=1):
    if df is None:
        df = render_csv(file,average_by=average_by)
        
    rows = int(math.ceil(len(what)/columns))
    f = plt.figure(figsize=[4*columns, 4*rows*height], dpi = 100)
    
    for i, (x, y) in enumerate(what):
        _df = copy.deepcopy(df)
        axs = f.add_subplot(rows, columns, i+ 1)
        axs.set_ylabel(y)
        #axs.set_xlabel(x)
        axs.set_title(y)
        if log:
            #axs.set_xscale("log")
            axs.set_yscale("log")
        else:
            axs.set_ybound(0, _df[y].max()*1.4)
            #axs.set_xbound(0, _df[x].max()*1.1)
            axs.set_autoscalex_on(False)
            axs.set_autoscaley_on(False)
            
        if average:
            _df = _df.groupby(x).mean()
            _df[x] = _df.index
            _df.plot.bar(y=y, x=x, ax=axs)
        else:
            _df.plot.bar(y=y, x=x, ax=axs)
        
        for i, v in enumerate(_df[y]):
            axs.text(i, v, f"{float(v):3.2}", ha='center' )
            
    plt.tight_layout()

            
def incremental_average(d):
    return [d[0:i+1].mean() for i in range(len(d))]


def IC_avg_and_combine(*argc):
    all = render_csv(argc[0])
    all = all[0:0]

    for f in argc:
        df = render_csv(f)
        t = df['function'][0]
        r = dict(function=df['function'][0],
                 IC=df['IC'].sum(),
                 CPI=df['CPI'].mean(),
                 CT=df['CT'].mean(),
                 ET=df['ET'].sum(),
                 cmdlineMHz=df['cmdlineMHz'].mean(),
                 realMHz=df['realMHz'].mean())
        all = all.append(r, ignore_index=True)

    return all

print("Done loading notebook! We're good to go!");
